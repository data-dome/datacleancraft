"""
spacy_model_loader.py: Module to load pre-trained SpaCy models.
"""

import spacy
from spacy.util import is_package
from typing import Optional

class SpacyModelLoader:
    """
    Class to load and manage SpaCy NLP models.
    """

    def __init__(self, model_name: str = "en_core_web_sm"):
        self.model_name = model_name
        self.model = None

    def load_model(self) -> Optional[spacy.language.Language]:
        """
        Loads the specified SpaCy model. Downloads if not available.

        Returns:
            spacy.language.Language: Loaded SpaCy model instance.
        """
        try:
            if not is_package(self.model_name):
                print(f"Model '{self.model_name}' not found locally. Trying to download...")
                from spacy.cli import download
                download(self.model_name)

            self.model = spacy.load(self.model_name)
            return self.model

        except Exception as e:
            print(f"❗ Failed to load SpaCy model '{self.model_name}': {str(e)}")
            return None

    def process_text(self, text: str) -> Optional[spacy.tokens.Doc]:
        """
        Processes text using the loaded SpaCy model.

        Args:
            text (str): Input text.

        Returns:
            spacy.tokens.Doc: Processed Doc object or None.
        """
        if not self.model:
            raise ValueError("Model not loaded. Call load_model() first.")

        return self.model(text)
