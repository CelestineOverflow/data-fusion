#include <Adafruit_CCS811.h>



Adafruit_CCS811 ccs;
void setup() {
  Serial.begin(9600);

  Serial.println("CCS811 test");

  if(!ccs.begin()){
    Serial.println("Failed to start sensor! Please check your wiring.");
    while(1);
  }

  while(!ccs.available());
  float temp = ccs.calculateTemperature();
  ccs.setTempOffset(temp - 25.0);
}

void loop() {
  if(ccs.available()){
    if(!ccs.readData()){
      Serial.print(ccs.geteCO2());
      Serial.print(",");
      Serial.print(ccs.getTVOC());
      Serial.print(",");
      Serial.println(ccs.calculateTemperature());
    }
    else{
      Serial.println("ERROR!");
      while(1);
    }
  }
}