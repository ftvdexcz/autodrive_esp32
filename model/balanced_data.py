import numpy as np
import pandas as pd 
from collections import Counter 
from random import shuffle
import cv2 

train_data = np.load('training_data.npy', allow_pickle=True)

print(len(train_data))
df = pd.DataFrame(train_data)
print(df.head())

# đa số thời gian xe chạy thẳng => mất cân bằng dữ liệu
print(Counter(df[1].apply(str)))

lefts, rights, forwards = [], [], []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == [1, 0, 0]:
      lefts.append([img, choice])
    elif choice == [0, 1, 0]:
      forwards.append([img, choice])
    elif choice == [0, 0, 1]:
      rights.append([img, choice])
    else: 
      print('No matches!!')

forwards = forwards[:len(lefts)][:len(rights)]
lefts = lefts[:len(forwards)]
rights = rights[:len(rights)]

final_data = forwards + lefts + rights

shuffle(final_data)

print(len(final_data))
np.save('balanced_training_data.npy', np.array(final_data, dtype=object))

# for data in train_data: 
#   img = data[0]
#   # print(img.shape)
#   choice = data[1]
#   cv2.imshow('test', img)
#   print(choice)
#   if cv2.waitKey(25) & 0xFF == ord('q'):
#     cv2.destroyAllWindows()
#     break