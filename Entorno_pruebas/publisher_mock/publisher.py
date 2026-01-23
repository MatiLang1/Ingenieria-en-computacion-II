import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = "mqtt-broker"
PORT = 1883

TOPICS = {
    "temp": "semillero/sensores/temperatura",
    "luz": "semillero/sensores/luz",
    "nivel": "semillero/sensores/nivel",
    "estado_sistema": "semillero/estado/sistema",
    "buzzer": "semillero/estado/buzzer"
}

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

while True:
    payload = {
        "temperatura": round(random.uniform(18, 35), 1),
        "luz": random.randint(200, 900),
        "nivel": random.choice(["OK", "BAJO"]),
        "estado_sistema": random.choice(["NORMAL", "ALERTA"]),
        "buzzer": random.choice(["ON", "OFF"])
    }

    client.publish(TOPICS["temp"], payload["temperatura"])
    client.publish(TOPICS["luz"], payload["luz"])
    client.publish(TOPICS["nivel"], payload["nivel"])
    client.publish(TOPICS["estado_sistema"], payload["estado_sistema"])
    client.publish(TOPICS["buzzer"], payload["buzzer"])

    print("Publicado:", payload)
    time.sleep(60)
