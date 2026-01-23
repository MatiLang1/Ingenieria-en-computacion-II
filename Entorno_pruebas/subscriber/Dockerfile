FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY subscriber.py .

RUN pip install --no-cache-dir paho-mqtt

CMD ["python", "subscriber.py"]
