import pytest
from datacleancraft.models.spacy_model_loader import SpacyModelLoader

@pytest.fixture
def spacy_loader():
    loader = SpacyModelLoader(model_name="en_core_web_sm")
    loader.load_model()
    return loader

def test_model_loading(spacy_loader):
    assert spacy_loader.model is not None, "SpaCy model should be loaded successfully."

def test_process_text(spacy_loader):
    text = "Data cleaning is crucial for analytics."
    doc = spacy_loader.process_text(text)
    print(len(doc))
    print(text.split())
    assert doc is not None, "Processed Doc object should not be None."
    assert len(doc) == len(text.split())+1, "Token count should roughly match word count."

def test_process_text_without_loading():
    loader = SpacyModelLoader(model_name="en_core_web_sm")
    with pytest.raises(ValueError, match="Model not loaded"):
        loader.process_text("Test text.")
