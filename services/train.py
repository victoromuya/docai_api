from mlflow import evaluate
from evaluate import evaluate_model
from file_loader import extract_text
from preprocess import clean_text, tokenize
from classifier import DocumentClassifier
import os


def load_dataset(data_dir, limit_per_class):
    texts = []
    labels = []

    for label in os.listdir(data_dir):
        folder = os.path.join(data_dir, label)

        if not os.path.isdir(folder):
            continue

        files = os.listdir(folder)[:limit_per_class]  # LIMIT HERE

        for file in files:
            path = os.path.join(folder, file)
            print(f"Processing {path}...")

            try:
                text = extract_text(path)
                processed = tokenize(clean_text(text))

                texts.append(processed)
                labels.append(label)

                print(f"Loaded {file} as {label}")

            except Exception as e:
                print(f"Skipping {file}: {e}")
                continue

    return texts, labels


# Load dataset
texts, labels = load_dataset("data/", limit_per_class=20)

# Train model
print(f"Training on {len(texts)} documents...")
classifier = DocumentClassifier()
classifier.train(texts, labels)


#evaluate
print("Evaluating model...")
metrics = evaluate_model(classifier.model, texts, labels)

# Save model
classifier.save("model/model.pkl")

print("Model trained and saved!")
