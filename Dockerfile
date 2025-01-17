# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Upgrade pip to the latest version
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir --upgrade pip

# Copy requirements.txt to the container
COPY python/packages/autogen-studio/requirements.txt /app/requirements.txt

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r autogen\python\packages\autogen-studio\requirements.txt && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Install additional dependencies
RUN pip install --no-cache-dir openai azure-openai fastapi uvicorn[standard] pydantic

# Stage 2: Final image
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . /app/

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
