# """
# Orchestrates the complete data cleaning pipeline.
# """

# from datacleancraft.ingestion.reader import read_file
# from datacleancraft.preprocessing.cleaner import clean_data
# from datacleancraft.structuring.mapper import map_fields, standardize_types
# from datacleancraft.preprocessing.pii_redactor import redact_pii
# from datacleancraft.validation.anomaly_detector import detect_anomalies
# from datacleancraft.models.gpt_integration import gpt_parse
# from datacleancraft.export.writer import write_file
# import pandas as pd
# from typing import Dict, Optional

# def run_pipeline(
#     input_path: str,
#     output_path: str,
#     field_mapping: Optional[Dict[str, str]] = None,
#     type_mapping: Optional[Dict[str, str]] = None,
#     redact_pii_enabled: bool = True,
#     anomaly_detection_enabled: bool = True,
#     gpt_fallback_enabled: bool = False
# ):
#     """
#     Runs the full data ingestion, cleaning, mapping, PII redaction, anomaly detection, and export pipeline.
#     """
#     print("[INFO] Reading file...")
#     df = read_file(input_path)

#     print("[INFO] Cleaning data...")
#     df = clean_data(df.to_dict(orient="records"))

#     if field_mapping:
#         print("[INFO] Mapping fields...")
#         df = map_fields(df, field_mapping)

#     if type_mapping:
#         print("[INFO] Standardizing types...")
#         df = standardize_types(df, type_mapping)

#     if redact_pii_enabled:
#         print("[INFO] Redacting PII...")
#         for col in df.select_dtypes(include=['object']).columns:
#             df[col] = df[col].apply(redact_pii)

#     if anomaly_detection_enabled:
#         print("[INFO] Detecting anomalies...")
#         anomalies = detect_anomalies(df)
#         df["anomaly_detected"] = anomalies

#     if gpt_fallback_enabled:
#         print("[INFO] Running GPT fallback parsing...")
#         for col in df.select_dtypes(include=['object']).columns:
#             df[col] = df[col].apply(lambda x: gpt_parse(x) if isinstance(x, str) else x)

#     print("[INFO] Writing output file...")
#     write_file(df, output_path)

#     print("[INFO] Pipeline completed successfully.")



# from datacleancraft.ingestion.reader import read_file
# from datacleancraft.ingestion.detector import DataTypeDetector
# from datacleancraft.preprocessing.cleaner import DataCleaner
# from datacleancraft.preprocessing.pii_redactor import PiiRedactor
# from datacleancraft.validation.quality_checker import DataQualityChecker
# from datacleancraft.export.writer import export_data

# def run_pipeline(
#     input_path: str,
#     output_path: str,
#     export_format: str = "csv",
#     redact_pii: bool = False
# ) -> pd.DataFrame:
#     """
#     Full data cleaning pipeline.
#     """

#     # Step 1: Read raw data
#     df = read_file(input_path)

#     # Step 2: Detect data types
#     detector = DataTypeDetector()
#     type_info = detector.detect(df)
#     print("[INFO] Detected Types:\n", type_info)

#     # Step 3: Basic Cleaning
#     cleaner = DataCleaner()
#     df = cleaner.clean(df)

#     # Step 4: Optional PII Redaction
#     if redact_pii:
#         redactor = PiiRedactor()
#         df = redactor.redact(df)

#     # Step 5: Validate quality
#     checker = DataQualityChecker()
#     checker.validate(df)

#     # Step 6: Export cleaned data
#     export_data(df, output_path, format=export_format)

#     return df
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
    ):
        self.input_path = input_path
        self.output_path = output_path
        self.export_format = export_format
        self.column_mapping = column_mapping
        self.anomaly_threshold = anomaly_threshold
        self.logger = default_logger

    def run(self):
        """
        Execute the data cleaning pipeline.
        """
        self.logger.info("🚀 Starting DataCleanCraft Pipeline.")

        # Step 1: Load Data
        df = load_data(self.input_path)
        self.logger.info(f"✅ Loaded data with {df.shape[0]} rows and {df.shape[1]} columns.")
        print(df)
        # Step 2: Data Quality Checks
        dataQualityChecker = DataQualityChecker()
        issues = dataQualityChecker.validate(df)
        if issues:
            self.logger.warning(f"⚠️ Data quality issues detected: {issues}")

        # Step 3: Standardize Data
        df = Standardizer().standardize(df)
        self.logger.info(f"✅ Standardized column names and formats.")
        print(df)
        # Step 4: Redact PII
        piiRedactor = PIIRedactor()
        df = piiRedactor.redact_dataframe(df)
        self.logger.info("✅ Redacted PII information.")
        print(df)
        # Step 5: Clean Data
        textCleaner = TextCleaner()
        df = textCleaner.clean_text_dataframe(df)
        self.logger.info("✅ Performed basic data cleaning (null handling, trimming, etc.).")
        print(df)
        # Step 6: Map Columns
        if self.column_mapping:
            fieldMapper = FieldMapper(self.column_mapping)
            df = fieldMapper.map_columns(df)
            self.logger.info("✅ Applied column mapping as per provided configuration.")

          # Step 7: Detect Anomalies
        anomaly_detector = AnomalyDetector(threshold=self.anomaly_threshold)
        df_anomaly = anomaly_detector.detect_anomalies(df)
        # df["anomaly_score"] = scores
        # df["is_anomaly"] = anomalies
        if(df_anomaly is not None):
            df = pd.concat([df, df_anomaly], axis=1)
        self.logger.info("✅ Anomaly detection completed and results appended.")

        # Step 8: Export Cleaned Data
        export_data(df, self.output_path, format=self.export_format)
        self.logger.info(f"✅ Exported cleaned data to {self.output_path} in {self.export_format.upper()} format.")

        self.logger.info("🎉 DataCleanCraft Pipeline completed successfully.")


# if __name__ == "__main__":
#     # Example run (for manual testing)
#     pipeline = DataCleaningPipeline(
#         input_path="data/input/sample.csv",
#         output_path="data/output/cleaned_data.csv",
#         export_format="csv",
#         column_mapping={"OldName": "NewName"},  # optional
#         anomaly_threshold=0.1,
#     )
#     pipeline.run()
