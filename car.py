import io
import cv2
import numpy as np
import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Load Image with PIL
img = cv2.imread("cars/rcar.jpeg")
image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
pilImage = Image.fromarray(image)

# Convert to JPEG Buffer
buffered = io.BytesIO()
pilImage.save(buffered, quality=100, format="JPEG")

# Build multipart form and post request
m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})

response = requests.post("https://detect.roboflow.com/car-number-plate-j5uqm/1?api_key=SAkY1wxTTmGkBnJRn4UA", data=m, headers={'Content-Type': m.content_type})

data = response.json()

# image = cv2.rectangle(image, start_point, end_point, color, thickness)

# print(data[''])

# print(response)
imWidth = int(data['predictions'][0]['width'])
imHeight = int(data['predictions'][0]['height'])
xp = int(data['predictions'][0]['x'])
yp = int(data['predictions'][0]['y'])
className = data['predictions'][0]['class']
confidence = float(data['predictions'][0]['confidence'])

start_x = xp - (imWidth / 2)

start_y = yp - (imHeight / 2)

start_point = (int(start_x), int(start_y))

end_x = xp + (imWidth / 2)

end_y = yp + (imHeight / 2)

end_point = (int(end_x), int(end_y))

fontScale = (imWidth * imHeight) / (4000 * 4000)

cv2.rectangle(img, start_point, end_point, color=(0, 255, 0), thickness=2)
cv2.putText(img, className, start_point, 0, 2, 255, 2,cv2.FONT_HERSHEY_DUPLEX)
# cv2.putText(img, className, start_point, cv2.FONT_HERSHEY_DUPLEX, fontScale, color=(0, 2, 255), thickness=2)

# print(start_point[1])
roi = img[start_point[1]:end_point[1], start_point[0]:end_point[0]]

img_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)


# print(xp, yp)

cv2.imshow('img', img)
cv2.imshow('det', roi)
cv2.imshow('rosi', img_gray)
cv2.waitKey(0)