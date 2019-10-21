import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# setup the blue light
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
# setup the yellow light
GPIO.setup(4, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
# setup the red light
GPIO.setup(6, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
# setup the green light
GPIO.setup(8, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)

def blue_on():
    GPIO.output(2, GPIO.HIGH)
    GPIO.output(3, GPIO.HIGH)

def blue_off():
    GPIO.output(2, GPIO.LOW)
    GPIO.output(3, GPIO.LOW)

def yellow_on():
    GPIO.output(4, GPIO.HIGH)
    GPIO.output(5, GPIO.HIGH)

def yellow_off():
    GPIO.output(4, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)

def red_on():
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(7, GPIO.HIGH)
#
def red_off():
    GPIO.output(6, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)

def green_on():
    GPIO.output(8, GPIO.HIGH)
    GPIO.output(9, GPIO.HIGH)

def green_off():
    GPIO.output(8, GPIO.LOW)
    GPIO.output(9, GPIO.LOW)


#
# def green_on():
#     GPIO.output(5, GPIO.HIGH)
#
# def green_off():
#     GPIO.output(5, GPIO.LOW)

def all_on():
    GPIO.output(2, GPIO.HIGH)
    GPIO.output(3, GPIO.HIGH)
    GPIO.output(4, GPIO.HIGH)
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(7, GPIO.HIGH)
    GPIO.output(8, GPIO.HIGH)
    GPIO.output(9, GPIO.HIGH)

def all_off():
    GPIO.output(2, GPIO.LOW)
    GPIO.output(3, GPIO.LOW)
    GPIO.output(4, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(8, GPIO.LOW)
    GPIO.output(9, GPIO.LOW)