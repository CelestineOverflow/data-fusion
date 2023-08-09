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



#define SEND_AS_DEGREES 1

static float roll = 0.0;
static float pitch = 0.0;
static float yaw = 0.0;
static float roll_cal = 0.0;
static float pitch_cal = 0.0;
static float yaw_cal = 0.0;
static long last_time = 0;
#if SEND_AS_DEGREES
static String unit = "deg/s";
#else
static String unit = "rad/s";
#endif

static void integrate_data()
{
  int rslt;
  int16_t accelGyro[6] = {0};
  float dt;
  long current_time = millis();
  if (last_time == 0)
  {
    dt = 0.01; // initial guess
  }
  else
  {
    dt = (current_time - last_time) / 10000.0; // convert to seconds
  }

  rslt = bmi160.getAccelGyroData(accelGyro);
  if (rslt == 0)
  {
    float gyro_rate_x = accelGyro[0] * 3.14 / 180.0; // Convert to rad/s
    float gyro_rate_y = accelGyro[1] * 3.14 / 180.0;
    float gyro_rate_z = accelGyro[2] * 3.14 / 180.0;

    float accel_x = accelGyro[3] / 16384.0;
    float accel_y = accelGyro[4] / 16384.0;
    float accel_z = accelGyro[5] / 16384.0;

    float accel_pitch = atan2(accel_y, sqrt(accel_x * accel_x + accel_z * accel_z));
    float accel_roll = atan2(-accel_x, accel_z);

    pitch = 0.98 * (pitch + gyro_rate_x * dt) + 0.02 * accel_pitch;
    roll = 0.98 * (roll + gyro_rate_y * dt) + 0.02 * accel_roll;
    yaw = yaw + gyro_rate_z * dt;

#if SEND_AS_DEGREES
    pitch_cal = pitch * 180.0 / 3.14;
    roll_cal = roll * 180.0 / 3.14;
    yaw_cal = yaw * 180.0 / 3.14;
#else
    pitch_cal = pitch;
    roll_cal = roll;
    yaw_cal = yaw;
#endif
    last_time = current_time;
  }
  else
  {
    Serial.println("err");
  }
}



void send_bmi_data(int (*send_data)(String))
{
  integrate_data();
  String data = "{";
  data += "\"id\": 0,";
  data += "\"orientation\": {";
  data += "\"pitch\": " + String(pitch_cal) + ",";
  data += "\"roll\": " + String(roll_cal) + ",";
  data += "\"yaw\": " + String(yaw_cal) + ",";
  data += "\"unit\": \"" + unit + "\"";
  data += "}";
  data += "}";

  send_data(data);
}

void print_bmi160()
{
  integrate_data();
  Serial.print("Pitch: ");
  Serial.print(pitch_cal);
  Serial.print(" Roll: ");
  Serial.print(roll_cal);
  Serial.print(" Yaw: ");
  Serial.print(yaw_cal);
  Serial.print(" ");
  Serial.println(unit);
}