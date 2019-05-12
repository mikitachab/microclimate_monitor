
###nitors GPIO pin 40 for input. A sound module is set up on physical pin 40.
#https://pinout.xyz/pinout/wiringpi#
import RPi.GPIO as GPIO
import time
import datetime
import os

SOUND_PIN = 24
def DETECTED(SOUND_PIN):
    global loud_detect_count
    loud_detect_count+=1
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_PIN, GPIO.IN)
GPIO.add_event_detect(SOUND_PIN, GPIO.BOTH)
GPIO.add_event_callback(SOUND_PIN,callback=DETECTED) 
 
loud_detect_count = 0


   


def get_sound():
    loud_detect_count = 0
    time.sleep(2)
    if loud_detect_count > 10:
        return True
    else: 
        return  False
