import io
import cv2
import numpy as np
import requests
from PIL import Image
import pytesseract
from requests_toolbelt.multipart.encoder import MultipartEncoder
import easyocr

# pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

# Load Image with PIL
img = cv2.imread("cars/a1.jpg")
image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
pilImage = Image.fromarray(image)

# Convert to JPEG Buffer
buffered = io.BytesIO()
pilImage.save(buffered, quality=100, format="JPEG")

# Build multipart form and post request
m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})

response = requests.post("https://detect.roboflow.com/car-number-plate-j5uqm/1?api_key=bgo9ajpdfCbf5L4VJzdY", data=m, headers={'Content-Type': m.content_type})

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

fontScale = (imWidth * imHeight) / (1000 * 1000)

cv2.rectangle(img, start_point, end_point, color=(0, 255, 0), thickness=2)

# cv2.putText(img, className, start_point, cv2.FONT_HERSHEY_DUPLEX, fontScale, color=(0, 2, 255), thickness=2)

# print(start_point[1])
roi = img[start_point[1]:end_point[1], start_point[0]:end_point[0]]

img_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
medianBlur = cv2.medianBlur(img_gray,5)
thresholding = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
kernel = np.ones((1,1),np.uint8)
dilating = cv2.dilate(thresholding, kernel, iterations = 1)
erode = cv2.erode(dilating, kernel, iterations = 1)
morphologyEx = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel)

cv2.imwrite('lpcar.png',img_gray)
crop_img = 'lpcar.png'

# print(xp, yp)



# ret, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# plate = pytesseract.image_to_string(thresholding)


# cv2.putText(img, plate, start_point, 0, 2, 255, 2,cv2.FONT_HERSHEY_DUPLEX)


xx = 'MH 43 AT 8022'

reader = easyocr.Reader(['en'])
result = reader.readtext(roi)

if xx in str(result):
   print('--Yes')
else:
   print("--No")

print("Number plate is: ", result)

cv2.imshow('img', img)
# cv2.imshow('det', roi)
cv2.imshow('rosi', roi)
cv2.waitKey(0)