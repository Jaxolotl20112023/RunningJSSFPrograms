import RPi.GPIO as GPIO
import time
import requests
from hx711 import HX711                # import the class HX711
from mfrc522 import SimpleMFRC522
import multiprocessing
from datetime import datetime
import pandas as pd
import numpy as np
import time
from gpiozero import Servo

servo = Servo(18)
        
GPIO.setmode(GPIO.BCM)                 # set GPIO pin mode to BCM numbering
reader = SimpleMFRC522()

sensor = 27
GPIO.setup(sensor, GPIO.IN)

hx = HX711(dout_pin=4, pd_sck_pin=17)
hx.zero()
ratio = 110.1 # kinda correct ratio is -95.4
hx.set_scale_ratio(ratio)

start_time = datetime.now().minute

print("start_time: ", start_time)

csv_df = pd.DataFrame(columns=['id', 'Weight', 'Average Weight'])
index = 0
id = 0

servo.detach()
    
def MotionDetectionMain() :
#     move_servos(16,90)
#     move_servos(18,90)
#     
#     GPIO.cleanup()
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(sensor, GPIO.IN)
    
    while True:
        
#          servo.value = 0
    
        
        #init_time = datetime.datetime.now()
#          
#          print("init time: ",init_time,"\n")
#          print("seconds: ", int(init_time.strftime("%S")))
#          print("goal time: ", goal_time)
#          print("type of goal time: ", type(goal_time))
#                 
#              print("time: ", datetime.now().day - start_time)
         if datetime.now().minute - start_time == 1:
             print("time: ", datetime.now().minute - start_time)
             move_servos()


                
         if GPIO.input(27):
             print("Motion Detected")
#              getIDMain()
             loadsensorMain()
         else:
             print("No motion")

             

def loadsensorMain() :
    
    print(hx)
    hx.set_scale_ratio(105.53)
    
    prevWeight = 0
    weight = 0
    
#     Input = input("enter key")
#     time.sleep(1)
    
    for i in range (4) :
        prevWeight = weight
        weight += hx.get_weight_mean()
        
        append(id, weight-prevWeight, "N/A")
        
        print(weight-prevWeight,'grams')
            
    averageWeight = weight/4
    
    print("Average Weight: ", averageWeight)
    
    append(id, "N/A", averageWeight)
    
    csv_df.to_csv('ALALA_FEEDER_DATA.csv')
    MotionDetectionMain()
    
def getIDMain ():
    
    p = multiprocessing.Process(target=readCard)
    p.start()
    p.join(5)

    if p.is_alive() :
        p.terminate()
        p.join
        print("NO IDS DETECTED")
        MotionDetectionMain()
    else :
        loadsensorMain()
        p.join

def readCard (): 
    
    print('Place Card on Reader')
    id,text = reader.read()
        
    print('ID: ', id)
    
def move_servos() :
    start_time = datetime.now().minute
    
    for i in range(0,5) :
        print("i: ", i)
        
        servo.min()
        time.sleep(5)
    
        servo.max()
        time.sleep(5)
        
    servo.detach()
        
    
def append(idValue, weightValue, avgValue) :
    
    csv_df.loc[len(csv_df)] = {"id":idValue, "Weight":weightValue, "Average Weight": avgValue}
    
if __name__ == "__main__":
    MotionDetectionMain()

