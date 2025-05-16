FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main_server.py .

CMD ["uvicorn", "main_server:server", "--host", "0.0.0.0", "--port", "8000"]