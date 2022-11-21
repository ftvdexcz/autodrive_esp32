import numpy as np
import cv2
from mss import mss
import time 
from getkeys import key_check
import os 

def keys_to_output(keys):
  # [A, W, D]
  output = [0,0,0]

  if 'A' in keys:
    output[0] = 1
  elif 'W' in keys:
    output[1] = 1
  else:
    output[2] = 1
  
  return output

# bbox for game window 
bounding_box = {'top': 40, 'left': 0, 'width': 800, 'height': 600}

sct = mss()

file_name = 'training_data.npy'
# file_vid_name = 'training_data-vid.npy'

if os.path.isfile(file_name):
  print('File exists, loading previous data')
  training_data = list(np.load(file_name))
  # training_data_vid = list(np.load(file_vid_name))
else: 
  print('File does not exist')
  training_data = []
  # training_data_vid = []

def main():
  for i in list(range(4)) [::-1]:
    print(i+1)
    time.sleep(1)

  last_time = time.time()
  while True:
      sct_img = sct.grab(bounding_box) # capture frame
      img = cv2.cvtColor(np.array(sct_img), cv2.COLOR_RGB2GRAY) # convert gray scale
      img = cv2.resize(img, (160, 120)) # resize 
      keys = key_check()
      output = keys_to_output(keys)
      training_data.append([img, output])
      # training_data_vid.append(img)
      # print(f'Loop took: {time.time() - last_time}') # 0.02s -> 50fps  
      # last_time = time.time()

      if len(training_data) % 500 == 0: 
        print(len(training_data))
        np.save(file_name, np.array(training_data, dtype=object))
        # np.save(file_vid_name, np.array(training_data_vid, dtype=object))

      # cv2.imshow('screen', sct_img)

      # if (cv2.waitKey(1) & 0xFF) == ord('q'):
      #     cv2.destroyAllWindows()
      #     break

if __name__ == '__main__':
  main()