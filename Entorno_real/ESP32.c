#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11

#define LDR_PIN 34
#define NIVEL_PIN 35

#define LED_VERDE 26
#define LED_ROJO 27
#define BUZZER 25

const char* ssid = "WIFI_de_la_red"; // Cambiar al Wi-Fi de la red
const char* password = "Password_de_la_red"; // Cambiar al Password de la red

const char* mqtt_server = "192.168.0.24"; // IP de mi pc (q tiene corriendo al broker mqtt). Cambiar al IP del broker MQTT
const int mqtt_port = 1883; // Puerto de la ESP32 en MQTT

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

bool buzzerState = false;
String estadoSistema = "NORMAL";

unsigned long lastPublish = 0;
const unsigned long interval = 60000; // 1 minuto

void setupWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) msg += (char)payload[i];

  if (String(topic) == "semillero/control/buzzer" && msg.indexOf("OFF") != -1) {
    buzzerState = false;
    digitalWrite(BUZZER, LOW);
    client.publish("semillero/estado/buzzer", "{ \"buzzer\": \"OFF\" }");
  }
}

void reconnectMQTT() {
  while (!client.connected()) {
    if (client.connect("ESP32_Semillero")) {
      client.subscribe("semillero/control/buzzer");
    } else {
      delay(2000);
    }
  }
}

void evaluarEstado(float temp, int nivel) {
  if (temp > 35 || nivel < 500) {
    estadoSistema = "ALERTA";
    digitalWrite(LED_ROJO, HIGH);
    digitalWrite(LED_VERDE, LOW);
    buzzerState = true;
    digitalWrite(BUZZER, HIGH);
  } else {
    estadoSistema = "NORMAL";
    digitalWrite(LED_ROJO, LOW);
    digitalWrite(LED_VERDE, HIGH);
    buzzerState = false;
    digitalWrite(BUZZER, LOW);
  }
}

void publishAll(float temp, int luz, int nivel) {
  char buf[80];

  sprintf(buf, "{ \"value\": %.2f }", temp);
  client.publish("semillero/sensores/temperatura", buf);

  sprintf(buf, "{ \"value\": %d }", luz);
  client.publish("semillero/sensores/luz", buf);

  sprintf(buf, "{ \"value\": %d }", nivel);
  client.publish("semillero/sensores/nivel", buf);

  sprintf(buf, "{ \"estado\": \"%s\" }", estadoSistema.c_str());
  client.publish("semillero/estado/sistema", buf);

  client.publish("semillero/estado/buzzer",
    buzzerState ? "{ \"buzzer\": \"ON\" }" : "{ \"buzzer\": \"OFF\" }");
}

void setup() {
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  dht.begin();
  setupWiFi();

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) reconnectMQTT();
  client.loop();

  if (millis() - lastPublish >= interval) {
    lastPublish = millis();

    float temp = dht.readTemperature();
    int luz = analogRead(LDR_PIN);
    int nivel = analogRead(NIVEL_PIN);

    evaluarEstado(temp, nivel);
    publishAll(temp, luz, nivel);
  }
}
