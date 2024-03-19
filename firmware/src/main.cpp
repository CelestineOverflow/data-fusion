#include <Arduino.h>
#include "network.h"
#include "leds.h"
#include "bmiutils.h"

#include <WiFiUdp.h>
WiFiUDP Udp;
unsigned int localUdpPort = 4210; // local port to listen on
#include <ESP8266WiFi.h>          
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>         


void setup()
{
  Serial.begin(115200);
  // WiFiManager wifiManager;
  // wifiManager.autoConnect("AutoConnectAP");
  //wifi pass 97106678
  WiFi.begin("Martin Router King", "aezakmiQ1");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("connected to wifi");
  Serial.println("local ip");
  Serial.println(WiFi.localIP());
  Serial.println("MAC address");
  setMacAddress(WiFi.macAddress());
  Serial.println("Initializing IMU");
  initBMI160();
  Serial.println("Initializing UDP");
  find_udp_server();
  Serial.println("Initializing OTA");
  Serial.println("Initializing UDP");
  Udp.begin(localUdpPort);
  Serial.println("UDP Server started on port: " + String(localUdpPort));
}

void loop()
{
  ArduinoOTA.handle();
  sendBMIData(send_data);
  int packetSize = Udp.parsePacket();
  if (packetSize) {
        char packetBuffer[255];
        Udp.read(packetBuffer, 255);
        String packet = String(packetBuffer);

        float w, x, y, z;
        if (sscanf(packet.c_str(), "%f,%f,%f,%f", &w, &x, &y, &z) == 4) {
            setOrientationOffset(w, x, y, z);
            Serial.println("Orientation Set: q=" + String(w) + "," + String(x) + "," + String(y) + "," + String(z));
        } else {
            Serial.println("Error: Invalid data format");
        }
    }
}



