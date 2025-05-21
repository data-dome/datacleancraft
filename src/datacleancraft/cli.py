
"""
cli.py - Command-line interface for DataCleanCraft pipeline.
"""

import click
from datacleancraft.pipeline import DataCleaningPipeline
from datacleancraft.utils.logger import default_logger

@click.command()
@click.option('--input-path', type=str, required=True, help='Path to input file (CSV or JSON).')
@click.option('--output-path', type=str, required=True, help='Path to output cleaned file.')
@click.option('--export-format', type=click.Choice(['csv', 'json']), default='csv', show_default=True, help='Export format.')
@click.option('--anomaly-threshold', type=float, default=0.1, show_default=True, help='Threshold for anomaly detection.')
@click.option('--column-mapping', type=str, default=None, help='Optional column mapping in format old1:new1,old2:new2')
@click.option('--redact-pii', type=bool, default=True, help='Enable or disable PII redaction.')
@click.option('--anomaly-detection', type=bool, default=True, help='Enable or disable anomaly detection.')
def run_pipeline(input_path, output_path, export_format, anomaly_threshold, column_mapping, redact_pii, anomaly_detection):
    """
    CLI entry point for running the DataCleanCraft cleaning pipeline.
    """
    default_logger.info("🚀 Starting CLI interface...")

    mapping_dict = None
    if column_mapping:
        mapping_dict = dict(item.split(":") for item in column_mapping.split(","))

    pipeline = DataCleaningPipeline(
        input_path=input_path,
        output_path=output_path,
        export_format=export_format,
        column_mapping=mapping_dict,
        anomaly_threshold=anomaly_threshold,
        redact_pii_enabled=redact_pii, 
        anomaly_detection_enabled=anomaly_detection,

    )

    pipeline.run()

    default_logger.info("🎉 Cleaning completed via CLI successfully!")

if __name__ == "__main__":
    run_pipeline()
