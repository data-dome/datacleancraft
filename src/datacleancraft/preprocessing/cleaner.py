"""
cleaner.py: Text cleaning functions like tokenization, lemmatization, deduplication.
"""
"""
Cleaner module for advanced text preprocessing operations using spaCy and text correction.
"""

import pandas as pd
import re
from typing import Optional , List
from datacleancraft.models.spacy_model_loader import SpacyModelLoader
from textblob import Word

class TextCleaner:
    
    def __init__(self):
        spacymodelloader = SpacyModelLoader()
        self.nlp = spacymodelloader.load_model()
        self.stopwords = set(self.nlp.Defaults.stop_words)

    def tokenize_and_lemmatize(self, texts: List[str]) -> List[List[str]]:
        """
        Tokenize and lemmatize input texts.

        Args:
            texts (List[str]): List of input texts.

        Returns:
            List[List[str]]: List of lists containing lemmas.
        """
        cleaned_texts = []
        for doc in self.nlp.pipe(texts, disable=["ner", "parser"]):
            lemmas = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
            cleaned_texts.append(lemmas)
        return cleaned_texts

    def correct_spelling(self, text: str) -> str:
        """
        Correct common spelling mistakes using TextBlob.

        Args:
            text (str): Input text.

        Returns:
            str: Text with corrected spelling.
        """
        corrected = " ".join([Word(word).correct() for word in text.split()])
        return corrected

    def clean_text(self, text: Optional[str]) -> Optional[str]:
        """
        Clean a single text value with NLP: trim spaces, lowercase, lemmatization,
        stopword removal, spelling correction, punctuation removal, etc.

        Args:
            text (str or None): Input text.

        Returns:
            str or None: Cleaned and processed text.
        """
        if not isinstance(text, str):
            return text

        text = text.strip().lower()

        # Correct spelling
        text = self.correct_spelling(text)

        # Process text through spaCy pipeline for lemmatization and stopword removal
        doc = self.nlp(text)

        # Lemmatize and remove stopwords and punctuation
        text = " ".join([token.lemma_ for token in doc if token.text not in self.stopwords and not token.is_punct])

        # Remove any special characters, keep only alphanumeric and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

        return text

    def clean_text_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply advanced text cleaning across a DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: Cleaned DataFrame with NLP-based cleaning.
        """
        cleaned_df = df.copy()

        # Apply the clean_text function across all string columns
        for col in cleaned_df.select_dtypes(include=["object", "string"]).columns:
            cleaned_df[col] = cleaned_df[col].apply(self.clean_text)

        return cleaned_df

    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
            """
            Remove duplicate rows from a DataFrame.

            Args:
                df (pd.DataFrame): Input DataFrame.
                subset (List[str], optional): Columns to consider for identifying duplicates.

            Returns:
                pd.DataFrame: De-duplicated DataFrame.
            """
            return df.drop_duplicates(subset=subset).reset_index(drop=True)