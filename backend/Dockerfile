FROM python:3.11-slim

# Set environment variables for Python performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install system utilities needed for building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Pre-download spaCy NLP models to keep API start times instant
RUN python -m spacy download en_core_web_sm

# Copy the remaining backend source code
COPY . .

# Expose port 7860 (default port for Hugging Face Spaces container)
EXPOSE 7860

# Start Uvicorn ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
