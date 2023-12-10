
#include "BMI160.h"
#include "madgwick.h"
#include <Arduino.h>

#define SEND_AS_DEGREES 1                // Set to 0 to send data as radian
#define DEG_TO_RAD 0.017453292519943295  // PI / 180
#define RAD_TO_DEG 57.295779513082320876 // 180 / PI
#define TO_RAD(deg) ((deg) * DEG_TO_RAD) // Convert degrees to radians

// Define transformation macros as per your requirement
// #define TRANSFORM_PITCH(pitch) (-TO_RAD(pitch) - PI / 2)
// #define TRANSFORM_ROLL(roll) (TO_RAD(yaw)) // Assuming yaw is to be used for roll
// #define TRANSFORM_YAW(yaw) (TO_RAD(roll)) // Assuming roll is to be used for yaw
#if SEND_AS_DEGREES
static const float gyroScaleFactor = 65.5; // Scale factor for gyro (±500 degrees/s)
static const String unit = "rad";
#else
static const float gyroScaleFactor = 1.14591559; // Scale factor for gyro (convert to radians)
static const String unit = "rad";
#endif

BMI160 bmi160;
static const int8_t i2c_addr = 0x68;
static int16_t offset_bmi160[6] = {0, 0, 0, 0, 0, 0};

Madgwick<float> madgwickFilter;
bool externalQuaternionSet = false;

// Quaternion to hold the orientation
float quaternion[4] = {1.0f, 0.0f, 0.0f, 0.0f};

void calibrateBMI()
{
#define CALIBRATE_COUNT 100
    int16_t ax, ay, az, gx, gy, gz;
    int16_t ax_offset = 0, ay_offset = 0, az_offset = 0, gx_offset = 0, gy_offset = 0, gz_offset = 0;

    for (int i = 0; i < CALIBRATE_COUNT; ++i)
    {
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

void initBMI160()
{
    Serial.println("Initializing BMI160");
    Wire.begin();
    Wire.setClock(400000);
    Wire.beginTransmission(i2c_addr);
    if (Wire.endTransmission() == 0)
    {
        Serial.println("BMI160 found");
    }
    else
    {
        Serial.println("BMI160 not found. Check connections.");
        while (1)
            ;
    }

    bmi160.initialize(i2c_addr, BMI160_GYRO_RATE_800HZ, BMI160_GYRO_RANGE_500, BMI160_DLPF_MODE_NORM, BMI160_ACCEL_RATE_800HZ, BMI160_ACCEL_RANGE_4G, BMI160_DLPF_MODE_OSR4);
    calibrateBMI();
    Serial.println("BMI160 initialized");
}

float gyroX = 0.0, gyroY = 0.0, gyroZ = 0.0;
long lastTime = 0;

void integrateGyroData()
{
    int16_t ax, ay, az, gx, gy, gz;
    bmi160.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    gx -= offset_bmi160[3];
    gy -= offset_bmi160[4];
    gz -= offset_bmi160[5];

    // remap axes
    //  Flipping axes
#ifdef FLIP_X
    gx = -gx;
    ax = -ax;
#endif
#ifdef FLIP_Y
    gy = -gy;
    ay = -ay;
#endif
#ifdef FLIP_Z
    gz = -gz;
    az = -az;
#endif

    // Swapping axes
    int16_t temp;
#ifdef SWAP_XY
    temp = gx;
    gx = gy;
    gy = temp;
    temp = ax;
    ax = ay;
    ay = temp;
#endif
#ifdef SWAP_YZ
    temp = gy;
    gy = gz;
    gz = temp;
    temp = ay;
    ay = az;
    az = temp;
#endif
#ifdef SWAP_XZ
    temp = gx;
    gx = gz;
    gz = temp;
    temp = ax;
    ax = az;
    az = temp;
#endif

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

void IntegrateDataMadgwick()
{
    long currentTime = micros();
    float dt = (currentTime - lastTime) / 1000000.0f; // Convert microseconds to seconds
    lastTime = currentTime;

    int16_t ax, ay, az, gx, gy, gz;
    bmi160.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    if (!externalQuaternionSet)
    {
        // Apply offsets only if the quaternion has not been externally set
        ax -= offset_bmi160[0];
        ay -= offset_bmi160[1];
        az -= offset_bmi160[2];
        gx -= offset_bmi160[3];
        gy -= offset_bmi160[4];
        gz -= offset_bmi160[5];
    }
    else
    {
        // Reset the flag after using the external quaternion for the first time
        externalQuaternionSet = false;
    }


    // remap axes
    //  Flipping axes


#ifdef FLIP_X
    gx = -gx;
    ax = -ax;
#endif
#ifdef FLIP_Y
    gy = -gy;
    ay = -ay;
#endif
#ifdef FLIP_Z
    gz = -gz;
    az = -az;
#endif
    int16_t temp = 0;

// Swap axes if needed
#ifdef SWAP_XY
    temp = gx;
    gx = gy;
    gy = temp;
    temp = ax;
    ax = ay;
    ay = temp;
#endif
#ifdef SWAP_YZ
    temp = gy;
    gy = gz;
    gz = temp;
    temp = ay;
    ay = az;
    az = temp;
#endif
#ifdef SWAP_XZ
    temp = gx;
    gx = gz;
    gz = temp;
    temp = ax;
    ax = az;
    az = temp;
#endif

    // Convert gyroscope data to rad/s
    float gyroRadX = gx / gyroScaleFactor * DEG_TO_RAD;
    float gyroRadY = gy / gyroScaleFactor * DEG_TO_RAD;
    float gyroRadZ = gz / gyroScaleFactor * DEG_TO_RAD;

    // Update the Madgwick filter
    madgwickFilter.update(quaternion, ax, ay, az, gyroRadX, gyroRadY, gyroRadZ, dt);
}

// void sendBMIData(int (*sendData)(String)) {
//     integrateGyroData();
//     String data = "{\"id\": 0, \"orientation\": {";
//     data += "\"pitch\": " + String(gyroX) + ", ";
//     data += "\"roll\": " + String(gyroY) + ", ";
//     data += "\"yaw\": " + String(gyroZ) + ", ";
//     data += "\"unit\": \"" + unit + "\"";
//     data += "}}";
//     sendData(data);
//     // printBMI160();
// }

float quaternion_offset[4] = {1.0f, 0.0f, 0.0f, 0.0f}; // Quaternion offset to be applied to the IMU's quaternion

void multiplyQuaternions(const float q1[4], const float q2[4], float result[4])
{
    result[0] = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]; // w
    result[1] = q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2]; // x
    result[2] = q1[0] * q2[2] - q1[1] * q2[3] + q1[2] * q2[0] + q1[3] * q2[1]; // y
    result[3] = q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1] + q1[3] * q2[0]; // z
}

