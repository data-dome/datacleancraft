"""
pipeline.py - Main Data Cleaning Pipeline for DataCleanCraft.
"""

import pandas as pd
import numpy as np
from datacleancraft.utils.logger import default_logger
from datacleancraft.ingestion.reader import load_data
from datacleancraft.preprocessing.cleaner import TextCleaner
from datacleancraft.preprocessing.pii_redactor import PIIRedactor
from datacleancraft.validation.quality_checker import DataQualityChecker
from datacleancraft.validation.anomaly_detector import AnomalyDetector
from datacleancraft.structuring.standardizer import Standardizer
from datacleancraft.structuring.mapper import FieldMapper
from datacleancraft.export.writer import export_data
from pathlib import Path
from typing import Optional


class DataCleaningPipeline:
    """
    Orchestrates the complete data cleaning workflow.
    """

    def __init__(
        self,
        input_path: str,
        output_path: str,
        export_format: str = "csv",
        column_mapping: Optional[dict] = None,
        anomaly_threshold: float = 0.1,
        redact_pii_enabled: bool = True,
        anomaly_detection_enabled: bool = True,
    ):
        self.input_path = input_path
        self.output_path = output_path
        self.export_format = export_format
        self.column_mapping = column_mapping
        self.anomaly_threshold = anomaly_threshold
        self.logger = default_logger
        self.redact_pii_enabled = redact_pii_enabled
        self.anomaly_detection_enabled = anomaly_detection_enabled

    def run(self):
        """
        Execute the data cleaning pipeline.
        """
        self.logger.info("🚀 Starting DataCleanCraft Pipeline.")

        # Step 1: Load Data
        df = load_data(self.input_path)
        self.logger.info(f"✅ Loaded data with {df.shape[0]} rows and {df.shape[1]} columns.")

        # Step 2: Data Quality Checks
        dataQualityChecker = DataQualityChecker()
        issues = dataQualityChecker.validate(df)
        if issues:
            self.logger.warning(f"⚠️ Data quality issues detected: {issues}")

        # Step 3: Standardize Data
        df = Standardizer().standardize(df)
        self.logger.info(f"✅ Standardized column names and formats.")
    
        # Step 4: Redact PII
        if self.redact_pii_enabled:
            self.logger.info("✅ PII Redaction started.")
            piiRedactor = PIIRedactor()
            df = piiRedactor.redact_dataframe(df)
            self.logger.info("✅ Redacted PII information.")

        # Step 5: Clean Data
        textCleaner = TextCleaner()
        df = textCleaner.clean_text_dataframe(df)
        self.logger.info("✅ Performed basic data cleaning (null handling, trimming, etc.).")

        # Step 6: Map Columns
        if self.column_mapping:
            fieldMapper = FieldMapper(self.column_mapping)
            df = fieldMapper.map_columns(df)
            self.logger.info("✅ Applied column mapping as per provided configuration.")

        # Step 7: Detect Anomalies
        if self.anomaly_detection_enabled:
            self.logger.info("✅ Anomaly detection started.")
            anomaly_detector = AnomalyDetector(threshold=self.anomaly_threshold)
            df_anomaly = anomaly_detector.detect_anomalies(df)
            if(df_anomaly is not None):
                df = pd.concat([df, df_anomaly], axis=1)
            self.logger.info("✅ Anomaly detection completed and results appended.")

        # Step 8: Export Cleaned Data
        export_data(df, self.output_path, format=self.export_format)
        self.logger.info(f"✅ Exported cleaned data to {self.output_path} in {self.export_format.upper()} format.")

        self.logger.info("🎉 DataCleanCraft Pipeline completed successfully.")