# data-fusion
 apriltags + imus ❤️


Go to '/docs' for the README.md file with images 
<!-- 
- [vscode](https://code.visualstudio.com/)
- [platformio](https://marketplace.visualstudio.com/items?itemName=platformio.platformio-ide)

additionally, for the python scripts we will be using:

- [python3](https://www.python.org/downloads/)

for jupyter notebooks you can either view them on vscode (recommended) or use:

- [jupyter](https://jupyter.org/install)


## Project structure:

- `firmware/` contains the microcontroller code
- `api/` - contains the python api for exposing the microcontroller data.
- `viewer/` - contains the sveltekit visualization code.


## Firmware Setup

As for the physical setup, you will need:

- ESP8266 microcontroller board provided to you.
- USB C cable to connect the microcontroller to your computer.

There are to connectors on the microcontroller board, one for the serial communication with the computer and the other for usb charging of a lipo battery. Use the serial connector to connect the microcontroller to your computer.

![microcontroller](./images/microcontroller.jpg)



for the microcontroller code, you will need to install the platformio extension for vscode:

- [platformio](https://marketplace.visualstudio.com/items?itemName=platformio.platformio-ide)


Once installed, you can open the folder `firmware/` in vscode and flash the code to the microcontroller.

Y


<!-- ## Sveltekit Setup

for visualization we will be using sveltekit, you will need nodejs to run it:

- [nodejs](https://nodejs.org/en/download/)

to run the visualization, you will need to install the dependencies and run the dev server:

```bash
cd viewer
npm install
npm run dev
```

## Installing three.js for sveltekit
```bash
npm install --save three 
npm i --save-dev @types/three
``` --> 