void setOrientationOffset(float w, float x, float y, float z)
{
    quaternion_offset[0] = w;
    quaternion_offset[1] = x;
    quaternion_offset[2] = y;
    quaternion_offset[3] = z;
}
void sendBMIData(int (*sendData)(String))
{
    IntegrateDataMadgwick(); // Update orientation using Madgwick filter

    float combinedQuaternion[4];
    multiplyQuaternions(quaternion, quaternion_offset, combinedQuaternion);

    // Convert combined quaternion to Euler angles (pitch, roll, yaw)
    float pitch = atan2(2.0f * (combinedQuaternion[0] * combinedQuaternion[1] + combinedQuaternion[2] * combinedQuaternion[3]), 1.0f - 2.0f * (combinedQuaternion[1] * combinedQuaternion[1] + combinedQuaternion[2] * combinedQuaternion[2]));
    float roll = asin(2.0f * (combinedQuaternion[0] * combinedQuaternion[2] - combinedQuaternion[3] * combinedQuaternion[1]));
    float yaw = atan2(2.0f * (combinedQuaternion[0] * combinedQuaternion[3] + combinedQuaternion[1] * combinedQuaternion[2]), 1.0f - 2.0f * (combinedQuaternion[2] * combinedQuaternion[2] + combinedQuaternion[3] * combinedQuaternion[3]));

    // Prepare data string
    String data = "{\"id\": 0, \"orientation\": {";
    data += "\"pitch\": " + String(pitch) + ", ";
    data += "\"roll\": " + String(roll) + ", ";
    data += "\"yaw\": " + String(yaw) + ", ";
    data += "\"unit\": \"" + unit + "\"";

    data += "}, \"quaternion\": {";
    data += "\"w\": " + String(combinedQuaternion[0]) + ", ";
    data += "\"x\": " + String(combinedQuaternion[1]) + ", ";
    data += "\"y\": " + String(combinedQuaternion[2]) + ", ";
    data += "\"z\": " + String(combinedQuaternion[3]);
    data += "}}";
    sendData(data);
    // Serial.println(data);
}
