# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:43:43 2019

@author: Srijani
"""

import _thread
import time
import RPi.GPIO as GPIO	
import xml.etree.ElementTree as ET
import socket
import time
import os
import sys
import subprocess
import shutil

#import numpy
from io import StringIO, BytesIO
from multiprocessing.pool import ThreadPool

# Define a function for corning status thread
def corning_status(*args, **kwargs):
    while True:
        server_address = ("192.168.1.80", 4460)
        command = '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><command><sensor>2_HSI</sensor><type>status</type></command>'
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #print("connecting.....")
        connected = False
        while not connected:
            try:
                s.connect(server_address)
                connected = True
            except Exception as e:
                pass #Do nothing, just try again
        
        
        s.connect(server_address)
        #print("connected")
        s.sendto(bytes(command, "ISO-8859-1"), server_address)
        resp, addr = s.recvfrom(4460)
        #print("message received")
        #print(resp.decode("ISO-8859-1"))
        root = ET.fromstring(resp)
        status = root[3].text
        #print(status)
        #time.sleep(2)
        #print("done sleeping")
        return status


def elapsed_time(start_time):
    elapsed_time = time.time() - start_time
    return elapsed_time


    

start_time = time.time()

while 1:
    status_corning = corning_status()
    time_elapsed = elapsed_time(start_time)
    total, used, free = shutil.disk_usage("/")

    print("Elapsed Time: %d"%time_elapsed)
    print("Total: %d GiB" % (total // (2**30)))
    print("Used: %d GiB" % (used // (2**30)))
    print("Free: %d GiB" % (free // (2**30)))
    if status_corning == "104":
        print("Corning status: Capturing ")
    elif status_corning == "204" or status_corning == "500":
        print("Corning status: Not capturing")
    else:
        print("Corning status: Camera off")
    if GPIO.input(18) == False:
        print("Lidar status: On and capturing")
    else:
        print("Lidar status: Off and not capturing")
        
    time.sleep(2)
        
    