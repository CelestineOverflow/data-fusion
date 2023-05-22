#include <ESP8266WiFi.h>
#include <Arduino.h>
#include <String.h>
#include <WiFiUdp.h>

IPAddress server(192, 168, 31, 242);
const uint16_t port = 1337;
// WiFiClient client;
static String ssid = "Martin Router King";
static String password = "aezakmiQ1";

// int wait_for_new_credentials()
// {
//     Serial.println("Waiting for new credentials");
//     //get new credentials from serial input
//     Serial.println("Enter SSID:");
//     while (Serial.available() == 0)
//     {
//         delay(500);
//     }
//     ssid = Serial.readString();
//     Serial.println("Enter password:");
//     while (Serial.available() == 0)
//     {
//         delay(500);
//     }
//     password = Serial.readString();
//     Serial.println("New credentials:");
//     Serial.println(ssid);
//     Serial.println(password);
//     return 0;
// }

int init_wifi()
{
    long unsigned int timeout = millis() + 10000;
    Serial.println("Connecting to WiFi");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        if (millis() > timeout)
        {
            Serial.println("Timeout");
            // wait_for_new_credentials();
        }
    }
    Serial.println("");
    Serial.print("WiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    return 0;
}


int send_data(String data)
{
    WiFiUDP udp;
    udp.beginPacket(server, port);
    udp.print(data);
    udp.endPacket();
    return 0;
}
