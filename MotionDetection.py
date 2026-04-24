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

GPIO.setmode(GPIO.BCM)                 # set GPIO pin mode to BCM numbering
reader = SimpleMFRC522()

sensor = 27
GPIO.setup(sensor, GPIO.IN)

hx = HX711(dout_pin=4, pd_sck_pin=17)
hx.zero()
ratio = 105.53 # kinda correct ratio is -95.4
hx.set_scale_ratio(ratio)

init_time = datetime.datetime.now()
start_time = int(init_time.strftime("%S"))
goal_time = start_time + 5
print("goal time: ", goal_time)

csv_df = pd.DataFrame(columns=['id', 'Weight', 'Average Weight'])
index = 0
id = 0

    
def MotionDetectionMain() :
#     move_servos(16,90)
#     move_servos(18,90)
#     
#     GPIO.cleanup()
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(sensor, GPIO.IN)
    
    while True:
        
        #init_time = datetime.datetime.now()
#          
#          print("init time: ",init_time,"\n")
#          print("seconds: ", int(init_time.strftime("%S")))
#          print("goal time: ", goal_time)
#          print("type of goal time: ", type(goal_time))
#                 
         try : 
             if int(init_time.strftime("%S")) == goal_time :
                 move_servos(16, 90)
#                  start_time = int(init_time.strftime("%S"))
#                  goal_time = start_time + 12
         except:
             print("error with moving servos")

                
         if GPIO.input(27) :
             print("Motion Detected")
             getIDMain()
         else:
             print("No motion")

             

def loadsensorMain() :
    
    print(hx)
    hx.set_scale_ratio(105.53)
    
    prevWeight = 0
    weight = 0
    
    Input = input("enter key")
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
    
def move_servos(pin, angle) :
    
    # calculate and set up the first servo
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    
    pwm1 = GPIO.PWM(pin, 50)
    
    pwm1.start(2.1)

    duty1 = angle / 18 + 2
    print(duty1)
        
    pwm1.ChangeDutyCycle(duty1)
    
    # calculate and set up the second servo
    #GPIO.setup(18, GPIO.OUT)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             )
    #pwm2 = GPIO.PWM(18,50)
    #duty2 = angle / 18 + 2
    
    #GPIO.output(18, True)
    #pwm2.ChangeDutyCycle(duty2)
    
def append(idValue, weightValue, avgValue) :
    
    csv_df.loc[len(csv_df)] = {"id":idValue, "Weight":weightValue, "Average Weight": avgValue}
    
if __name__ == "__main__":
    MotionDetectionMain()
