FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir paho-mqtt

COPY subscriber.py .

CMD ["python", "subscriber.py"]
