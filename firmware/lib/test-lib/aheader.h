#include <Arduino.h>

void test()
{
    Serial.print("test lib");
    for (int i = 0; i < 10; i++)
    {
        Serial.print("___");
        Serial.print(i);
        delay(1000);
    }
    Serial.println("___");
}