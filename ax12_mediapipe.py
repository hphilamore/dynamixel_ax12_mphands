# Connecting rapsberry pi to arduino using i2c
#https://www.deviceplus.com/arduino/connecting-a-raspberry-pi-to-an-arduino-uno/
#https://www.deviceplus.com/arduino/using-i2c-and-an-arduino-uno-to-work-with-analogue-voltages-on-a-raspberry-pi/

import cv2
import mediapipe
import RPi.GPIO as GPIO
import serial
import time

import RPi.GPIO as GPIO
import serial
import time
from smbus import SMBus

arduino = 0x8
i2cbus = SMBus(1)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)     # Control Data Direction Pin


# Pins on savage electronics board for RPi zero
# GPIO.setup(6,GPIO.OUT)      # Blue LED Pin 
# GPIO.setup(26,GPIO.IN)      # S2 Push Button Pin
# GPIO.setup(19,GPIO.IN)      # S3 Push Button Pin
# GPIO.setup(13,GPIO.IN)      # S4 Push Button Pin

# pins for communicating with scribbler robot
GPIO.setup(6,GPIO.OUT)      
GPIO.setup(26,GPIO.OUT)      

N_hands = 2

# TODO: work out how to change serial0--> AMA0 on RPi
# TODO: set serial permissions on RPi so that 'sudo su' not required to acess ttyS0 to run programme
# https://roboticsbackend.com/raspberry-pi-hardware-permissions/
# TODO: add set-up stuff to README on repo 
Dynamixel=serial.Serial("/dev/ttyS0",baudrate=1000000,timeout=0.1, bytesize=8)   # UART in ttyS0 @ 1Mbps

 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
 
capture = cv2.VideoCapture(0)

frameWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

ax_start = 0xFF    # 2 x FF bytes indicate start of incoming packet 
ax_id = 0x01       # servo ID 
ax_goal_length = 0x05 # length of instruction packet (N parameters + 2)

# instructions for servo to perform 
ax_ping = 0x01
ax_read_data = 0x02
ax_write_data = 0x03
ax_reg_write = 0x04
ax_action = 0x05
ax_reset = 0x06
ax_sync_write = 0x83
ax_ccw_angle_limit_l = 0x08
ax_ccw_al_lt = 0x00
ax_ccw_al_l = 0xFF
ax_ccw_al_h = 0x03
ax_speed_length = 0x05
ax_goal_speed_l = 0x20
ccw = 0
cw = 1


def move(servo_id, position):

	P = position  # position as 10-bit number
	
	print(P/1024 * 300)

	h = P >> 8    # value of high 8 bit byte

	l = P & 0xff        # value of low 8-bit byte                 
	
	checksum = ~(servo_id + ax_goal_length + ax_write_data + 0x1E + h + l) & 0xff
	checksum = format(checksum, '#04x') # convert to hex number full representation (with 0x...) 
	
	#print('checksum = ', checksum)
	
	instruction_packet = (format(ax_start, '02x') + " " +
                          format(ax_start, '02x') + " " +
                          format(servo_id, '02x') + " " + 
                          format(ax_goal_length, '02x') + " " +
                          format(ax_write_data, '02x') + " " +
                          format(0x1E, '02x') + " " +
                          format(l, '02x') + " " +
                          format(h, '02x') + " " +
                          checksum[2:] 
                          ).upper()
                          #str(ax_write_data) + str(0x1E) + str(l) + str(h) + str(checksum))
	
	#print(instruction_packet)
	
	Dynamixel.write(bytearray.fromhex(instruction_packet))

	return(instruction_packet)



