import numpy as np
import pandas as pd
import os
import cv2
import time
import random
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array

paths=[]
for dirname, _, filenames in os.walk('dataset/Car_Number_Plate'):
    for filename in filenames:
        paths+=[os.path.join(dirname, filename)]

n=len(paths)
# num=random.sample(range(n),k=4)

labels = open('dataset\Yolo_weights_for_licence plate_detector\classes.names').read()
print(labels)

weights_path = 'dataset\Yolo_weights_for_licence plate_detector\lapi.weights'
configuration_path = 'dataset\Yolo_weights_for_licence plate_detector\darknet-yolov3.cfg'

probability_minimum = 0.5
threshold = 0.3

network = cv2.dnn.readNetFromDarknet(configuration_path, weights_path)
layers_names_all = network.getLayerNames()
layers_names_output = [layers_names_all[i[0]-1] for i in network.getUnconnectedOutLayers()]

image_input = cv2.imread('car1.jpeg')

# %matplotlib inline
plt.rcParams['figure.figsize'] = (10.0,10.0)
plt.imshow(cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB))
plt.show()

