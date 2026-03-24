import re
import spacy

nlp = spacy.load("en_core_web_sm")


def clean_text(text):
    text = re.sub(r"\n+", " ", text)  # remove new lines
    text = re.sub(r"\s+", " ", text)  # normalize spaces
    return text.lower()


def tokenize(text):
    doc = nlp(text)
    return " ".join(
        [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    )
