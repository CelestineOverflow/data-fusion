#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ESP8266Ping.h>
#include <string>
#include <ArduinoJson.h>
//=================================================================================================
// IMU Setup
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps612.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif
// AD0 low = 0x68 (default for SparkFun breakout and InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 mpu;
// MPU6050 mpu(0x69); // <-- use for AD0 high
//=================================================================================================

const static String ssid = "Martin Router King"; // SSID
const static String password = "aezakmiQ1";      // PASSWORD

// const static String local_server_ip = "192.168.31.242";
const static IPAddress local_server = IPAddress(192, 168, 31, 242);
const static int port = 8080;
//=================================================================================================
// json data template
void sendJsonData(IPAddress serverIp, int port, Quaternion q, VectorInt16 a)
{
  StaticJsonDocument<256> doc;

  doc["id"] = "imuex";
  doc["sensorid"] = "sensor1";

  JsonArray quaternion = doc.createNestedArray("quaternion");
  quaternion.add(q.w);
  quaternion.add(q.x);
  quaternion.add(q.y);
  quaternion.add(q.z);

  JsonArray acceleration = doc.createNestedArray("acceleration");
  acceleration.add(a.x);
  acceleration.add(a.y);
  acceleration.add(a.z);
  // send the data thru UDP
  WiFiUDP udp;
  udp.beginPacket(serverIp, port);
  serializeJson(doc, udp);
  udp.endPacket();
  udp.stop();
}

// void sendPacket()
// {
//     WiFiUDP udp;
//     udp.begin(0);
//     udp.beginPacket(local_server_ip.c_str(), port);
//     udp.write('{"device_id": "01", "quaternion": [0, 0, 0, 0], "position": [0, 0, 0]}');
//     udp.endPacket();
//     udp.stop();
// }

IPAddress findServer(IPAddress local_ip)
{
  for (uint8_t i = 240; i < 255; i++)
  {
    IPAddress ip(local_ip[0], local_ip[1], local_ip[2], i);
    Serial.print("Pinging ");
    Serial.println(ip);
    if (Ping.ping(ip, 1))
    {
      Serial.print("Found possible server at ");
      Serial.println(ip);
      WiFiUDP udp;
      udp.begin(0);
      udp.beginPacket(ip, port);
      udp.write('{"device_id": "01", "quaternion": [0, 0, 0, 0], "position": [0, 0, 0]}');
      udp.endPacket();
      // check if the server is listening
      delay(1000);
      if (udp.parsePacket())
      {
        Serial.print("Server found at ");
        Serial.println(ip);
        return ip;
      }
      else
      {
        Serial.print("Server not found at ");
        Serial.println(ip);
      }
      return ip;
    }
  }
  return IPAddress(0, 0, 0, 0);
}

boolean setup_imu()
{
  Serial.println(F("Initializing DMP..."));
  uint8_t devStatus; // return status after each device operation (0 = success, !0 = error)
  devStatus = mpu.dmpInitialize();
  if (devStatus == 0)
  {
    // Calibration Time: generate offsets and calibrate our MPU6050
    mpu.CalibrateAccel(6);
    mpu.CalibrateGyro(6);
    Serial.println();
    mpu.PrintActiveOffsets();
    // turn on the DMP, now that it's ready
    Serial.println(F("Enabling DMP..."));
    mpu.setDMPEnabled(true);

    // enable Arduino interrupt detection
    Serial.print(F("Enabling interrupt detection (Arduino external interrupt "));
    
    Serial.print(digitalPinToInterrupt(INTERRUPT_PIN));
    Serial.println(F(")..."));
    attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
    mpuIntStatus = mpu.getIntStatus();

    // set our DMP Ready flag so the main loop() function knows it's okay to use it
    Serial.println(F("DMP ready! Waiting for first interrupt..."));
    dmpReady = true;

    // get expected DMP packet size for later comparison
    packetSize = mpu.dmpGetFIFOPacketSize();
  }
  else
  {
    // ERROR!
    // 1 = initial memory load failed
    // 2 = DMP configuration updates failed
    // (if it's going to break, usually the code will be 1)
    Serial.print(F("DMP Initialization failed (code "));
    Serial.print(devStatus);
    Serial.println(F(")"));
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.println("Booting");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid.c_str(), password.c_str());
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  // IPAddress server_ip = findServer(WiFi.localIP());
  sendJsonData(local_server, port, Quaternion(0, 0, 0, 0), VectorInt16(0, 0, 0));
}

uint8_t fifoBuffer[64]; // FIFO storage buffer
bool dmpReady = false;  // set true if DMP init was successful

void loop()
{
  // if programming failed, don't try to do anything
  if (!dmpReady)
    return;
  // read a packet from FIFO
  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer))
  { // Get the Latest packet
  }
}
