import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = "mqtt-broker"
PORT = 1883

TOPICS = {
    "temp": "almacigo/sensores/temperatura",
    "luz": "almacigo/sensores/luz",
    "agua": "almacigo/sensores/nivel_agua",
    "estado": "almacigo/sistema/estado"
}

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

while True:
    payload = {
        "temperatura": round(random.uniform(18, 35), 1),
        "luz": random.randint(200, 900),
        "nivel_agua": random.choice(["OK", "BAJO"]),
        "estado_sistema": random.choice(["NORMAL", "ALERTA"])
    }

    client.publish(TOPICS["temp"], payload["temperatura"])
    client.publish(TOPICS["luz"], payload["luz"])
    client.publish(TOPICS["agua"], payload["nivel_agua"])
    client.publish(TOPICS["estado"], payload["estado_sistema"])

    print("Publicado:", payload)
    time.sleep(60)
