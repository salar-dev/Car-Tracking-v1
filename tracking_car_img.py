import cv2
import os
import io
from datetime import datetime
from PIL import Image
from cv2 import split
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import easyocr
import colorama
from colorama import Fore, Back, Style



directory = 'cars/images'
num_in_car = []


print('\033[39m')
## Ask User to enter number of the car
CarNumber = input(f'{Fore.GREEN}Enter Car Number -> ')
print('\033[39m')

for filename in os.listdir(directory):
   if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):

      ## Get Now Time and Date
      currentDateAndTime = datetime.now()
      _hour = currentDateAndTime.hour
      _minute = currentDateAndTime.minute
      _second = currentDateAndTime.second
      _cday = datetime.today().strftime("%p")
      # _year = currentDateAndTime.year
      # _month = currentDateAndTime.month
      # _day = currentDateAndTime.day

      ## Put Time in one val
      timeNow = ('{}:{}:{} {}'.format(_hour, _minute, _second, _cday))

      file_dir = str(os.path.join(directory, filename))
      # print(file_dir)

      ## Open Curent file with opencv
      img = cv2.imread(file_dir) ## using $file_dir val with cv2.imread
      image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert img from bgr to rgb
      pilImage = Image.fromarray(image) ## put cv2 image to PIL Image

      #Convert to JPEG Buffer
      buffered = io.BytesIO()
      pilImage.save(buffered, quality=100, format="JPEG")

      # Build multipart form and post request
      m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})

      # Put RoboFlow Project Link with v number and api of user
      response = requests.post("https://detect.roboflow.com/car-number-plate-j5uqm/1?api_key=SAkY1wxTTmGkBnJRn4UA", data=m, headers={'Content-Type': m.content_type})

      data = response.json() ## Convert data from link to json data 

      ######### Put all data in variables #########
      imWidth = int(data['predictions'][0]['width'])  ## Width of image
      imHeight = int(data['predictions'][0]['height']) ## Height of image
      xp = int(data['predictions'][0]['x'])   ## x cinter point of license plate
      yp = int(data['predictions'][0]['y'])   ## y cinter point of license plate
      className = data['predictions'][0]['class']  ## className always br "LP"
      confidence = float(data['predictions'][0]['confidence']) ## How confidence it's
      #############################################

      #### Making Variables to Calculate Rectangle Size and Postion ###########
      #### We user rectangle with opencv to draw around license plate of car ##
      start_x = xp - (imWidth / 2)
      start_y = yp - (imHeight / 2)
      start_point = (int(start_x), int(start_y))
      end_x = xp + (imWidth / 2)
      end_y = yp + (imHeight / 2)
      end_point = (int(end_x), int(end_y))
      ## draw around license plate of car on $img ##
      cv2.rectangle(img, start_point, end_point, color=(0, 255, 0), thickness=2)
      ##############################################

      ## Crop license plate from the image and put in val $cropedPlate
      cropedPlate = img[start_point[1]:end_point[1], start_point[0]:end_point[0]]

      ## Save Crop license plate to the project direct if we need to do some process on it ....
      cv2.imwrite('cropedPlate.png', cropedPlate)
      
      ## Read Number of icense plate of car as Text and saving in $result val, only English >>>
      ## You can change the language to ar - arabic or any language you want.
      reader = easyocr.Reader(['en'])
      result = reader.readtext(cropedPlate)

      ## Print the number of car.
      print("Number plate is: ", result[0][-2])

      # resizedImg = cv2.resize(img, (854, 480))

      cv2.putText(img, result[0][-2], (15, 60), 0, 2, 255, 3, 1)
      cv2.putText(img, 'Matched ->', (15, 140), 0, 2, 255, 3, 1)

      sText = filename.split('.')
      print(f'{Fore.GREEN}Searching... in Image Number -> {Fore.WHITE}' ,sText[0] )

      if CarNumber in str(result):
         
         ## Show the car image using opencv.
         cv2.imshow('img', img)
         
         ## Show croped Plate using opencv.
         # cv2.imshow('cropedPlate', cropedPlate)

         cv2.waitKey(1)
         cv2.destroyAllWindows()

         print('Number Get.')

         car_time = '{} | {}'.format(filename, timeNow)

         num_in_car.append(car_time)
      else:
         cv2.waitKey(1)
         cv2.destroyAllWindows()
         

      

   else:
      continue
# print(' list-- ', num_in_car)

if len(num_in_car) == 0:
   print(f'{Fore.RED}No Number Found!{Fore.WHITE}')
else:
   print(f'{Fore.MAGENTA}Done.{Fore.WHITE}')
   print(f'{Fore.YELLOW}########################')
   for textN in num_in_car:
      sText = textN.split('.')
      eText = textN.split('|')
      print('Image Number -> {} | Time -> {}'.format(sText[0], eText[1]))
   print(f'########################{Fore.WHITE}')