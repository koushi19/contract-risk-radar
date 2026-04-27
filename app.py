from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import pdfplumber
from app.pipeline import analyze_contract

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Helper to extract text from a PDF file."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        raw_text = ""
        
        # 3.1 Priority Order: PDF -> TXT -> Textarea
        file_pdf = request.files.get('file_pdf')
        file_txt = request.files.get('file_txt')
        textarea_text = request.form.get('textarea_text', '').strip()
        
        if file_pdf and file_pdf.filename.endswith('.pdf'):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file_pdf.filename)
            file_pdf.save(path)
            raw_text = extract_text_from_pdf(path)
            os.remove(path) # Cleanup
            
        elif file_txt and file_txt.filename.endswith('.txt'):
            raw_text = file_txt.read().decode('utf-8', errors='ignore')
            
        elif textarea_text:
            raw_text = textarea_text
            
        if not raw_text:
            return render_template('index.html', error="Please provide a contract via PDF, TXT, or Textarea.")
        
        try:
            summary, results = analyze_contract(raw_text)
            return render_template('results.html', summary=summary, results=results)
        except ValueError as e:
            return render_template('index.html', error=str(e))
        except Exception as e:
            return render_template('index.html', error="An unexpected error occurred during analysis.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
