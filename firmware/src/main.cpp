#include <Arduino.h>
#include "network.h"
#include "leds.h"
#include "bmiutils.h"

#include <ESP8266WiFi.h>          
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>         


void setup()
{
  Serial.begin(115200);
  WiFiManager wifiManager;
  wifiManager.autoConnect("AutoConnectAP");
  Serial.println("connected to wifi");
  Serial.println("local ip");
  Serial.println(WiFi.localIP());
  Serial.println("Initializing IMU");
  init_bmi160();
  Serial.println("Initializing UDP");
  // find_udp_server();
  Serial.println("Initializing OTA");
}

void loop()
{
  // ArduinoOTA.handle();
  // print_bmi160();
  send_bmi_data(send_data);
}



