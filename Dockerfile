# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Create an isolated virtual environment
RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Create a non-root user
RUN useradd --uid 1000 --user-group --no-create-home app

WORKDIR /app

# Copy the pre-built virtual environment from the builder
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Copy only the application code needed at runtime
COPY --chown=app:app app/ ./app/

# Run as non-root user
USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]