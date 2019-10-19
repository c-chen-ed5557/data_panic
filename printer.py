import serial
import adafruit_thermal_printer
from api import request_tweets, request_news, request_quotes
import random

uart = serial.Serial('/dev/serial0', baudrate=9600, timeout=3000)
ThermalPrinter=adafruit_thermal_printer.get_printer_class(1.11)
printer = ThermalPrinter(uart)

# def print_tweets():
#    printer.bold = True
#    printer.print('A tweet')
#    printer.bold = False
#    printer.feed(2)
#    printer.print(request_tweets())
def random_texts():
    texts_list = [print_quotes, print_news, print_tweets]
    texts_list[int(random.random()*3)]()

def print_quotes():
    data = request_quotes()
    printer.print(data['quote'])
    printer.feed(2)
    printer.print('by: ' + data['by'])
    printer.feed(4)

def print_news():
    data = request_news()
    print(data['content'])
    printer.print('Title: ' + str(data['title']))
    printer.feed(2)
    printer.print('Author: ' + str(data['author']))
    printer.feed(2)
    # printer.print('Content: ' + str(data['content']))
    # printer.feed(2)
    
    if data['content'] == None:
        printer.print("Opps! It seems we did not find anything. What a pity.")
        printer.feed(4)
    else:
        printer.print('Content: ' + str(data['content']))
        printer.feed(4)

def print_tweets():
    data = request_tweets()
    printer.print(str(data['username']) + ' says:')
    printer.feed(1)
    printer.print(str(data['content']))
    printer.feed(4)
