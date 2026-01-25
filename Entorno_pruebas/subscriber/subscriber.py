import time
from collections import deque
import paho.mqtt.client as mqtt

BROKER = "mqtt-broker" #nombre del contenedor del broker MQTT (definido en el nombre del servicio en el docker compose)
PORT = 1883 #puerto del broker MQTT (definido en el servicio "mqtt-broker" en el docker compose, es el puerto virtual aunq tambien esta mapeado al de la PC)

MAX_REGISTROS = 500 #cantidad maxima de registros a guardar
registros = deque(maxlen=MAX_REGISTROS) #cola de registros (deque es una cola con tamaño maximo)

def on_message(msg): #se ejecuta cuando se recibe un mensaje
    registro = {
        "topic": msg.topic.decode(), #decodifica el topic que viene en formato bytes a texto plano
        "valor": msg.payload.decode() #decodifica el payload que viene en formato bytes a texto plano
    }
    registros.append(registro)
    print("Recibido:", registro)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message


#el 60 es el "Keep Alive" en s, le dice al broker: si no recibes ninguna señal mía (mensaje o ping) por más de 60 segundos, asume que me he desconectado. El cliente envía pings automáticos usando el meotdo .loop_forever() para mantener la conexión viva

while True:
    try:
        client.connect(BROKER, PORT, 60)
        break
    except ConnectionRefusedError:
        print("Broker no listo, reintentando en 2s")
        time.sleep(2)

client.subscribe("semillero/#") #se suscribe a todos los topics que empiecen con "semillero/"
client.loop_forever() #esto envia los pings para mantener la conexion con el broker viva, si por mas de 60s el broker MQTT no recibe ningun ping, asume que el cliente se desconectó
