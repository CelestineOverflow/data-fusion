#include <Arduino.h>
#include "network.h"
#include "leds.h"
#include "bmiutils.h"
#include "Commander.h"


Commander cmd;

bool helloHandler(Commander &Cmdr){
  Cmdr.print("Hello! this is ");
  Cmdr.println(Cmdr.commanderName);
  return 0;
}

bool goodbyeHandler(Commander &Cmdr){
  Cmdr.print("Goodbye from ");
  Cmdr.println(Cmdr.commanderName);
  return 0;
}

//Now the command list must be defined
const commandList_t commands[] = {
  {"hello",       helloHandler,     "Say hello"},
  {"set",         goodbyeHandler,   "Say goodbye"},
};

//Initialisation function
void initialiseCommander(){
  cmd.begin(&Serial, commands, sizeof(commands)); //start Commander on Serial
}




void setup()
{
  Serial.begin(115200);
  // cmd.begin(&Serial, commands, sizeof(commands)); //start Commander on Serial
  // cmd.commandPrompt(ON);                          //enable the command prompt
  // cmd.echo(true);                                 //Echo incoming characters to theoutput port
  // Serial.println("Hello: Type 'help' to get help");
  // cmd.printCommandPrompt();
  // init_wifi();
  init_bmi160();
  // find_udp_server();
}

void loop()
{
  // cmd.update();
  print_bmi160();
  // send_bmi_data(send_data);
}


