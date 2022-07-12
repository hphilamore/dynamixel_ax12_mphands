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

Dynamixel=serial.Serial("/dev/ttyS0",baudrate=1000000,timeout=0.1, bytesize=8)   # UART in ttyS0 @ 1Mbps

 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
 
capture = cv2.VideoCapture(0)

frameWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=N_hands) as hands:

    GPIO.output(6,GPIO.HIGH)
    GPIO.output(18,GPIO.HIGH)
    #Dynamixel.write(bytearray.fromhex("FF FF 01 05 03 1E CD 00 0B"))  # Move Servo with ID = 1 to position 205
    Dynamixel.write(bytearray.fromhex("FF FF 01 05 03 1E 00 00 D8"))  # Move Servo with ID = 1 to position 205
    time.sleep(1)
    print(0)
    Dynamixel.write(bytearray.fromhex("FF FF 01 05 03 1E CC 00 0C"))  # Move Servo with ID = 1 to position 205
    time.sleep(1)
    print(60)

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
                    Dynamixel.write(bytearray.fromhex("FF FF 01 05 03 1E 00 00 D8"))  # Move Servo with ID = 1 to position 205
                    print(0)
                    
                else:
                    GPIO.output(18,GPIO.HIGH)
                    Dynamixel.write(bytearray.fromhex("FF FF 01 05 03 1E CC 00 0C"))  # Move Servo with ID = 1 to position 205
                    print(60)
        
        
        cv2.imshow('Test hand', frame)
 
        if cv2.waitKey(1) == 27:
            break
 
cv2.destroyAllWindows()
capture.release()