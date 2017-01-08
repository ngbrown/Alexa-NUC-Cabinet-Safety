#! /usr/bin/env python
from PyMata.pymata import PyMata

import subprocess
import os
import random
import time
import alsaaudio
import wave
import random
from creds import *
import requests
import json
import re
from memcache import Client

# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

myMQTTClient = AWSIoTMQTTClient("arn:aws:iot:us-east-1:194337674115:thing/NUC-Gateway")
myMQTTClient.configureEndpoint("a1am3uuthfk12b.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("root-CA.crt", "NUC-Gateway.private.key", "NUC-Gateway.cert.pem")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.connect()

Button = 8
LED_Status = 3
LED_Record = 4
blue_led = 5;
red_led = 6;

board = PyMata("/dev/ttyACM0", verbose=True)

board.set_pin_mode(LED_Status, board.OUTPUT, board.DIGITAL)
board.set_pin_mode(LED_Record, board.OUTPUT, board.DIGITAL)
board.set_pin_mode(Button, board.INPUT, board.DIGITAL)

def customCallback(client, userdata, message):
    print("Received a new message: ")
    parsed_json = json.loads(message.payload)
    blue_led_state = parsed_json["state"]["desired"]["blue_led"]
    red_led_state = parsed_json["state"]["desired"]["red_led"]
    print(blue_led_state)
    print(red_led_state)
    board.digital_write(blue_led, blue_led_state)
    board.digital_write(red_led, red_led_state)

#Setup
recorded = False
servers = ["127.0.0.1:11211"]
mc = Client(servers, debug=1)
path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))

def internet_on():
    print "Checking Internet Connection"
    try:
        r =requests.get('https://api.amazon.com/auth/o2/token')
        print "Connection OK"
        return True
    except:
        print "Connection Failed"
        return False

def start():
    recording = 0
    last = 0
    while True:
        val =  board.digital_read(Button)
        time.sleep(.01)


if __name__ == "__main__":

    board.digital_write(LED_Status, 0)
    board.digital_write(LED_Record, 0)
    myMQTTClient.subscribe("$aws/things/NUC-Gateway/shadow/update/accepted", 1, customCallback)

    while internet_on() == False:
        print "."
    for x in range(0, 3):
        time.sleep(.1)
        board.digital_write(LED_Status, 1)
        time.sleep(.1)
        board.digital_write(LED_Status, 0)
    start()
