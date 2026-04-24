import RPi.GPIO as GPIO                # import GPIO
from hx711 import HX711                # import the class HX711

GPIO.setmode(GPIO.BCM)                 # set GPIO pin mode to BCM numbering
hx = HX711(dout_pin=4, pd_sck_pin=17)
hx.zero()


target = 100
ratio = 95.03 # kinda correct ratio is -95.4

hx.set_scale_ratio(ratio)

actualWeight = hx.get_weight_mean()

Input = input("START CALIBRATION: PRESS ENTER")

while round(actualWeight) != target :
    if actualWeight < target : ratio -= 0.5
    else : ratio += 0.5

    hx.set_scale_ratio(ratio)

    actualWeight = hx.get_weight_mean()
    print(ratio," | ",actualWeight)