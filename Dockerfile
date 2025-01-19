# Stage 1: Build dependencies
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app/python/packages/autogen-studio

# Upgrade pip to the latest version and install build tools
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir --upgrade pip

# Install Python dependencies directly
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    pydantic \
    openai \
    loguru

# Clean up unnecessary files
RUN apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Stage 2: Final image
FROM python:3.11-slim

# Set working directory
WORKDIR /app/python/packages/autogen-studio

# Add PYTHONPATH to ensure the application package is discoverable
ENV PYTHONPATH="/app/python/packages/autogen-studio:${PYTHONPATH}"

# Copy Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code to the container
COPY . /app/

# Expose the application port
EXPOSE 8000

# Run the application with the correct module path
CMD ["uvicorn", "autogenstudio.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
