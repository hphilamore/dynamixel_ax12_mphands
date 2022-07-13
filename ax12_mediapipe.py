import cv2
import mediapipe
import RPi.GPIO as GPIO
import serial
import time

import RPi.GPIO as GPIO
import serial
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)     # Control Data Direction Pin
GPIO.setup(6,GPIO.OUT)      # Blue LED Pin

GPIO.setup(26,GPIO.IN)      # S2 Push Button Pin
GPIO.setup(19,GPIO.IN)      # S3 Push Button Pin
GPIO.setup(13,GPIO.IN)      # S4 Push Button Pin

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


def move(servo_id, position):

	P = position  # position as 10-bit number 

	h = P >> 8    # value of high 8 bit byte

	l = P & 0xff        # value of low 8-bit byte                 
	
	# print('check', format(h, '#04x'),format(l, '#04x')) # print full hex string representation 
	
# 	checksum = hex(~(servo_id +
#                      ax_goal_length + 
#                      ax_write_data +
#                      0x1E + h + l)
#                    & 0xff)
	
	checksum = ~(servo_id + ax_goal_length + ax_write_data + 0x1E + h + l) & 0xff
	checksum = format(checksum, '#04x') # convert to hex number full representation (with 0x...) 
#                        
#     checksum = format(checksum, '#04x')       
	
	
	
	print(checksum)
	
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

	return(instruction_packet)

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

    #GPIO.output(6,GPIO.HIGH) # switch on LED 
    GPIO.output(18,GPIO.HIGH)
    #Dynamixel.write(bytearray.fromhex("FF FF 01 05 03 1E 00 00 D8"))  # Move Servo with ID = 1 to 0 degrees
    angle = 0
    Dynamixel.write(bytearray.fromhex(move(0x01, int(angle/300 * 1024))))  
    time.sleep(1)
    print(0)
    #Dynamixel.write(bytearray.fromhex("FF FF 01 05 03 1E CC 00 0C"))  # Move Servo with ID = 1 to 60 degrees
    angle = 60
    Dynamixel.write(bytearray.fromhex(move(0x01, int(angle/300 * 1024))))  # Move Servo with ID = 1 to position 205
    time.sleep(1)
    print(60)
    
    print(move(ax_id, 0))
    print(move(ax_id, int(60/300 * 1024)))
    print(move(ax_id, int(120/300 * 1024)))

    while (True):
 
        ret, frame = capture.read()
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
 
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
 
        
            for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
                print(f'HAND NUMBER: {hand_no+1}')
                print('-----------------------')
        
#                 for i in range(20):
#                     print(f'{handsModule.HandLandmark(i).name}:')
#                     print(f'{hand_landmarks.landmark[handsModule.HandLandmark(i).value]}')

#                 i in range(20):    
#                     print(f'{mp_hands.HandLandmark(i).name}:') 
#                     print(f'x: {hand_landmarks.landmark[handsModule.HandLandmark(i).value].x * image_width}')
#                     print(f'y: {hand_landmarks.landmark[handsModule.HandLandmark(i).value].y * image_height}')
#                     print(f'z: {hand_landmarks.landmark[handsModule.HandLandmark(i).value].z * image_width}n')
                    
                print(f'{handsModule.HandLandmark(0).name}:')
                print(f'{hand_landmarks.landmark[handsModule.HandLandmark(0).value]}')
#                 print(f'x: {hand_landmarks.landmark[handsModule.HandLandmark(0).value].x * frameWidth}')
#                 print(f'y: {hand_landmarks.landmark[handsModule.HandLandmark(0).value].y * frameHeight}')
#                 print(f'z: {hand_landmarks.landmark[handsModule.HandLandmark(0).value].z * frameWidth}n')
                
                print()
                
                print(f'{handsModule.HandLandmark(12).name}:')
                print(f'{hand_landmarks.landmark[handsModule.HandLandmark(12).value]}')
#                 print(f'x: {hand_landmarks.landmark[handsModule.HandLandmark(12).value].x * frameWidth}')
#                 print(f'y: {hand_landmarks.landmark[handsModule.HandLandmark(12).value].y * frameHeight}')
#                 print(f'z: {hand_landmarks.landmark[handsModule.HandLandmark(12).value].z * frameWidth}n')
        
                if hand_landmarks.landmark[handsModule.HandLandmark(12).value].x > 0.5:
                    GPIO.output(18,GPIO.HIGH)
                    #Dynamixel.write(bytearray.fromhex("FF FF 01 05 03 1E 00 00 D8"))  
                    angle = 0
                    Dynamixel.write(bytearray.fromhex(move(0x01, int(angle/300 * 1024))))
                    #GPIO.output(18,GPIO.HIGH)
                    #Dynamixel.write(bytearray.fromhex("FF FF 02 05 03 1E 00 00 D7"))  
                    #angle = 0
                    Dynamixel.write(bytearray.fromhex(move(0x02, int(angle/300 * 1024))))
                    
                    print(0)
                    
                else:
                    GPIO.output(18,GPIO.HIGH)
                    #Dynamixel.write(bytearray.fromhex("FF FF 01 05 03 1E CC 00 0C"))
                    angle = 60
                    Dynamixel.write(bytearray.fromhex(move(0x01, int(angle/300 * 1024))))
                    #GPIO.output(18,GPIO.HIGH)
                    #Dynamixel.write(bytearray.fromhex("FF FF 02 05 03 1E CC 00 0B"))
                    #angle = 60
                    Dynamixel.write(bytearray.fromhex(move(0x02, int(angle/300 * 1024))))
                    print(60)
        
        
        cv2.imshow('Test hand', frame)
 
        if cv2.waitKey(1) == 27:
            break
 
cv2.destroyAllWindows()
capture.release()