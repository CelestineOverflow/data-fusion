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
  initBMI160();
  WiFiManager wifiManager;
  wifiManager.autoConnect("AutoConnectAP");
  Serial.println("connected to wifi");
  Serial.println("local ip");
  Serial.println(WiFi.localIP());
  Serial.println("Initializing IMU");
  
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

        float pitch, roll, yaw;
        if (sscanf(packet.c_str(), "%f,%f,%f", &pitch, &roll, &yaw) == 3) {
            setOrientation(pitch, roll, yaw);
            Serial.println("Orientation Set: Pitch=" + String(pitch) + ", Roll=" + String(roll) + ", Yaw=" + String(yaw));
        } else {
            Serial.println("Error: Invalid data format");
        }
    }
}



