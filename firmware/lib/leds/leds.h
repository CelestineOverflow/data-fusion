#include <Arduino.h>

#define LED_1 D5
#define LED_2 D6
#define LED_3 D7

//create a cpp class to handle the leds

void selftestsweepthruleds(){
    pinMode(LED_1, OUTPUT);
    pinMode(LED_2, OUTPUT);
    pinMode(LED_3, OUTPUT);
    for (int i = 0; i < 10; i++)
    {
        digitalWrite(LED_1, HIGH);
        delay(100);
        digitalWrite(LED_1, LOW);
        digitalWrite(LED_2, HIGH);
        delay(100);
        digitalWrite(LED_2, LOW);
        digitalWrite(LED_3, HIGH);
        delay(100);
        digitalWrite(LED_3, LOW);
    }
}