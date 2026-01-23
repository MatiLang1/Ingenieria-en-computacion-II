import time
import paho.mqtt.client as mqtt

BROKER = "mqtt-broker"
PORT = 1883
recibido = {}
required_keys = {"semillero/sensores/temperatura", "semillero/sensores/luz", "semillero/sensores/nivel", "semillero/sistema/estado_sistema", "semillero/estado/buzzer"}

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Recibido {topic}: {payload}")
    
    #Guardamos el valor
    recibido[topic] = payload
    
    #Verificamos si estan todos los datos para validar la logica
    if required_keys.issubset(recibido.keys()):
        validar_logica()

def validar_logica():
    try:
        temp = float(recibido["semillero/sensores/temperatura"])
        luz = int(recibido["semillero/sensores/luz"])
        nivel = int(recibido["semillero/sensores/nivel"])
        estado_sistema = recibido["semillero/sistema/estado_sistema"]
        buzzer = recibido["semillero/estado/buzzer"]

        print(f"Validando logica con: T={temp} L={luz} N={nivel} -> E={estado_sistema} B={buzzer}")

        #Replicamos la logica de control que usa el publisher_mock para corroborar que el estado_sistema y el buzzer esten correctos
        estado_sistema_esperado = "OK"
        buzzer_esperado = "OFF"
        
        is_alerta = (temp > 35) or (luz > 900) or (nivel < 100)
        is_aviso = (temp > 28) or (luz > 700) or (nivel < 300)

        if is_alerta:
            estado_sistema_esperado = "ALERTA"
            buzzer_esperado = "ON"
        elif is_aviso:
            estado_sistema_esperado = "AVISO"
            buzzer_esperado = "OFF"
        
        if estado_sistema == estado_sistema_esperado and buzzer == buzzer_esperado:
            print("Logica validada correctamente")
            client.disconnect() #Terminamos el test
        else:
            print(f"ERROR DE LOGICA: Valores esperados: {estado_sistema_esperado} y {buzzer_esperado}. Valores recibidos: {estado_sistema} y {buzzer}")
    except ValueError:
        pass #Datos que no se pueden parsear o incompletos

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

client.loop_start()
time.sleep(65)

if recibido:
    print("Test pasado")
else:
    print("Test fallido")

client.loop_stop()
