# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y build-essential
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get remove -y build-essential
RUN apt-get autoremove -y
RUN rm -rf /var/lib/apt/lists/*
RUN pip install openai azure-openai
RUN pip install fastapi uvicorn[standard] pydantic

# Stage 2: Final image
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
