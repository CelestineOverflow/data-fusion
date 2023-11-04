#include <Arduino.h>
#include "network.h"
#include "leds.h"
#include "bmiutils.h"





void setup()
{
  Serial.begin(115200);
  init_wifi();
  init_bmi160();
  find_udp_server();
}

void loop()
{
  // print_bmi160();
  ArduinoOTA.handle();
  send_bmi_data(send_data);
}


