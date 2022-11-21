import numpy as np
import cv2
from mss import mss
import time 
from getkeys import key_check
import os 
from directkeys import ReleaseKey, PressKey, W, A, S, D


# bbox for game window 
bounding_box = {'top': 40, 'left': 0, 'width': 800, 'height': 600}

sct = mss()

def main():
  for i in list(range(4)) [::-1]:
    print(i+1)
    time.sleep(1)

  # Test input directkeys
  # print('down')
  # PressKey(W)
  # time.sleep(3)
  # print('up')
  # ReleaseKey(W)

  last_time = time.time()
  while True:
      sct_img = sct.grab(bounding_box) # capture frame
      img = cv2.cvtColor(np.array(sct_img), cv2.COLOR_RGB2GRAY) # convert gray scale
      img = cv2.resize(img, (80, 60)) # resize 
      print(f'Loop took: {time.time() - last_time}') # 0.02s -> 50fps  
      last_time = time.time()

      cv2.imshow('screen', sct_img)

      if (cv2.waitKey(1) & 0xFF) == ord('q'):
          cv2.destroyAllWindows()
          break

if __name__ == '__main__':
  main()