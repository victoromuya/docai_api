# from celery import shared_task
import os
from services.file_loader import extract_text
from services.preprocess import clean_text, tokenize
from services.extractor import extract_entities, extract_amount
from services.classifier import DocumentClassifier

from api.models import DocumentResult

classifier = DocumentClassifier()
classifier.load("services/models/model.pkl")
 

def process_document(file_path):
    # Step 1: Extract text
    raw_text = extract_text(file_path)

    # Step 2: Preprocess
    cleaned = clean_text(raw_text)
    processed = tokenize(cleaned)

    # Step 3: Classify
    # doc_type = classifier.predict(processed)
    doc_type, confidence = classifier.predict_with_confidence(processed)

    # Step 4: Extract data
    entities, text = extract_entities(raw_text)
    amount = extract_amount(raw_text)

    return {
        "document_type": doc_type,
        "confidence": float(confidence),
        "entities": entities,
        "text": text,
        "amount": amount,
    }
