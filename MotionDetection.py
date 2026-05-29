import RPi.GPIO as GPIO
# import time
# import requests
from hx711 import HX711                # import the class HX711
from mfrc522 import SimpleMFRC522
import multiprocessing
from datetime import datetime
import pandas as pd
import numpy as np
import time
from gpiozero import Servo
from rclone_python import rclone
import os 

# Servo set up
servo = Servo(18)

# RFID set up
GPIO.setmode(GPIO.BCM)                 # set GPIO pin mode to BCM numbering
reader = SimpleMFRC522()

# Motion sensor set up
sensor = 27
GPIO.setup(sensor, GPIO.IN)

# Load cell set up 
hx = HX711(dout_pin=4, pd_sck_pin=17)
hx.zero()
ratio = 111 # kinda correct ratio is -95.4
hx.set_scale_ratio(ratio)

# initialize the date 
start_time = datetime.now().minute
# start_time = datetime.now().day

print("start_time: ", start_time)

# prepare the saving of the data
csv_df = pd.DataFrame(columns=['Date', 'id', 'Weight', 'Average Weight'])
csv_df.to_csv('ALALA_FEEDER_DATA.csv.gz', compression='gzip')
data_path = "/home/alalajssf123/Desktop/RunningJSSFPrograms/ALALA_FEEDER_DATA.csv.gz"
remote_path = "GoogleDrive:ALALA_DATA"
csv_df_len = len(csv_df)
print(csv_df_len)

index = 0
id = 0


print("Time: ",datetime.strftime(datetime.now(),"%H"))

# set the servo to starting position
servo.detach()
servo.min()
time.sleep(3)
    
def MotionDetectionMain() :
    servo.value = None
    
    while True:
        
         time.sleep(0.2)
        
        
#          servo.value = 0
    
        
        #init_time = datetime.datetime.now()
#          
#          print("init time: ",init_time,"\n")
#          print("seconds: ", int(init_time.strftime("%S")))
#          print("goal time: ", goal_time)
#          print("type of gogal time: ", type(goal_time))
#                 
#              print("time: ", datetime.now().day - start_time)
#          if datetime.now().day - start_time == 1 and int(datetime.strftime(datetime.now(),"%H")) <= 4:
#              print("time: ", datetime.now().day - start_time)
#              move_servos()
             
#          if datetime.now().minute == start_time+1 :
#              print("time: ", datetime.now().hour - start_time)
#              move_servos()


                
         if GPIO.input(27):
             print("Motion Detected")
#              getIDMain()
             loadsensorMain()
         else:
             print("No motion")

             

def loadsensorMain() :
    
    print(hx)
    hx.set_scale_ratio(ratio)
    
    prevWeight = 0
    weight = 0
    
#     Input = input("enter key")
#     time.sleep(1)
    
    for i in range (4) :
        prevWeight = weight
        weight += hx.get_weight_mean()
        
        append(datetime.now(),id, weight-prevWeight, "N/A")
        
        print(weight-prevWeight,'grams')
            
    averageWeight = weight/4
    
    print("Average Weight: ", averageWeight)
    
    append(datetime.now(),id, "N/A", averageWeight)
    save()
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
    servo.detach()
    
    for i in range(0,5) :
        print("i: ", i)
        
        print("max")
        servo.max()
        time.sleep(5)
        
        print("min")
        servo.min()
        time.sleep(5)
        
    servo.detach()
        
    
def save() :
    global csv_df_len
    global csv_df
    
    csv_df.to_csv('ALALA_FEEDER_DATA.csv.gz', compression='gzip')
    print(csv_df_len)
    
    if len(csv_df) >= csv_df_len+20 :
        csv_df_len = len(result)
        health_df = pd.DataFrame(get_pi_health())
        health_df.to_csv('RASP_HEALTH_DATA.csv.gz', mode='a', compression='gzip')
        rclone.copy("/home/alalajssf123/Desktop/RunningJSSFPrograms/RASP_HEALTH_DATA.csv.gz", remote_path)
    
    rclone.copy(data_path, remote_path)
    
#     csv_df = pd.DataFrame(columns=['Date', 'id', 'Weight', 'Average Weight'])


    
    
def get_pi_health():
    temp = os.popen("vcgencmd measure_temp").readline()
    voltage = os.popen("vcgencmd measure_volts").readline()
    throttled = os.popen("vcgencmd get_throttled").readline()
    
    data = {
        "Temperature: " : [temp.replace("temp=","").strip()],
        "Voltage: " : [voltage.replace("volt=","")],
        "Throttled: " : [throttled.replace("throttled=","")]
    }
    
    return data

def append(date, idValue, weightValue, avgValue) :
    
    csv_df.loc[len(csv_df)] = {"Date": date, "id":idValue, "Weight":weightValue, "Average Weight": avgValue}
    
if __name__ == "__main__":
    MotionDetectionMain()

