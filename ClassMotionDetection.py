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
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder,Quality
from picamera2.outputs import FileOutput
from picamera2.outputs import FfmpegOutput
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


GPIO.setmode(GPIO.BCM)

class Camera() :
    
    def __init__(self) :
        self.picam = Picamera2()
        self.video = None
        self.config = self.picam.create_video_configuration()
        self.picam.configure(self.config)

        self.encoder = H264Encoder(bitrate=10000000)
        
        self.record_num = 0
        self.output = None
        self.name = None
        
        self.capture_start = None
        self.capture_end = None
        self.start = None
        self.is_recording = False
        
    def start_preview(self):
        self.picam.start_preview()
    
    def end_preview(self):
        self.picam.stop_preview()
        self.picam.close()
        
    def start_record(self) :
        self.capture_start = None
        self.name = "vid",record_num,".h264"
        self.output = FileOutput(self.name)
        self.picam.start_recording(encoder, output, quality=Quality.HIGH)
        self.start = (datetime.now().hour*60*60) + (datetime.now().minute*60)
        self.is_recording = True
        
    def end_record(self) :
        self.capture_end = None
        self.picam.stop_recording()
        self.record_num+=1
        self.is_recording = False
        self.set_capture_end()
        
    def set_capture_start(self):
        self.capture_start = (datetime.now().hour*60*60) + (datetime.now().minute*60 - 60) - self.start
        
    def set_capture_end(self):
        self.capture_end = (datetime.now().hour*60*60) + (datetime.now().minute*60) - self.capture_start
        
class load_cell() : 

    def __init__(self,dout,sck,ratio,file_name) : 
        self.dout = dout
        self.sck = sck
        self.ratio = ratio
        self.file_name = file_name
        self.hx = HX711(dout_pin=self.dout, pd_sck_pin=self.sck) 
        self.hx.zero() 
        self.hx.set_scale_ratio(ratio) 

        self.csv_df = pd.DataFrame(columns=['Date', 'id', 'Weight', 'Average Weight'])
        self.csv_df.to_csv(f'{file_name}_{datetime.now().month}-{datetime.now().day}-{datetime.now().year}.csv.gz', compression='gzip')
        self.data_path = f"/home/alalajssf123/Desktop/RunningJSSFPrograms/{file_name}_{datetime.now().month}-{datetime.now().day}-{datetime.now().year}.csv.gz"
        self.df_csv_len = len(self.csv_df)

    def activate(self) : 
#         GPIO.output(self.dout,GPIO.HIGH)
#         GPIO.output(self.sck, GPIO.HIGH) 
#         GPIO.cleanup()

        hx = self.hx
        file_name = self.file_name

        print(hx)
        
        prevWeight = 0
        weight = 0
        
        for i in range (4) :
            prevWeight = weight
            weight += hx.get_weight_mean()
            
            append(self.csv_df,rfid1.id, weight-prevWeight, "N/A")
            
            print(weight-prevWeight,'grams')
                
        averageWeight = weight/4
        
        print("Average Weight: ", averageWeight)

        append(self.csv_df,rfid1.id, "N/A", averageWeight)
        save(self)
        #MotionDetectionMain()
        rfid1.getIDMain()
        
    def deactivate(self) : 
        GPIO.output(self.dout,GPIO.LOW)
        GPIO.output(self.sck, GPIO.LOW) 
        GPIO.cleanup()

    def change_files(self) : 

        os.remove(self.data_path)

        self.csv_df = pd.DataFrame(columns=['Date', 'id', 'Weight', 'Average Weight'])
        self.csv_df.to_csv(f'{self.file_name}_{datetime.now().month}-{datetime.now().day}-{datetime.now().year}.csv.gz', compression='gzip')
        self.data_path = f"/home/alalajssf123/Desktop/RunningJSSFPrograms/{self.file_name}_{datetime.now().month}-{datetime.now().day}-{datetime.now().year}.csv.gz"

    def convert_to_csv(self) : 
        self.csv_df.to_csv(f'{self.file_name}_{datetime.now().month}-{datetime.now().day}-{datetime.now().year}.csv.gz', compression='gzip')
        
        
class rfid() : 

    def __init__(self) : 
        GPIO.setmode(GPIO.BCM)                
        self.reader = SimpleMFRC522()
        self.id = None

    def getIDMain (self):
    
        p = multiprocessing.Process(target=self.readCard)
        p.start()
        p.join(5)

        if p.is_alive() :
            p.terminate()
            p.join
            print("NO IDS DETECTED")
             
            if cam1.capture_start != None:
                cam1.end_record()
                ffmpeg_extract_subclip(f"{cam1.name}.mp4", cam1.capture_start, cam1.capture_end, outputfile=f"{cam1.name}f")
                cam1.capture_start = None 
                cam1.capture_end = None

            MotionDetectionMain()
        else :
                
            if cam1.capture_start == None:
                cam1.set_capture_start()
            
            bird_cell.activate()
            p.join

    def readCard (self): 

        reader = self.reader
        
        print('Place Card on Reader')
        self.id,text = reader.read()

        print('ID: ', self.id)

class servo() : 

    def __init__(self, pin) :
        self.pin = pin 
        self.servo = Servo(self.pin);
        
        self.servo.detach()
        self.servo.min()
        time.sleep(3)
        
    def move_servos(self) :
        global start_time
        servoc = self.servo

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
    
    def reset_servo(self) :
        self.servo.value = None

# Servo set up
servo1 = servo(18)

# Camera set up
cam1 = Camera()

# Motion sensor set up
sensor = 27
GPIO.setup(sensor, GPIO.IN)

# RFID set up 
rfid1 = rfid() 

# Load cell set up 
ratio = 111 # kinda correct ratio is -95.4
bird_cell = load_cell(4,17,ratio,"ALALA_BIRD_DATA")
# feeder_cell = load_cell(0,0,ratio,"ALALA_FEEDER_DATA")

# initialize the date 
# start_time = datetime.now().minute
start_time = datetime.now().day

print("start_time: ", start_time)

# prepare the saving of the data
remote_path = "GoogleDrive:ALALA_DATA/Alala_Bird_Weight"
df_bird_cell_len = len(bird_cell.csv_df)
print(df_bird_cell_len)

index = 0

print("Time: ",datetime.strftime(datetime.now(),"%H"))

# set the servo to starting position
# servo.detach()
# servo.min()
# time.sleep(3)
    
def MotionDetectionMain() :
    servo1.reset_servo()
    
    while True:
        
         
         if not cam1.is_recording :
            cam1.start_record()
             
        
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
         if datetime.now().day - start_time >= 1 and int(datetime.strftime(datetime.now(),"%H")) <= 4:
             print("time: ", datetime.now().day - start_time)
             servo1.move_servos()
#              feeder_cell.activate()

             bird_cell.change_files()
#              feeder_cell.change_files()
             
#          if datetime.now().minute == start_time+1 :
#              print("time: ", datetime.now().hour - start_time)
#              move_servos()


                
         if GPIO.input(27):
             print("Motion Detected")
             rfid1.getIDMain()
             #bird_cell.activate()
#              rfid1.getIDMain()
         else:
             print("No motion")

        
    
def save(df) :
    
    df.convert_to_csv()
    print(df.df_csv_len)
    
    if len(df.csv_df) >= df.df_csv_len+10 :
        df.df_csv_len = len(df.csv_df)
        health_df = pd.DataFrame(get_pi_health())
        health_df.to_csv('RASP_HEALTH_DATA.csv.gz', compression='gzip')
        rclone.copy("/home/alalajssf123/Desktop/RunningJSSFPrograms/RASP_HEALTH_DATA.csv.gz", "GoogleDrive:ALALA_DATA/Pi_Health")
    
    rclone.copy(df.data_path, remote_path)
    
def get_pi_health():
    temp = os.popen("vcgencmd measure_temp").readline()
    voltage = os.popen("vcgencmd measure_volts").readline()
    throttled = os.popen("vcgencmd get_throttled").readline()
    
    temp = temp.replace("temp=","").strip()
    temp = temp.replace("'C","").strip()
    voltage = voltage.replace("V","").strip()
    
    data = {
        "Temperature: " : [temp.replace("temp=","").strip()],
        "Voltage: " : [voltage.replace("volt=","").strip()],
        "Throttled: " : [throttled.replace("throttled=","").strip()]
    }
    
    return data

def append(df, idValue, weightValue, avgValue) :
    
    df.loc[len(df)] = {"Date": f"{datetime.now().month}-{datetime.now().day}-{datetime.now().year}", "id":idValue, "Weight":weightValue, "Average Weight": avgValue}
    
if __name__ == "__main__":
    MotionDetectionMain()
