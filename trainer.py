import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
import os

def train_model():
    # 1. Load the dataset
    if not os.path.exists('data.csv'):
        print("Error: data.csv not found.")
        return

    df = pd.read_csv('data.csv')
    
    # Ensure no empty rows
    df = df.dropna()

    # 2. Define the pipeline
    # TF-IDF converts text to numerical features
    # RandomForest is robust for small datasets
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # 3. Train the model
    print("Training the model...")
    pipeline.fit(df['text'], df['label'])

    # 4. Save the model
    # We save the entire pipeline so it handles vectorization automatically
    joblib.dump(pipeline, 'model.joblib')
    print("Model saved as model.joblib")

    # 5. Quick self-test with the samples from the assignment
    test_clauses = [
        "The Client shall indemnify and hold harmless the Vendor from any and all claims... with no upper limit on the amount recoverable by the Vendor.",
        "Either party may terminate this agreement with 30 days written notice.",
        "This agreement shall automatically renew for successive one-year terms unless either party provides written notice of non-renewal at least 60 days prior..."
    ]
    
    predictions = pipeline.predict(test_clauses)
    for clause, label in zip(test_clauses, predictions):
        print(f"Test Clause: {clause[:50]}... -> Prediction: {label}")

if __name__ == "__main__":
    train_model()
