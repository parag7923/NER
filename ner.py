import spacy
from utils import extract_text_from_pdf

nlp = spacy.load('en_core_web_trf')  # Using transformer-based Spacy model for accuracy

def perform_ner(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities