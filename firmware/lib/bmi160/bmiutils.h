
#include "BMI160.h"
#include "madgwick.h"
#include <Arduino.h>

#define SEND_AS_DEGREES 1                // Set to 0 to send data as radian
#define DEG_TO_RAD 0.017453292519943295  // PI / 180
#define RAD_TO_DEG 57.295779513082320876 // 180 / PI
#define TO_RAD(deg) ((deg) * DEG_TO_RAD) // Convert degrees to radians

// #define x_axis_flip
// #define y_axis_flip

#ifdef x_axis_flip
#define FLIP_X(x) (-(x))
#else
#define FLIP_X(x) (x)
#endif

#ifdef y_axis_flip
#define FLIP_Y(y) (-(y))
#else
#define FLIP_Y(y) (y)
#endif

#ifdef z_axis_flip
#define FLIP_Z(z) (-(z))
#else
#define FLIP_Z(z) (z)
#endif

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
float quaternion[4] = {1.0f, 0.0f, 0.0f, 0.0f}; // w, x, y, z

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
    long currentTime = micros();
    float dt = (currentTime - lastTime) / 1000000.0;
    lastTime = currentTime;

    float gyroRateX = FLIP_X(gx) / gyroScaleFactor;
    float gyroRateY = FLIP_Y(gy) / gyroScaleFactor;
    float gyroRateZ = FLIP_Z(gz) / gyroScaleFactor;

    gyroX -= gyroRateX * dt;
    gyroY += gyroRateY * dt;
    gyroZ += gyroRateZ * dt;
}

float valueSwitch = 1.0f;
float targetQuaternion[4] = {1.0f, 0.0f, 0.0f, 0.0f};

void IntegrateDataMadgwick()
{
    long currentTime = micros();
    float dt = (currentTime - lastTime) / 1000000.0f; // Convert microseconds to seconds
    lastTime = currentTime;

    int16_t ax, ay, az, gx, gy, gz;
    // X and Y axes are swapped in both accelerometer and gyroscope data
    bmi160.getMotion6(&ay, &ax, &az, &gy, &gx, &gz);
    //ay ax az
    ax = FLIP_X(ax);
    ay = FLIP_Y(ay);
    az = FLIP_Z(az);
    // Serial.print("ax: ");
    // Serial.print(ax);
    // Serial.print(" ay: ");
    // Serial.print(ay);
    // Serial.print(" az: ");
    // Serial.println(az);
    // Convert gyroscope data to rad/s
    float gyroRadX = FLIP_X(gx) / gyroScaleFactor * DEG_TO_RAD;
    float gyroRadY = FLIP_Y(gy) / gyroScaleFactor * DEG_TO_RAD;
    float gyroRadZ = FLIP_Z(gz) / gyroScaleFactor * DEG_TO_RAD;

    // Update the Madgwick filter
    madgwickFilter.update(quaternion, ax, ay, az, gyroRadX, gyroRadY, gyroRadZ, dt);
    // Update the target quaternion if external quaternion is set
    if (valueSwitch < 1.0f)
    {
        valueSwitch += 0.001f;
        madgwickFilter.update(targetQuaternion, ax, ay, az, gyroRadX, gyroRadY, gyroRadZ, dt);
        for (int i = 0; i < 4; i++)
        {
            quaternion[i] = (1 - valueSwitch) * quaternion[i] + valueSwitch * targetQuaternion[i];
        }
    }
}

