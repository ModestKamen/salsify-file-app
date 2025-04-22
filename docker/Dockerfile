# Use Python 3.13 slim as base image
FROM python:3.13-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files for building wheels
COPY pyproject.toml .
RUN pip install build && python -m build --wheel

# Final stage
FROM python:3.13-slim

WORKDIR /app

# Copy only necessary files
COPY file_api_app/ ./file_api_app/
COPY pyproject.toml .

# Copy wheels from builder stage
COPY --from=builder /app/dist/*.whl /wheels/
RUN pip install --no-cache-dir /wheels/*

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "-m", "file_api_app"]