def set_endless(servo_id, status):
    
    if status: # turn endless rotation on               
	
        checksum = ~(servo_id + ax_goal_length + ax_write_data + ax_ccw_angle_limit_l) & 0xff
        checksum = format(checksum, '#04x') # convert to hex number full representation (with 0x...) 
        
        #print('checksum = ', checksum)
        
        instruction_packet = (format(ax_start, '02x') + " " +
                              format(ax_start, '02x') + " " +
                              format(servo_id, '02x') + " " + 
                              format(ax_goal_length, '02x') + " " +
                              format(ax_write_data, '02x') + " " +
                              format(ax_ccw_angle_limit_l, '02x') + " " +
                              format(ax_ccw_al_lt, '02x') + " " +
                              format(ax_ccw_al_lt, '02x') + " " +
                              checksum[2:] 
                               ).upper()
                              
	
    else: # turn endless rotation off
        
        checksum = ~(servo_id + ax_goal_length + ax_write_data +
                     ax_ccw_angle_limit_l + ax_ccw_al_l + ax_ccw_al_h) & 0xff
        checksum = format(checksum, '#04x') # convert to hex number full representation (with 0x...)
        
        print('checksum = ', checksum)
        
        instruction_packet = (format(ax_start, '02x') + " " +
                              format(ax_start, '02x') + " " +
                              format(servo_id, '02x') + " " + 
                              format(ax_goal_length, '02x') + " " +
                              format(ax_write_data, '02x') + " " +
                              format(ax_ccw_angle_limit_l, '02x') + " " +
                              format(ax_ccw_al_l, '02x') + " " +
                              format(ax_ccw_al_h, '02x') + " " +
                              checksum[2:] 
                              ).upper()
        
    #print(instruction_packet)
    
    Dynamixel.write(bytearray.fromhex(instruction_packet))
    
    return(instruction_packet)



def turn(servo_id, side, speed):
    if side == ccw:
        #print('ccw')
        speed_h = speed >> 8 # convert position as 10-bit number to high 8 bit byte
        speed_l = speed & 0xff
        
    else:
        #print('cw')
        speed_h = (speed >> 8) + 4
        speed_l = speed & 0xff
        
    checksum = ~(servo_id + ax_speed_length + ax_write_data +
                 ax_goal_speed_l + speed_l + speed_h) & 0xff
    
    checksum = format(checksum, '#04x') # convert to hex number full representation (with 0x...)
    
    #print('checksum = ', checksum)
    
    instruction_packet = (format(ax_start, '02x') + " " +
                          format(ax_start, '02x') + " " +
                          format(servo_id, '02x') + " " + 
                          format(ax_speed_length, '02x') + " " +
                          format(ax_write_data, '02x') + " " +
                          format(ax_goal_speed_l, '02x') + " " +
                          format(speed_l, '02x') + " " +
                          format(speed_h, '02x') + " " +
                          checksum[2:] 
                          ).upper()
        
    #print(instruction_packet)
    
    Dynamixel.write(bytearray.fromhex(instruction_packet))
    
    return(instruction_packet)


def sweep(servo_id):
    for i in range(300):
        move(servo_id, int(i/300 * 1024))
        time.sleep(0.1)
        print(i)
        
def binary_position(servo_id, x):
    set_endless(servo_id, False)
    if x > 0.5:
        GPIO.output(18,GPIO.HIGH) 
        angle = 0
        move(servo_id, int(angle/300 * 1024))
        print(angle)

        
    else:
        GPIO.output(18,GPIO.HIGH)
        angle = 60
        move(servo_id, int(angle/300 * 1024))   
        print(angle)


def binary_rotation(servo_id, x):
    set_endless(servo_id, True)
    if x > 0.5:
        GPIO.output(18,GPIO.HIGH) 
        turn(servo_id, ccw, 500)


    else:
        GPIO.output(18,GPIO.HIGH)
        turn(servo_id, cw, 500)
        
        
        
def follow_hand(x, z):
    GPIO.output(18,GPIO.HIGH) 
    set_endless(0x01, True)
    set_endless(0x02, True)
    
    if 0.0 < x < 1.0:              # hand detected in frame
        #val = int(255 * x)
        z_scale_factor = 10; 
        val = int(255 * z_scale_factor * abs(z))
        if val>255:val=255         # cap value sent over i2c at 255  
        print(val);
        #GPIO.output(26,GPIO.HIGH)
        try:
            i2cbus.write_byte(arduino, val)
        except:
            print("connection to arduino failed")
        
        if z <= -0.5:
            print('stop')
            turn(0x01, ccw, 0)
            turn(0x02, cw, 0)
        
        elif x < 0.4:                # turn left
            print('hand left')
            turn(0x01, ccw,  500)
            turn(0x02, cw, 0)
             
        elif x > 0.6:              # turn right
            print('hand right')
            turn(0x01, ccw,  0)
            turn(0x02, cw, 500)
            
        else:                      # go forwards
            print('hand centre')
            turn(0x01, ccw,  500)
            turn(0x02, cw, 500)
            
    
