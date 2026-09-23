FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gerador/ ./gerador/
RUN mkdir -p /data

CMD ["python", "-m", "gerador"]
