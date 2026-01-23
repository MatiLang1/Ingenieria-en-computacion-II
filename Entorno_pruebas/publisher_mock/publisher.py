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

#Umbrales de Aviso y Alerta
TEMP_AVISO = 28
TEMP_ALERTA = 35
LUZ_AVISO = 700
LUZ_ALERTA = 900
NIVEL_AVISO = 300
NIVEL_ALERTA = 100

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
while True:
    try:
        client.connect(BROKER, PORT, 60)
        break
    except ConnectionRefusedError:
        print("Broker no listo, reintentando en 2s")
        time.sleep(2)

while True:
    # Generar valores aleatorios
    temp = round(random.uniform(10, 40), 1)
    luz = random.randint(0, 1023)
    nivel = random.randint(0, 1023)

    # Determinar Estado_sistema y Buzzer
    estado_sistema = "OK"
    buzzer = "OFF"
    
    #Logica de Alerta, Aviso y OK
    is_alerta = (temp > TEMP_ALERTA) or (luz > LUZ_ALERTA) or (nivel < NIVEL_ALERTA)
    is_aviso = (temp > TEMP_AVISO) or (luz > LUZ_AVISO) or (nivel < NIVEL_AVISO)

    if is_alerta:
        estado_sistema = "ALERTA"
        buzzer = "ON"
    elif is_aviso:
        estado_sistema = "AVISO"
        buzzer = "OFF"

    payload = {
        "temperatura": temp,
        "luz": luz,
        "nivel": nivel,
        "estado_sistema": estado_sistema,
        "buzzer": buzzer
    }

    client.publish(TOPICS["temp"], payload["temperatura"])
    client.publish(TOPICS["luz"], payload["luz"])
    client.publish(TOPICS["nivel"], payload["nivel"])
    client.publish(TOPICS["estado_sistema"], payload["estado_sistema"])
    client.publish(TOPICS["buzzer"], payload["buzzer"])

    print("Publicado:", payload)
    time.sleep(60)
