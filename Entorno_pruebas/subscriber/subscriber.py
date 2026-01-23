import json
import time
from collections import deque
import paho.mqtt.client as mqtt

BROKER = "mqtt-broker"
PORT = 1883

MAX_REGISTROS = 500
registros = deque(maxlen=MAX_REGISTROS)

def on_message(client, userdata, msg):
    registro = {
        "topic": msg.topic,
        "valor": msg.payload.decode()
    }
    registros.append(registro)
    print("Recibido:", registro)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

while True:
    try:
        client.connect(BROKER, PORT, 60)
        break
    except ConnectionRefusedError:
        print("Broker no listo, reintentando en 2s")
        time.sleep(2)

client.subscribe("semillero/#")
client.loop_forever()
