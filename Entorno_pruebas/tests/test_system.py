import time
import paho.mqtt.client as mqtt

BROKER = "mqtt-broker"
PORT = 1883
recibido = False

def on_message(client, userdata, msg):
    global recibido
    recibido = True
    print("Test OK - mensaje recibido:", msg.topic)

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.subscribe("semillero/#")

client.loop_start()
time.sleep(65)

if recibido:
    print("TEST PASADO")
else:
    print("TEST FALLIDO")

client.loop_stop()
