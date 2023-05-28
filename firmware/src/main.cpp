#include <Arduino.h>
#include "aheader.h"
#include "network.h"
#include "leds.h"
#include "bmiutils.h"
void setup()
{
  Serial.begin(115200);
  init_wifi();
  init_bmi160();
  selftestsweepthruleds();
  Serial.println("sending data");
}

void loop()
{
  // print_bmi160();
  send_bmi_data(send_data);
  // delay(1000);
}
