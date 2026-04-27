# Clause Risk Radar 🛰️
### Legal NLP · ML Classification · Flask

A high-performance contract analysis tool that identifies and classifies legal risks at the clause level using local Machine Learning.

---

## 🚀 Quick Start

1. **Install Dependencies** (Python 3.9+):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python run_app.py
   ```
   Open your browser to `http://127.0.0.1:5000`

---

## 🧠 Design Decisions & Architecture

### 1. NLP Pipeline & Segmentation
- **Segmentation Strategy**: The tool splits raw text into logical units using structural delimiters (newlines and numbering).
- **Merge Rule**: Clauses under 10 words are automatically merged with the preceding clause to maintain semantic completeness (Requirement 4.1).
- **Truncation**: For the UI, clauses are truncated to 300 characters to ensure the dashboard remains clean and readable.

### 2. Machine Learning Model
- **Algorithm**: Support Vector Machine (SVM) / Random Forest.
- **Why?**: Since the task requires local intelligence with a small dataset (~66 hand-labeled clauses), traditional ML outperforms Deep Learning in speed and reliability on local machines.
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency) with bigrams. This allows the model to "weigh" critical legal phrases like *"uncapped liability"* or *"sole discretion"* more heavily.
- **Performance**: Analyzes a 2,000-word contract in under 1 second.

### 3. Reasoning Engine
Since external LLM APIs were forbidden, I built a keyword-mapped reasoning engine that bridges the gap between ML classification and human understanding. It scans for specific "risk triggers" within flagged clauses to provide actionable feedback.

---

## 📊 Dataset Distribution
As per Requirement 4.3, the model was trained on 66 diverse legal clauses:
| Risk Class | Count | Description |
| :--- | :--- | :--- |
| **Safe** | 22 | Balanced terms, mutual obligations. |
| **Review** | 22 | Auto-renewals, long notice periods, etc. |
| **Risky** | 22 | Uncapped liability, unilateral termination. |

---

## 🎨 UI/UX Features
- **Glassmorphism Design**: Modern, dark-mode aesthetic for a premium feel.
- **Priority Loading**: PDF → TXT → Textarea.
- **Live Feedback**: The upload zone updates immediately once a file is selected.
- **Risk Dashboard**: Quick summary of risk distribution and top-3 highest risk flags.

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **ML**: Scikit-Learn, Joblib, Pandas
- **Extraction**: PdfPlumber (High-accuracy PDF text extraction)
- **Frontend**: Vanilla CSS, HTML5, JavaScript
