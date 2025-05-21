"""
api.py - FastAPI service for DataCleanCraft pipeline.
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import pandas as pd
import tempfile
from pathlib import Path
from datacleancraft.pipeline import DataCleaningPipeline
from datacleancraft.utils.logger import default_logger

app = FastAPI(
    title="🧹 DataCleanCraft API",
    description="API for automatic data cleaning, PII redaction, anomaly detection, and standardization.",
    version="1.0.0",
)

@app.post("/clean")
async def clean_data(
    file: UploadFile = File(...),
    export_format: str = Form("csv"),
    anomaly_threshold: float = Form(0.1),
):
    """
    Endpoint to clean uploaded CSV/JSON file and return cleaned version.
    """
    try:
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_input:
            contents = await file.read()
            temp_input.write(contents)
            temp_input_path = temp_input.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{export_format}") as temp_output:
            temp_output_path = temp_output.name

        pipeline = DataCleaningPipeline(
            input_path=temp_input_path,
            output_path=temp_output_path,
            export_format=export_format,
            column_mapping=None,
            anomaly_threshold=anomaly_threshold,
        )
        pipeline.run()

        # Load output and return as JSON
        cleaned_df = pd.read_csv(temp_output_path) if export_format == "csv" else pd.read_json(temp_output_path, lines=True)
        response = cleaned_df.to_dict(orient="records")

        default_logger.info("✅ API cleaning request completed successfully.")
        return JSONResponse(content={"status": "success", "data": response})

    except Exception as e:
        default_logger.error(f"❌ API error during cleaning: {str(e)}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
