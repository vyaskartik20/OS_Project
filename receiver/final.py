from subprocess import Popen, STDOUT, TimeoutExpired, PIPE,getstatusoutput
from signal import SIGINT
from threading import Thread
from ewmh import EWMH
from time import sleep
import validators

# function to find file location
def location(file_name):
    status, output = getstatusoutput("locate " +file_name)
    print(output)
    return output

# def window_resize():
    

def open_processes(process_name,file_url,height,width,x,y):
    status, output = getstatusoutput("which " +process_name)
    # location of binary file of the process
    binary_location = output
    # flag to indicate wheter a url or not
    f = 0
    valid = validators.url(file_url)
    if valid:
        f = 1
    file_location = ""
    if f == 0:
        file_location = location(file_url)
    if f == 1:
        Popen([binary_location,file_url])
    else:
        Popen([binary_location,file_location])



    

open_processes("firefox","https://www.google.com/",30,40,50,50)
# open_processes("code","final.py",30,40,50,50)
