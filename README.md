# dynamixel_ax12_mphands

A program to run media pipe hand tracking and dynamixel ax-12 servos within the same program on a raspberry pi

Raspberry pi media pipe installation

Raspberry pi4 media pipe installation

Install buster legacy OS
sudo apt update
sudo apt install git
sudo apt-get install python3-pip

Raspi-config
- Enable serial
- Enable camera 
- Enable remote GPIO

Venv

Install opencv - instructions:
https://raspberrypi-guide.github.io/programming/install-opencv

- pip3 install opencv-python==4.5.3.56

- Install dependencies from link above  

- pip3 install numpy --upgrade (https://raspberrypi-guide.github.io/programming/install-opencv) (this will take a really long time!) 

- Install dependencies (perhaps not needed?) (https://stackoverflow.com/questions/53347759/importerror-libcblas-so-3-cannot-open-shared-object-file-no-such-file-or-dire)

- pip3 install mediapipe-rpi4 
- (Check if raspberry pi 3 or 4) 
- https://pypi.org/project/mediapipe-rpi4/

- Enable raspberry pi camera in rasps-config 
- pip install "picamera[array]" —> [ not sure this step is necessary! ]


This warning may show but it won’t stop things working ‘matplotlib 3.5.2 has requirement numpy>=1.17, but you'll have numpy 1.16.2 which is incompatible.’



Communication with Arduino over i2c
Raspi-config
- Enable I2C
