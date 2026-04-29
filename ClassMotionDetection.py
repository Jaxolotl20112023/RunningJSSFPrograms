import RPi.GPIO as GPIO
import time
import requests
from hx711 import HX711                # import the class HX711
from mfrc522 import SimpleMFRC522
import multiprocessing
import datetime
import pandas as pd
import numpy as np
import time

# setting the GPIO mode
GPIO.setmode(GPIO.BCM)                 # set GPIO pin mode to BCM numbering

# gets the reader for the RFID
reader = SimpleMFRC522()

# this sets up the Motion Sensor 
sensor = 27 # GPIO pin # the sensor data is put in       
GPIO.setup(sensor, GPIO.IN) # setting the GPIO to get information from the sensor

# sets up the load cell 
hx = HX711(dout_pin=4, pd_sck_pin=17) # get and set the GPIO pins that'll receive and give out info 
hx.zero() # zero out the scale 
ratio = 105.53  
hx.set_scale_ratio(ratio) # set the scale's ratio

# init_time = datetime.datetime.now()
# start_time = int(init_time.strftime("%S"))
# goal_time = start_time + 5
# print("goal time: ", goal_time)

# creates the Pandas Dataframe that'll store the id, weight, and average weight
csv_df = pd.DataFrame(columns=['id', 'Weight', 'Average Weight'])

# index = 0
id = 0

class motionDetector() :

  def __init__(pin) : 
    self.pin = pin 
    GPIO.setup(self.pin, GPIO.IN) # setting the GPIO to get information from the sensor

  def detection() : 
    while True:
        # checks if there has been any movement by the motion sensor
        if GPIO.input(self.pin) :
            print("Motion Detected")
            return 
        else:
            print("No motion")

class loadSensor() : 

    def __init__(dout, sdk) :
        self.dout = dout
        self.sdk = sdk 

        self.hx = HX711(dout_pin=self.dout, pd_sck_pin=self.sdk) # get and set the GPIO pins that'll receive and give out info 
        self.hx.zero() # zero out the scale 
        ratio = 105.53  
        self.hx.set_scale_ratio(ratio) # set the scale's ratio

    def measure(self) : 
        dout = self.dout
        sdk = self.sdk 
        hx  = self.hx

        prevWeight = 0
        weight = 0
        
        Input = input("enter key")
    #     time.sleep(1)
    
        # displays the current weight while calculating the average weight of a sample of 4
        for i in range (4) :
            prevWeight = weight
            weight += hx.get_weight_mean()
            
            append(id, weight-prevWeight, "N/A") # saves these values into the dataframe
            
            print(weight-prevWeight,'grams')
                
        averageWeight = weight/4
        
        print("Average Weight: ", averageWeight) # print out the average weight
        
        append(id, "N/A", averageWeight) # save the average weight to the dataframe
        
        csv_df.to_csv('ALALA_FEEDER_DATA.csv') # save the data collected into a csv file 
         # return to the main looping function
class rFID() : 

     def __init__():
         self.reader = SimpleMFRC522() 

     def search():
          p = multiprocessing.Process(target=self.readCard)
          p.start()
          p.join(5) # sets the 5 second timer for the function
      
          # if it is still running after 5 seconds it terminates and goes back to looking for motion
          if p.is_alive() :
              p.terminate()
              p.join
              print("NO IDS DETECTED")
              return False
          else : # if not, then it will check weight
              p.join
              return True

     def readCard(self):
          print('Place Card on Reader')
          id,text = self.reader.read()
              
          print('ID: ', id)
      

class servos():

     def __init__(pin, angle) :
          self.pin = pin
          self.angle = angle 

     def move(self) : 
          pin = self.pin
          angle = self.angle
       
          GPIO.cleanup()
          GPIO.setmode(GPIO.BOARD)
          GPIO.setup(pin, GPIO.OUT)
          
          pwm1 = GPIO.PWM(pin, 50)
          
          pwm1.start(2.1)
      
          duty1 = angle / 18 + 2
          print(duty1)
              
          pwm1.ChangeDutyCycle(duty1)

mD = motionDetector(27)
RFID = rFID()
ls = loadSensor(4,17)


mD.detection()
if RFID.search() : 
  ls.measure()
  mD.detection()
else : 
  mD.detection()

    
def append(idValue, weightValue, avgValue) :
    
    csv_df.loc[len(csv_df)] = {"id":idValue, "Weight":weightValue, "Average Weight": avgValue}
    
if __name__ == "__main__":
    MotionDetectionMain()
