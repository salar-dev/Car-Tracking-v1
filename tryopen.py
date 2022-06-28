import cv2
import os

directory = 'cars'
for filename in os.listdir(directory):
   if filename.endswith(".mp4"):
      print(os.path.join(directory, filename))
   else:
      continue