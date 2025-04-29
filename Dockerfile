
# Use official Python slim image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy code
COPY src/ src/
COPY setup.py pyproject.toml README.md LICENSE ./
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir .


EXPOSE 8000

CMD ["uvicorn", "datacleancraft.api:app", "--host", "0.0.0.0", "--port", "8000"]

# Set default command
ENTRYPOINT ["datacleancraft"]


