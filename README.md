# dynamixel_ax12_mphands

A program to run media pipe hand tracking and dynamixel ax-12 servos within the same program on a raspberry pi

Raspberry pi media pipe installation


Install buster legacy OS
sudo apt update
sudo apt install git
sudo apt-get install python3-pip

Sudo saspi-config
- Enable serial
- Enable camera 
- Enable remote GPIO

(Venv)

Install opencv - instructions:
https://qengineering.eu/install-opencv-4.4-on-raspberry-64-os.html
(or https://qengineering.eu/install-opencv-4.4-on-raspberry-pi-4.html)

https://raspberrypi-guide.github.io/programming/install-opencv
Or
https://stackoverflow.com/questions/53347759/importerror-libcblas-so-3-cannot-open-shared-object-file-no-such-file-or-dire)

- pip3 install opencv-python==4.5.3.56

- Install prerequistes from link above  

- pip3 install numpy --upgrade (https://raspberrypi-guide.github.io/programming/install-opencv) (this will take a really long time!) 


- pip3 install mediapipe-rpi4 
- (Check if raspberry pi 3 or 4) 
- https://pypi.org/project/mediapipe-rpi4/

- Enable raspberry pi camera in rasps-config 


This warning may show but it won’t stop things working ‘matplotlib 3.5.2 has requirement numpy>=1.17, but you'll have numpy 1.16.2 which is incompatible.’

Communication with Arduino over i2c:
Raspi-config —> Enable I2C

Communication with ADC over SPI:
https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi?view=all
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-mcp3xxx
Raspi-config —> Enable SPI


These are now the possible options for communicating with the raspberry pi :
1. All RPi connect to router via static IP 
2. Connect Mac to router/phone internet and use ethernet bridge to RPi
3. Set phone internet as router for all RPi (with static IP)
4. Connect computer to router wirelessly and connect RPi to router via ethernet 

If you see this warning when using ssh:
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Enter this:
ssh-keygen -R 192.168.1.247


If you need to ist IP adresses on bridge network, enter this:
arp -a | grep : | grep bridge100
