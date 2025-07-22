# 📦 datacleancraft

**Note** It works with python > 3.8 < 3.13 due to spacy depedency on numpy 1.26.4 which is not supported by python version > 3.13.   

**datacleancraft** is a flexible, privacy-aware, local-first **Data Cleaning and Structuring** toolkit.  
It enables ingestion, preprocessing, schema mapping, anomaly detection, and exporting — with optional GPT/LLM enhancement.

It can be used as:

- ✅ Local Python package (script, batch processing)
- ✅ CLI Tool
- ✅ FastAPI Microservice (Data Cleaning as a Service)

---

## ✨ Features

- **Ingestion**: Load JSON, CSV, XML, Text files
- **Preprocessing**: Tokenization, Lemmatization, Deduplication
- **PII Redaction**: GDPR/HIPAA compliance via automatic masking
- **Structuring**: Map fields into standardized schemas
- **Anomaly Detection**: Pre-trained Autoencoder for numeric anomalies
- **Validation**: Data Quality Checks
- **Exporting**: Save cleaned data as CSV or JSON
- **Model Integration**: GPT fallback with OpenAI key, SpaCy lightweight NLP models
- **FastAPI Interface**: Serve it via simple REST APIs
- **Privacy First**: Local processing unless GPT is explicitly used
- **Logging**: Standard Python logging throughout
- **Ready for Docker**: Containerize easily

---

## 🏗 Project Structure
datacleancraft/ ├── src/ │ └── datacleancraft/ │ ├── ingestion/ │ │ ├── reader.py │ │ └── detector.py │ ├── preprocessing/ │ │ ├── cleaner.py │ │ └── pii_redactor.py │ ├── structuring/ │ │ ├── mapper.py │ │ └── standardizer.py │ ├── validation/ │ │ ├── anomaly_detector.py │ │ └── quality_checker.py │ ├── export/ │ │ └── writer.py │ ├── models/ │ │ ├── spacy_model_loader.py │ │ ├── gpt_integration.py │ │ └── autoencoder_loader.py │ ├── utils/ │ │ ├── logger.py │ │ └── error_handler.py │ └── pipeline.py ├── tests/ │ └── test_*.py ├── cli.py ├── app.py ├── setup.py ├── pyproject.toml ├── requirements.txt ├── Dockerfile ├── README.md ├── LICENSE └── .gitignore


---

## 🚀 Installation

```bash
# Clone
git clone https://github.com/yourname/datacleancraft.git
cd datacleancraft

# Install
pip install -e .

# install dependencies only
pip install -r requirements.txt

## 🛠 Usage
# 1. As a Python Library
from datacleancraft.pipeline import run_pipeline

result = run_pipeline(
    input_path="data/raw/customers.csv",
    output_path="data/cleaned/customers_clean.csv",
    export_format="csv",
    redact_pii=True
)

print(result.head())

# 2. From CLI

python cli.py --input data/raw/sample.csv --output data/cleaned/sample_clean.csv --format csv --redact
Options:
--input	Input file path (CSV, JSON, XML, TXT)
--output	Output file path
--format	Output format: csv, json
--redact	Redact PII fields (optional)

# 3. Run FastAPI Server

uvicorn src.datacleancraft.api:app --reload
curl -X POST "http://127.0.0.1:8000/clean/" -F "file=@path/to/your.csv"

## 🧪 Run Tests
pytest tests/

## 🐳 Docker
docker build -t datacleancraft .
docker run -p 8000:8000 datacleancraft

Access FastAPI at http://localhost:8000/docs

## 📋 Requirements
Python 3.8+
pandas
numpy
torch
spacy
fastapi
uvicorn
openai (optional for GPT)

(See requirements.txt for full list.)

## 🛡️ Compliance
PII redaction helps towards GDPR, HIPAA compliance

Local-first model loading (SpaCy, Autoencoder) to protect data privacy

GPT integration is optional and requires API key

## 📜 License
MIT License. See LICENSE.

## 🤝 Contributions
Pull requests are welcome! Feel free to submit:

New format support (Parquet, SQL, etc.)

Improved anomaly detection models

More advanced PII detection

Better CLI options

## 🌟 Future Roadmap

 Custom training the autoencoder on anomaly detection.

 Falling back on GPT / Gemini LLMs instead of the local Spacy model to boost accuracy, handle different cultural aspects, and cover a wider range of exceptional cases.

 Native Parquet & Feather file support

 PDF/Text file ingestion using OCR

 Named Entity Recognition for better redaction

 Web dashboard interface

 Automatic schema inference

