import socket               # Import socket module
import time
from pynput.keyboard import Listener, Key, Controller
import json
from log import key_check

kb = Controller()

def key_out(key):
    output = [0, 0, 0, 0] # A, W, S, D 
    if 'A' in key:
        output[0] = 1
    if 'D' in key:
        output[3] = 1
    if 'W' in key:
        output[1] = 1
    if 'S' in key:
        output[2] = 1
    return output

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        
        landmarks = hand_landmarks.landmark
        # print(landmarks)
        
        check = [] # 0: close, 1: open
        if landmarks[4].x < landmarks[5].x: 
          check.append(0) 
        else:
          check.append(1)

        for i in range(4):
          if landmarks[8+i*4].y < landmarks[5+i*4].y:
            check.append(1)
          else:
            check.append(0)
        
        if check == [1,1,1,1,1]:
          # print('down')
          kb.press('s')
          kb.release('w')
          kb.release('a')
          kb.release('d')
        elif check == [0,1,0,0,0]:
          # print('left')
          kb.press('a')
          kb.release('s')
          kb.release('w')
          kb.release('d')
        elif check == [0,0,0,0,1]:
          # print('right')
          kb.press('d')
          kb.release('a')
          kb.release('w')
          kb.release('s')
        elif check == [0,1,0,0,1]:
          # print('forward')
          kb.press('w')
          kb.release('a')
          kb.release('d')
          kb.release('s')

        key = key_check()
        a = key_out(key)
        x = '{"a":'
        x += str(a[0])
        x += ',"d":'
        x += str(a[3])
        x += ',"w":'
        x += str(a[1])
        x += ',"s":'
        x += str(a[2])
        x += "}"
        msg = str.encode(x, 'utf-8')
        print(x)
        
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    

cap.release()
kb.release('w')
kb.release('a')
kb.release('s')
kb.release('d')


 
