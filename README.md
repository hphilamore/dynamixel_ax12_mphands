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


Install opencv by following instructions:
https://qengineering.eu/install-opencv-4.4-on-raspberry-64-os.html
(or https://qengineering.eu/install-opencv-4.4-on-raspberry-pi-4.html)

Prerequisites for installing mediapipe
pip3 install --upgrade setuptools
pip3 install numpy --upgrade

Install mediapipe (checking RPi model is correct)
pip3 install mediapipe-rpi4


If you see this warning when using ssh:
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Enter this:
ssh-keygen -R 192.168.1.247


If you need to ist IP adresses on bridge network, enter this:
arp -a | grep : | grep bridge100
