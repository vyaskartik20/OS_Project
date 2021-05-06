from subprocess import Popen, STDOUT, TimeoutExpired, PIPE,getstatusoutput
from signal import SIGINT
from threading import Thread
from ewmh import EWMH
from time import sleep
import validators
import json



def open_processes(process_name,file_url):
    status, output = getstatusoutput("which " +process_name)
    # location of binary file of the process
    binary_location = output
    # opening a sub process
    Popen([binary_location,file_url])

f = open('transfer2.json')
data = json.load(f)
for pno, pinfo in data.items():
    print("\nProcess No:", pno)
    
    # print(pinfo['process'],pinfo['file'])
    open_processes(pinfo['process'],pinfo['file'])