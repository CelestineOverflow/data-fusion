#include <DFRobot_BMI160.h>
#include <Arduino.h>

static DFRobot_BMI160 bmi160;
static const int8_t i2c_addr = 0x68;


static int16_t offset_bmi160[6] = {0, 0, 0, 0, 0, 0};

static void calibrate_bmi(int16_t *accelGyro)
{
#define CALIBRATE_COUNT 100

  for (int i = 0; i < CALIBRATE_COUNT; i++)
  {
    int16_t temp[6] = {0, 0, 0, 0, 0, 0};
    int rslt = bmi160.getAccelGyroData(temp);
    if (rslt != 0)
    {
      Serial.println("err");
      return;
    }
    for (int i = 0; i < 6; i++)
    {

      offset_bmi160[i] += temp[i];
    }
  }
  for (int i = 0; i < 6; i++)
  {
    offset_bmi160[i] /= CALIBRATE_COUNT;
  }
}

void init_bmi160()
{
  Serial.println("init bmi160");
  // init the hardware bmin160
  if (bmi160.softReset() != BMI160_OK)
  {
    Serial.println("reset false");
    while (1)
      ;
  }

  // set and init the bmi160 i2c address
  if (bmi160.I2cInit(i2c_addr) != BMI160_OK)
  {
    Serial.println("init false");
    while (1)
      ;
  }
  calibrate_bmi(offset_bmi160);
  Serial.println("init bmi160 done");
}

void print_bmi160()
{
  int i = 0;
  int rslt;
  int16_t accelGyro[6] = {0};

  // get both accel and gyro data from bmi160
  // parameter accelGyro is the pointer to store the data
  rslt = bmi160.getAccelGyroData(accelGyro);
  if (rslt == 0)
  {
    for (i = 0; i < 6; i++)
    {
      if (i < 3)
      {
        // the first three are gyro data
        Serial.print(accelGyro[i] * 3.14 / 180.0);
        Serial.print("\t");
      }
      else
      {
        // the following three data are accel data
        Serial.print(accelGyro[i] / 16384.0);
        Serial.print("\t");
      }
    }
    Serial.println();
  }
  else
  {
    Serial.println("err");
  }
}

float delta_t = 0.0;

// send data to function pointer
//  structure
//  "id" : 0,
//  "accelerometer": {
//      "x": 0,
//      "y": 0,
//      "z": 0
//  },
//  "gyroscope": {
//      "x": 0,
//      "y": 0,
//      "z": 0
//  }
void send_bmi_data(int (*send_data)(String))
{
  int i = 0;
  int rslt;
  int16_t accelGyro[6] = {0};
  rslt = bmi160.getAccelGyroData(accelGyro);
  if (rslt == 0)
  {
    String data = "{";
    data += "\"id\": 0,";
    data += "\"accelerometer\": {";
    data += "\"x\": " + String(accelGyro[3] / 16384.0) + ",";
    data += "\"y\": " + String(accelGyro[4] / 16384.0) + ",";
    data += "\"z\": " + String(accelGyro[5] / 16384.0);
    data += "},";
    data += "\"gyroscope\": {";
    data += "\"x\": " + String(accelGyro[0]) + ",";
    data += "\"y\": " + String(accelGyro[1]) + ",";
    data += "\"z\": " + String(accelGyro[2]);
    data += "}";
    data += "}";
    send_data(data);
  }
  else
  {
    Serial.println("err");
  }
}

