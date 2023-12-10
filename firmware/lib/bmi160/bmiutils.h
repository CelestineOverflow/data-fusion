
#include "BMI160.h"
#include <Arduino.h>

#define SEND_AS_DEGREES 1  // Set to 0 to send data as radians

#if SEND_AS_DEGREES
static const float gyroScaleFactor = 65.5; // Scale factor for gyro (±500 degrees/s)
static const String unit = "deg";
#else
static const float gyroScaleFactor = 1.14591559; // Scale factor for gyro (convert to radians)
static const String unit = "rad";
#endif

BMI160 bmi160;
static const int8_t i2c_addr = 0x68;
static int16_t offset_bmi160[6] = {0, 0, 0, 0, 0, 0};

void calibrateBMI() {
    #define CALIBRATE_COUNT 100
    int16_t ax, ay, az, gx, gy, gz;
    int16_t ax_offset = 0, ay_offset = 0, az_offset = 0, gx_offset = 0, gy_offset = 0, gz_offset = 0;

    for (int i = 0; i < CALIBRATE_COUNT; ++i) {
        bmi160.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
        ax_offset += ax;
        ay_offset += ay;
        az_offset += az;
        gx_offset += gx;
        gy_offset += gy;
        gz_offset += gz;
        delay(10);
    }

    offset_bmi160[0] = ax_offset / CALIBRATE_COUNT;
    offset_bmi160[1] = ay_offset / CALIBRATE_COUNT;
    offset_bmi160[2] = az_offset / CALIBRATE_COUNT;
    offset_bmi160[3] = gx_offset / CALIBRATE_COUNT;
    offset_bmi160[4] = gy_offset / CALIBRATE_COUNT;
    offset_bmi160[5] = gz_offset / CALIBRATE_COUNT;
}

void initBMI160() {
    Serial.println("Initializing BMI160");
    Wire.begin();
    Wire.setClock(400000); 
    Wire.beginTransmission(i2c_addr);
    if (Wire.endTransmission() == 0) {
        Serial.println("BMI160 found");
    } else {
        Serial.println("BMI160 not found. Check connections.");
        while (1);
    }

    bmi160.initialize(i2c_addr, BMI160_GYRO_RATE_800HZ, BMI160_GYRO_RANGE_500, BMI160_DLPF_MODE_NORM, BMI160_ACCEL_RATE_800HZ, BMI160_ACCEL_RANGE_4G, BMI160_DLPF_MODE_OSR4);
    calibrateBMI();
    Serial.println("BMI160 initialized");
}

float gyroX = 0.0, gyroY = 0.0, gyroZ = 0.0;
long lastTime = 0;

void integrateGyroData() {
    int16_t ax, ay, az, gx, gy, gz;
    bmi160.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    gx -= offset_bmi160[3];
    gy -= offset_bmi160[4];
    gz -= offset_bmi160[5];

    long currentTime = micros();
    float dt = (currentTime - lastTime) / 1000000.0;
    lastTime = currentTime;

    float gyroRateX = gx / gyroScaleFactor;
    float gyroRateY = gy / gyroScaleFactor;
    float gyroRateZ = gz / gyroScaleFactor;

    gyroX -= gyroRateX * dt;
    gyroY += gyroRateY * dt;
    gyroZ += gyroRateZ * dt;
}

void printBMI160() {
    Serial.print("gyroX = "); Serial.print(gyroX);
    Serial.print(" gyroY = "); Serial.print(gyroY);
    Serial.print(" gyroZ = "); Serial.println(gyroZ);
}

void sendBMIData(int (*sendData)(String)) {
    integrateGyroData();
    String data = "{\"id\": 0, \"orientation\": {";
    data += "\"pitch\": " + String(gyroX) + ", ";
    data += "\"roll\": " + String(gyroY) + ", ";
    data += "\"yaw\": " + String(gyroZ) + ", ";
    data += "\"unit\": \"" + unit + "\"";
    data += "}}";
    sendData(data);
    // printBMI160();
}

void setOrientation(float pitch, float roll, float yaw) {
    gyroX = pitch;
    gyroY = roll;
    gyroZ = yaw;
}