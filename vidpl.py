import io
import cv2
import numpy as np
import requests
from PIL import Image
import time
import pytesseract
from requests_toolbelt.multipart.encoder import MultipartEncoder
import easyocr

# pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

cap = cv2.VideoCapture('cars/vid7.mp4')

pTime = 0
cTime = 0

try:

   while True:
      success, img = cap.read()

      cTime = time.time()
      fps = 1/(cTime-pTime)
      pTime = cTime

      image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      pilImage = Image.fromarray(image)

      buffered = io.BytesIO()
      pilImage.save(buffered, quality=100, format="JPEG")

      try:

         # Build multipart form and post request
         m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})

         response = requests.post("https://detect.roboflow.com/car-number-plate-j5uqm/1?api_key=SAkY1wxTTmGkBnJRn4UA", data=m, headers={'Content-Type': m.content_type})

         data = response.json()

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

         fontScalee = (imWidth * imHeight) / (4000 * 4000)

         # cv2.putText(img , str(int(fps)), (15, 40), cv2.FONT_HERSHEY_PLAIN, 2, (244,0,218), 2, )

         cv2.rectangle(img, start_point, end_point, color=(0, 255, 0), thickness=2)
         
         

         roi = img[start_point[1]:end_point[1], start_point[0]:end_point[0]]
         img_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
         # medianBlur = cv2.medianBlur(img_gray,3)
         thresholding = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
         # kernel = np.ones((2,2),np.uint8)
         # dilating = cv2.dilate(thresholding, kernel, iterations = 1)
         # kernel2 = np.ones((1,1),np.uint8)
         # erode = cv2.erode(dilating, kernel2, iterations = 1)
         # morphologyEx = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel)

         # ret, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

         plate = pytesseract.image_to_string(thresholding)

         ## box char
         hImg, wImg = img_gray.shape
         boxes = pytesseract.image_to_boxes(img_gray)
         for b in boxes.splitlines():
            b = b.split(' ')
            # print(b)
            x,y,w,h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(img_gray, (x,hImg-y), (w, hImg-h), (0,0,255), 2)

         reader = easyocr.Reader(['en'])
         result = reader.readtext(roi)

         cv2.putText(img, result[0][-2], (15, 60), 0, 2, 255, 3, 1)

         logo = cv2.resize(img, (854, 480))

         # print(data)
         print("Number plate is: ", result[0][-2])
         

         # cv2.imshow('det', roi)
         cv2.imshow('det', roi)
         

         cv2.imshow('Car Tracker', logo)
      except:
         print('No Number Plate Found 2')
      if cv2.waitKey(5) & 0xff == 27:
         break
except:
   print('No Number Plate Found')
