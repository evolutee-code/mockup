# Pull official Python base image (Alpine variant)
FROM python:3.12-slim

# Set working directory
WORKDIR /opt/python-projects/app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        python3-dev \
        libffi-dev \
        libssl-dev \
        librdkafka-dev \
        libmagic1  \
        libmagic-dev \
        git \
        curl \
        ffmpeg \
        openssl && \
    pip install --upgrade pip setuptools wheel && \
    pip install aiokafka && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps

# Copy the rest of the project files
COPY ../.. /opt/python-projects/app/