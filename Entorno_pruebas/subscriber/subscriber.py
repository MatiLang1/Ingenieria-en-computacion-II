#Codigo suscriptor MQTT (este genera un JSON con los datos recibidos, aprovechando el volumen de docker)
import time
import json
import os
from collections import deque
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "mqtt-broker"
PORT = 1883
MAX_REGISTROS = 500
JSON_FILE = "registros_mqtt.json"

# Usamos deque para mantener los 500 en memoria, pero también persistiremos en disco
registros = deque(maxlen=MAX_REGISTROS)

def guardar_en_disco():
    """Guarda la cola de registros actual en un archivo JSON."""
    try:
        with open(JSON_FILE, "w") as f:
            # Convertimos la deque a lista para que sea serializable
            json.dump(list(registros), f, indent=4)
    except Exception as e:
        print(f"Error al guardar JSON: {e}")

def on_message(client, userdata, msg):
    #estructuramos el registro con tiempo
    nuevo_dato = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": msg.topic,
        "valor": msg.payload.decode()
    }
    
    registros.append(nuevo_dato)
    
    #actualizamos el JSON cada vez que llega un mensaje
    guardar_en_disco()
    
    print(f"Recibido y guardado: {nuevo_dato['topic']} -> {nuevo_dato['valor']}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

#cargar registros previos si el archivo ya existe (para no perder datos al reiniciar)
if os.path.exists(JSON_FILE):
    try:
        with open(JSON_FILE, "r") as f:
            datos_previos = json.load(f)
            registros.extend(datos_previos)
            print(f"Se cargaron {len(datos_previos)} registros previos del disco.")
    except:
        pass

#manejamos la conexion del suscriptor con el broker
while True:
    try:
        client.connect(BROKER, PORT, 60)
        break
    except ConnectionRefusedError:
        print("Broker no listo, reintentando en 2s")
        time.sleep(2)

client.subscribe("semillero/#")
print("Suscriptor conectado y esperando mensajes...")
client.loop_forever()


#Codigo anterior (suscriptor MQTT, sin generar JSON)
# import time
# from collections import deque
# import paho.mqtt.client as mqtt

# BROKER = "mqtt-broker" #nombre del contenedor del broker MQTT (definido en el nombre del servicio en el docker compose)
# PORT = 1883 #puerto del broker MQTT (definido en el servicio "mqtt-broker" en el docker compose, es el puerto virtual aunq tambien esta mapeado al de la PC)

# MAX_REGISTROS = 500 #cantidad maxima de registros a guardar
# registros = deque(maxlen=MAX_REGISTROS) #cola de registros (deque es una cola con tamaño maximo)

# def on_message(client, userdata,msg): #se ejecuta cuando se recibe un mensaje
#     registro = {
#         "topic": msg.topic, #el topic ya viene en formato string (texto plano)
#         "valor": msg.payload.decode() #decodifica el payload que viene en formato bytes a texto plano
#     }
#     registros.append(registro)
#     print("Recibido:", registro)

# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# client.on_message = on_message


# #el 60 es el "Keep Alive" en s, le dice al broker: si no recibes ninguna señal mía (mensaje o ping) por más de 60 segundos, asume que me he desconectado. El cliente envía pings automáticos usando el meotdo .loop_forever() para mantener la conexión viva

# while True:
#     try:
#         client.connect(BROKER, PORT, 60)
#         break
#     except ConnectionRefusedError:
#         print("Broker no listo, reintentando en 2s")
#         time.sleep(2)

# client.subscribe("semillero/#") #se suscribe a todos los topics que empiecen con "semillero/"
# client.loop_forever() #esto envia los pings para mantener la conexion con el broker viva, si por mas de 60s el broker MQTT no recibe ningun ping, asume que el cliente se desconectó



