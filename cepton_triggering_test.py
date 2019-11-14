import _thread
import time
import RPi.GPIO as GPIO	
import xml.etree.ElementTree as ET
import socket
import time
import os
import sys
import subprocess
#import numpy
from io import StringIO, BytesIO
from multiprocessing.pool import ThreadPool

# Define a function for corning status thread
def corning_status(delay):
    while True:
        server_address = ("192.168.1.80", 4460)
        command = '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><command><sensor>2_HSI</sensor><type>status</type></command>'
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #print("connecting.....")
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

# Define a function for starting the capture
def start_capture(status_corning):
    print(GPIO.input(18))

    if status_corning == "104" and GPIO.input(18)== False:
#         while Tr:
#         print(j)
            GPIO.output(18,GPIO.HIGH)
            print("start capturing")
            #file_name = "testdata%s"%(j)
            global process
            process =  subprocess.Popen(['tcpdump', '-n', '-i', 'eth0', '-G', '10', '-w', '/home/pi/Downloads/test_data/capture_test/trace_%Y%m%d-%H%M%S.pcap'], stdout=subprocess.PIPE)        
            #command_line = "sudo tcpdump -n -i eth0 -G 30 -w /home/pi/Downloads/test_data/capture_test/trace_%Y%m%d-%H%M%S.pcap"
            #command_line_2 = ".pcap"
            #command_line = command_line_1+file_name+command_line_2
            #os.system (command_line)
            print("imaging started")
    elif status_corning == "104" and GPIO.input(18)== True:
        print("still imaging")
    elif status_corning == "204" and GPIO.input(18)== True:
        
        cmd = "kill -9 " + str(process.pid)
        os.system(cmd)
        print("saved pcap file")
        GPIO.output(18,GPIO.LOW)
        print("not imaging")
    elif status_corning == "500" and GPIO.input(18)== True:
        print(process.pid)
        cmd = "kill -9" + " " + str(process.pid)
        os.system(cmd)
        print("saved pcap file")
        GPIO.output(18,GPIO.LOW)
        #print("not imaging")
    else:
        print("ready")
            
        
GPIO.setmode(GPIO.BCM)	
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.LOW)
print(GPIO.input(18))

#_thread.start_new_thread( corning_status, (100,) )
pool = ThreadPool(processes=2)
async_result = pool.apply_async(corning_status, (100,) )
status_corning = async_result.get()
while True:   
   status_corning = corning_status(100)
   print(status_corning)
   start_capture(status_corning)
   time.sleep(2)

# except:
# print( "Error: unable to start thread")

# while True:
# pass




