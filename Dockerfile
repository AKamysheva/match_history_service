FROM python:3.13.10-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtual environment inside the container
RUN poetry config virtualenvs.create false
# Install dependencies (option no-interaction - Do not ask any interactive question; option no-root - Do not install the root package)
RUN poetry install --no-interaction --no-root

COPY . .

EXPOSE 8500
