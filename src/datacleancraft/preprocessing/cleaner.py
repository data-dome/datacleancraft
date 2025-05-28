"""
cleaner.py: Advanced text preprocessing, Text cleaning functions like deduplication, tokenization using spaCy and text correction. 
"""

import string
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
        Correct common spelling mistakes using TextBlob (slow, use optionally).

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

        #Correct spelling
        text = self.correct_spelling(text)

        #Process text through spaCy pipeline for lemmatization and stopword removal
        doc = self.nlp(text)

        #Lemmatize and remove stopwords and punctuation
        text = " ".join([token.lemma_ for token in doc if token.text not in self.stopwords and not token.is_punct])

        # Remove any special characters, keep only alphanumeric and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

        return text
    
    def clean_text(self, 
        text: Optional[str],
        lowercase: bool = True,
        remove_stopwords_punct: bool = True,
        spell_correct: bool = False
    ) -> Optional[str]:
        if not isinstance(text, str):
            return text
        
        if remove_stopwords_punct:
            #Process text through spaCy pipeline for stopword removal and punctuation removal
            doc = self.nlp(text)
            text = " ".join(token.text for token in doc if not token.is_punct and token.text not in self.stopwords)

        if lowercase:
            text = text.lower()

        if spell_correct:
            text = self.correct_spelling(text)

        # Keep only printable, alphanumeric and space characters
        text = "".join(c for c in text if c in string.printable and (c.isalnum() or c.isspace()))

        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

        # Remove extra spaces
        return " ".join(text.split())

    def clean_text_dataframe(self,
        df: pd.DataFrame,
        text_columns: Optional[List[str]] = None,
        lowercase: bool = True,
        remove_stopwords_punct: bool = True,
        spell_correct: bool = False
    ) -> pd.DataFrame:
        cleaned_df = self.remove_duplicates(df.copy())

        if text_columns is None:
            text_columns = cleaned_df.select_dtypes(include=["object", "string"]).columns.tolist()

        for col in text_columns:
            cleaned_df[col] = cleaned_df[col].apply(
                lambda x: self.clean_text(
                    x,
                    lowercase=lowercase,
                    remove_stopwords_punct=remove_stopwords_punct,
                    spell_correct=spell_correct
                )
            )

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