FROM python:3.11-slim

WORKDIR /app

COPY test_system.py .

RUN pip install --no-cache-dir paho-mqtt

CMD ["python", "test_system.py"]
