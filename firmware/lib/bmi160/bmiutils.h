#include <DFRobot_BMI160.h>
#include <Arduino.h>

static DFRobot_BMI160 bmi160;
static const int8_t i2c_addr = 0x68;

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
    Serial.println("init bmi160 done");
}

void print_bmi160()
{
      int i = 0;
  int rslt;
  int16_t accelGyro[6]={0}; 
  
  //get both accel and gyro data from bmi160
  //parameter accelGyro is the pointer to store the data
  rslt = bmi160.getAccelGyroData(accelGyro);
  if(rslt == 0){
    for(i=0;i<6;i++){
      if (i<3){
        //the first three are gyro data
        Serial.print(accelGyro[i]*3.14/180.0);Serial.print("\t");
      }else{
        //the following three data are accel data
        Serial.print(accelGyro[i]/16384.0);Serial.print("\t");
      }
    }
    Serial.println();
  }else{
    Serial.println("err");
  }
}
//send data to function pointer
void send_bmi_data(int (*send_data)(String))
{
    int i = 0;
    int rslt;
    int16_t accelGyro[6] = {0};

    //get both accel and gyro data from bmi160
    //parameter accelGyro is the pointer to store the data
    rslt = bmi160.getAccelGyroData(accelGyro);
    if (rslt == 0)
    {
        for (i = 0; i < 6; i++)
        {
            if (i < 3)
            {
                send_data(String(accelGyro[i] * 3.14 / 180.0) + "\t");
            }
            else
            {
                send_data(String(accelGyro[i] / 16384.0) + "\t");
            }
        }
        Serial.println();
    }
    else
    {
        Serial.println("err");
    }
}