#     else:                          # stop
#         #GPIO.output(26,GPIO.LOW)
#         i2cbus.write_byte(arduino, 0)
#         print('no hand')
#         turn(0x01, cw, 0)
#         turn(0x02, ccw, 0) 

        
        
def continuous_position(servo_id, x):
    #  Continous position selection based on hand tracking
    if x >= 0:                         # move function only accepts positive integers 
        finger_x_pos = x
        finger_x_pos *= 1024
        move(servo_id, int(finger_x_pos)) 


def binary_scribbler_GPIO(x):

    if x > 0.5:
        GPIO.output(6,GPIO.HIGH) 
        GPIO.output(26,GPIO.LOW) 
        angle = 0
        print(angle)

        
    else:
        GPIO.output(26,GPIO.HIGH) 
        GPIO.output(6,GPIO.LOW)  
        angle = 60
        print(angle)
        
        
def forwards():
    GPIO.output(18,GPIO.HIGH) 
    set_endless(0x01, True)
    set_endless(0x02, True)
    
    turn(0x01, ccw,500)
    turn(0x02, cw, 500)    


def move_check(servo_id, position):

	P = position  # position as 10-bit number 

	B = P/256               # seperate into 2 8 bit bytes by dividing by max value of 8 bit byte 

	H = int(B // 1)         # decimal value of high byte, convert to intager

	L = B - H                     
	L = int(L * 256)        # decimal value of low byte

	H = hex(H)

	L = hex(L)
	
	print(H,L)

	return(H, L)

 
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=N_hands) as hands:

    
    #sweep(0x02)
    
    #forwards()

   

    while (True):
 
        ret, frame = capture.read()
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        
 
        if results.multi_hand_landmarks != None:
            print('hand detected - ', end='')
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
 
            for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
                print(f'HAND NUMBER: {hand_no+1}')
                print('-----------------------')
        
                  # show all 20 hand positions 
#                 for i in range(20):
#                     print(f'{handsModule.HandLandmark(i).name}:')
#                     print(f'{hand_landmarks.landmark[handsModule.HandLandmark(i).value]}')

                
                # show wrist position 
                print(f'{handsModule.HandLandmark(0).name}:')
                print(f'{hand_landmarks.landmark[handsModule.HandLandmark(0).value]}')               
                print()
                
                # show middle finger tip position 
                print(f'{handsModule.HandLandmark(12).name}:')
                print(f'{hand_landmarks.landmark[handsModule.HandLandmark(12).value]}')
                
                x = hand_landmarks.landmark[handsModule.HandLandmark(12).value].x
                z = hand_landmarks.landmark[handsModule.HandLandmark(12).value].z

                print(f'x = {x}')
                print(f'z = {z}')
                
                # binary_position(0x01, x)
                
#                 binary_rotation(0x01, x)
#                 binary_rotation(0x02, x)

                follow_hand(x,z)
                
                
                
                
                #continuous_position(x)                   
#                 # Continous position selection based on hand tracking
#                 if hand_landmarks.landmark[handsModule.HandLandmark(12).value] != None: 
#                     finger_x_pos = hand_landmarks.landmark[handsModule.HandLandmark(12).value].x
#                     finger_x_pos *= 1024
#                     move(0x01, int(finger_x_pos)) 
                # binary_scribbler_GPIO(x)
                
                
        else:                          # stop
            #GPIO.output(26,GPIO.LOW)
            try:
                i2cbus.write_byte(arduino, 0)
            except:
                print("connection to arduino failed")
            
            print('no hand')
            turn(0x01, cw, 0)
            turn(0x02, ccw, 0) 
                
        
        # comment out for set-up without display e.g/ headless raspberry pi
        cv2.imshow('Test hand', frame)
 
        if cv2.waitKey(1) == 27:
            break
 
cv2.destroyAllWindows()
capture.release()
