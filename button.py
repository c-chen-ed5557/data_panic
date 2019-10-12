import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

switch = 18
button_counter = 0
GPIO.setup(switch, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def my_callback(channel):
    global button_counter
    button_counter += 1
    print(button_counter)

GPIO.add_event_detect(switch, GPIO.FALLING, callback=my_callback)

while True:
    time.sleep(1)
    # button_status = GPIO.input(18)
    # if GPIO.input(18) == LOW and GPIO.input(18) != button_status:
    #     GPIO.output(14, GPIO.HIGH)
    #     button_counter += 1
    #     print(button_counter)
    # if GPIO.input(18) == False:
    #     GPIO.output(14, GPIO.HIGH)
    #     button_counter += 1
    #     print(button_counter)