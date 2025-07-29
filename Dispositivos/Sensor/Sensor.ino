#include <WiFi.h>
#include <PubSubClient.h>
#include <ESPmDNS.h>
#include <WiFiManager.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <TimeLib.h>
#include <string>

// Defina o fuso horário do Brasil (UTC-3, ou seja, -10800 segundos)
const long utcOffsetSeconds = -10800;

// Configuração do UDP para o NTP
WiFiUDP udp;
NTPClient timeClient(udp, "pool.ntp.org", utcOffsetSeconds, 60000);

int horaInicio, minutoInicio, segundoInicio;
int currentHour;
int currentMinute;
int currentSecond;
int currentDay;
int currentMonth;
int currentYear;

// MQTT Connection set 

#define MQTT_ID "brennoaaa_teste"
#define MQTT_BROKER "broker.hivemq.com"
#define MQTT_PORT 1883
#define MQTT_TOPIC_PUB "esp32/pub"
#define MQTT_TOPIC_SUB "esp32/sub"

// Define net client
WiFiClient espClient; 

// Define mqtt client
PubSubClient MQTT(espClient);

String nomePaciente = "jorge júnior";
String cpf = "12345678910";
String medico = "CRM123456";
/*
{
"paciente": nome do paciente,
"cpf": cpf,
"medico": crm
"hora": hora,
"dadoBiometricoX": dado biometrico x,
"dadoBiometricoY": dado biometrico y,
"dadoBiometricoZ": dado biometrico Z,
}
*/
void setupWIFI(){
  WiFiManager wm;
  bool res;

  res = wm.autoConnect("Esp-Brenno","BrennoAndrade"); // password protected ap

  if(!res) {
      Serial.println("Failed to connect");
  } 
  else {
      //if you get here you have connected to the WiFi    
      Serial.println("connected...yeey :)");
  }
}

void setupMQTT(){
    // Config MQTT Broker connection

    MQTT.setServer(MQTT_BROKER, MQTT_PORT);
    MQTT.setCallback(mqtt_callback); 

    // Conn exec

    while (!MQTT.connected()){
        Serial.print("- MQTT Setup: Tentando se conectar ao Broker MQTT: ");
        Serial.println(MQTT_BROKER);

        if(MQTT.connect(MQTT_ID)){
            Serial.println("- MQTT Setup: Conectado com sucesso");
             MQTT.subscribe(MQTT_TOPIC_SUB);
        } else {
            Serial.println("- MQTT Setup: Falha ao se conectar, tentando novamente em 2s");
            delay(2000);
        }
    }
}

void setup(void){
    // Set baudrate of serial com
    Serial.begin(115200);
    // Pinmode
    pinMode(LED_BUILTIN, OUTPUT);
    // Call setup wifi
    setupWIFI();
    // Call setup mqtt
    setupMQTT();
    // Call setup ota
}

void loop(void){

    if (!MQTT.connected()) {
        setupMQTT(); // reconecta apenas se necessário
    }
    MQTT.loop();
    delay(1000);
}

void atualizarHora(int &currentHour, int &currentMinute, int &currentSecond, int &currentDay, int &currentMonth, int &currentYear) {
  // Atualiza a hora
  timeClient.update();

  // Obtém o tempo em segundos desde a epoch
  unsigned long epochTime = timeClient.getEpochTime();

  // Converte o tempo epoch para uma data legível
  setTime(epochTime);

  // Obtém a data e hora separadas usando a biblioteca TimeLib
  currentHour = hour();
  currentMinute = minute();
  currentSecond = second();
  currentDay = day();
  currentMonth = month();
  currentYear = year();

  // Exibe as informações na Serial Monitor
  Serial.print("Data: ");
  Serial.print(currentDay);
  Serial.print("/");
  Serial.print(currentMonth);
  Serial.print("/");
  Serial.print(currentYear);
  Serial.print(" Hora: ");
  Serial.print(currentHour);
  Serial.print(":");
  Serial.print(currentMinute);
  Serial.print(":");
  Serial.println(currentSecond);
}


// Callback function
// Called when data is received in one of topics
void mqtt_callback(char* topic, byte* payload, unsigned int length)
{
  String message;
  Serial.print("- MQTT Callback Topic: ");
  Serial.println(topic);

  for (int i = 0; i < length; i++)
  {
    char c = (char)payload[i];
    message += c;
  }

  String direction;
  int distance = 1000;

  int spaceIndex = message.indexOf(' ');
  if (spaceIndex != -1) {
    direction = message.substring(0, spaceIndex);
    distance = message.substring(spaceIndex + 1).toInt();
  } else {
    direction = message;
  }

  Serial.println(direction);

  if (direction.equals("dados")) {
    float temperatura = random(360, 400) / 10.0;  // Ex: 36.0°C a 40.0°C
    float oximetria = random(80, 100);            // Ex: 950 hPa a 1050 hPa
    atualizarHora(currentHour, currentMinute, currentSecond, currentDay, currentMonth, currentYear);

    String horaFormatada = String(currentYear) + "/" + String(currentMonth) + "/" + String(currentDay) + "/" +
                           String(currentHour) + "h" + String(currentMinute) + "m" + String(currentSecond) + "s";

    String path = "{\"acao\":\"ret_dados\",\"paciente\":\"" + nomePaciente + "\",\"cpf\":\"" + cpf + "\",\"medico\":\""+ medico + "\",\"hora\":\"" + 
                    horaFormatada + "\",\"Temperatura\":\"" + temperatura +"\",\"Oximetria\":\"" + oximetria + "\"}";

    Serial.println(path);
    MQTT.publish(MQTT_TOPIC_PUB, path.c_str());
  }
}


