import numpy as np
import cv2
from mss import mss
import time 
from directkeys import ReleaseKey, PressKey, W, A, S, D
from getkeys import key_check
from alexnet import alexnet

width, height = 160, 120
lr = 1e-3
epochs = 10
model_name = 'training_data_and_model/model/pygta5-car-fast-{}-{}-{}-epochs-300K-data.model'.format(lr, 'alexnetv2', epochs)

t_time = 0.08

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(W)
    PressKey(A)
    ReleaseKey(D)
    time.sleep(t_time) # trong khoảng t_time này sẽ tiếp tục rẽ trái (PressKey(A)), không ReleaseKey ngay lập tức 
    ReleaseKey(A) 

def right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    time.sleep(t_time)
    ReleaseKey(D)

model = alexnet(width, height, lr)
model.load(model_name)

# bbox for game window 
bounding_box = {'top': 40, 'left': 0, 'width': 800, 'height': 600}

sct = mss()

def main():
  for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

  paused = False
  last_time = time.time()
  while True:
      if not paused: 
        sct_img = sct.grab(bounding_box)
    
        print(f'Loop took: {time.time() - last_time}') # 0.02s -> 50fps  
        last_time = time.time() 

        screen_frame = cv2.cvtColor(np.array(sct_img), cv2.COLOR_RGB2GRAY)
        screen_frame = cv2.resize(screen_frame,(160, 120))

        prediction = model.predict([screen_frame.reshape(width, height, 1)])[0]
        moves = list(np.around(prediction))
        print(prediction)

        turn_thresh = .75
        fwd_thresh = 0.7
        right_thresh = 0.8

        if prediction[1] > fwd_thresh:
            straight()
        elif prediction[0] > turn_thresh:
            left()
        elif prediction[2] > right_thresh:
            right()
        else:
            straight()

        # if moves == [1, 0, 0]:
        #   left()
        # elif moves == [0, 1, 0]:
        #   straight()
        # elif moves == [0, 0, 1]:
        #   right()

      keys = key_check()
      if 'T' in keys: 
        if paused: 
          paused = False
          time.sleep(1)
        else: 
          paused = True
          ReleaseKey(A)
          ReleaseKey(W)
          ReleaseKey(D)
          time.sleep(1)

if __name__ == '__main__':
  main()