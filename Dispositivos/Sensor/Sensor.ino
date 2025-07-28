#include <WiFi.h>
#include <PubSubClient.h>

// ====== CONFIGURAÇÕES Wi-Fi ======
const char* ssid = "NOME_DA_SUA_REDE";
const char* password = "SUA_SENHA";

// ====== CONFIGURAÇÕES MQTT ======
const char* mqttServer = "test.mosquitto.org";
const int mqttPort = 1883;
const char* mqttClientId = "esp32Client123";

// Criando objetos WiFi e MQTT
WiFiClient espClient;
PubSubClient client(espClient);

void setupWiFi() {
  delay(10);
  Serial.println("Conectando-se ao WiFi...");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado com sucesso.");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT...");
    if (client.connect(mqttClientId)) {
      Serial.println("Conectado!");
    } else {
      Serial.print("Erro, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5 segundos...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setupWiFi();

  client.setServer(mqttServer, mqttPort);
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();

  // Publica a mensagem no tópico
  String mensagem = "Olá, mundo!";
  client.publish("teste/mundo", mensagem.c_str());
  Serial.println("Mensagem publicada: " + mensagem);

  // Aguarda 10 segundos antes de enviar novamente
  delay(10000);
}