void IntegrateDataGyroOnly()
{
    long currentTime = micros();
    float dt = (currentTime - lastTime) / 1000000.0f; // Convert microseconds to seconds
    lastTime = currentTime;

    int16_t ax, ay, az, gx, gy, gz;
    // X and Y axes are swapped in both accelerometer and gyroscope data
    bmi160.getMotion6(&ay, &ax, &az, &gy, &gx, &gz);
    //ay ax az
    ax = FLIP_X(ax);
    ay = FLIP_Y(ay);
    az = FLIP_Z(az);
    // Serial.print("ax: ");
    // Serial.print(ax);
    // Serial.print(" ay: ");
    // Serial.print(ay);
    // Serial.print(" az: ");
    // Serial.println(az);
    // Convert gyroscope data to rad/s
    float gyroRadX = FLIP_X(gx) / gyroScaleFactor * DEG_TO_RAD;
    float gyroRadY = FLIP_Y(gy) / gyroScaleFactor * DEG_TO_RAD;
    float gyroRadZ = FLIP_Z(gz) / gyroScaleFactor * DEG_TO_RAD;


    // Rate of change of quaternion from gyroscope
    float qDot1 = 0.5f * (-quaternion[1] * gyroRadX - quaternion[2] * gyroRadY - quaternion[3] * gyroRadZ);
    float qDot2 = 0.5f * (quaternion[0] * gyroRadX + quaternion[2] * gyroRadZ - quaternion[3] * gyroRadY);
    float qDot3 = 0.5f * (quaternion[0] * gyroRadY - quaternion[1] * gyroRadZ + quaternion[3] * gyroRadX);
    float qDot4 = 0.5f * (quaternion[0] * gyroRadZ + quaternion[1] * gyroRadY - quaternion[2] * gyroRadX);

    // Integrate to yield quaternion
    quaternion[0] += qDot1 * dt;
    quaternion[1] += qDot2 * dt;
    quaternion[2] += qDot3 * dt;
    quaternion[3] += qDot4 * dt;

    // Normalize the quaternion
    float recipNorm = invSqrt(quaternion[0] * quaternion[0] + quaternion[1] * quaternion[1] + quaternion[2] * quaternion[2] + quaternion[3] * quaternion[3]);
    quaternion[0] *= recipNorm;
    quaternion[1] *= recipNorm;
    quaternion[2] *= recipNorm;
    quaternion[3] *= recipNorm;
}


void multiplyQuaternions(const float q1[4], const float q2[4], float result[4])
{
    result[0] = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]; // w
    result[1] = q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2]; // x
    result[2] = q1[0] * q2[2] - q1[1] * q2[3] + q1[2] * q2[0] + q1[3] * q2[1]; // y
    result[3] = q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1] + q1[3] * q2[0]; // z
}
void eulerToQuaternion(float yaw, float pitch, float roll, float *q)
{
    float cy = cos(yaw * 0.5);
    float sy = sin(yaw * 0.5);
    float cp = cos(pitch * 0.5);
    float sp = sin(pitch * 0.5);
    float cr = cos(roll * 0.5);
    float sr = sin(roll * 0.5);

    q[0] = cr * cp * cy + sr * sp * sy; // W
    q[1] = sr * cp * cy - cr * sp * sy; // X
    q[2] = cr * sp * cy + sr * cp * sy; // Y
    q[3] = cr * cp * sy - sr * sp * cy; // Z
}



static float InverseoffsetXQuaternionInverse[4] = {0.70710678118, -0.70710678118, 0, 0};
void setOrientationOffset(float w, float x, float y, float z)
{
    targetQuaternion[0] = w;
    targetQuaternion[1] = x;
    targetQuaternion[2] = y;
    targetQuaternion[3] = z;
    valueSwitch = 0.0f;
}


String macAddress;

void setMacAddress(String mac)
{
    macAddress = mac;
    macAddress.replace(":", "");
}




#include <ArduinoJson.h>

static float offsetXQuaternion[4] = {1, 0, 0, 0}; // order is w, x, y, z

void sendBMIData(int (*sendData)(String))
{
    IntegrateDataMadgwick(); // Update orientation using Madgwick filter
    //IntegrateDataGyroOnly(); // Update orientation using only gyroscope data
    
     StaticJsonDocument<256> doc; // Adjust size as needed
    JsonObject imu = doc.createNestedObject("imu");
    JsonObject macObject = imu.createNestedObject(macAddress.c_str());
    JsonObject quaternionObject = macObject.createNestedObject("quaternion");
    // Your current orientation quaternion (assuming quaternion is globally defined or accessible)
    // float quaternion[4] = {w, x, y, z};
    // Quaternion to store the result after applying the offset
    float resultQuaternion[4];

    // Apply the offset
    multiplyQuaternions(offsetXQuaternion, quaternion, resultQuaternion);
    quaternionObject["x"] = resultQuaternion[1];
    quaternionObject["y"] = resultQuaternion[2];
    quaternionObject["z"] = resultQuaternion[3];
    quaternionObject["w"] = resultQuaternion[0];

    String output;
    serializeJson(doc, output);
    sendData(output);


}
