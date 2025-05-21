"""
pii_redactor.py: Redact/mask PII information to support GDPR and HIPAA compliance.
"""

import re
import pandas as pd
from datacleancraft.models.spacy_model_loader import SpacyModelLoader

# PII entity labels that we want to redact
PII_ENTITIES = {"PERSON", "GPE", "LOC", "ORG", "DATE", "TIME", "MONEY", "EMAIL", "PHONE"}

class PIIRedactor:
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'\b(\+?\d{1,3}[-.\s]?|\()?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b')
    SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    
    def __init__(self, mask_token: str = "[REDACTED]"):
        spacymodelloader = SpacyModelLoader()
        self.nlp = spacymodelloader.load_model()
        self.mask_token = mask_token

    def redact_text(self, text: str) -> str:
        """
        Redact emails, phone numbers, SSNs, and PII entities from text.

        Args:
            text (str): Input text.

        Returns:
            str: Redacted text.
        """
        if not isinstance(text, str):
            return text

        # Redact PII entities using spaCy's NER
        doc = self.nlp(text)
        redacted = text

        for ent in doc.ents:
            if ent.label_ in PII_ENTITIES:
                redacted = redacted.replace(ent.text, self.mask_token)

        # Simple regex-based email/phone fallback
        redacted = self.EMAIL_PATTERN.sub(self.mask_token, redacted)
        redacted = self.PHONE_PATTERN.sub(self.mask_token, redacted)
        redacted = self.SSN_PATTERN.sub(self.mask_token, redacted)

        return redacted

    def redact_dataframe(self, df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
        """
        Redact PII from specified DataFrame columns or all text columns if none are provided.

        Args:
            df (pd.DataFrame): Input DataFrame.
            columns (list): Columns to redact. If None, all text columns are redacted.

        Returns:
            pd.DataFrame: Redacted DataFrame.
        """
        # If no columns specified, select all text columns
        if columns is None:
            columns = df.select_dtypes(include=["object", "string"]).columns.tolist()
        
        for col in columns:
            if col in df.columns:  # Ensure the column exists in the DataFrame
                df[col] = df[col].apply(self.redact_text)
        
        return df