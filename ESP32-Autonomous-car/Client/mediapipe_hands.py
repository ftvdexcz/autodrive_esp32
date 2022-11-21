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
          print('stop')
        elif check == [0,1,0,0,0]:
          print('left')
        elif check == [0,0,0,0,1]:
          print('right')
        elif check == [0,1,0,0,1]:
          print('forward')


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