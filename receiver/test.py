import subprocess
import os
import sys
import validators

# status stores success
# use whereis command to locate the process 
# output stores the location of process installed
status, output = subprocess.getstatusoutput("whereis " +sys.argv[1])
#checking whether process exists or not
if status !=0:
    print("process not found")
    exit()

# print(output)

#spliiting output to get process location
s = output.split(' ')

# print(s[1])

#checking whether string is url or not
url = 0

valid = validators.url(sys.argv[2])

if valid:
    url = 1

# print(url)

# opening file or url in process
subprocess.Popen([s[1],sys.argv[2]])

# use whereis command to locate the process
# s = os.system("whereis " +sys.argv[1])

#use find to locate a file

# opening a process
subprocess.Popen(["/usr/bin/libreoffice","/home/aditya/Downloads/presentation2.pptx"])
# subprocess.Popen(["/snap/bin/code","1.py"])
# opening a url in new chrome window
# subprocess.Popen(["/usr/bin/google-chrome", "https://github.com/vyaskartik20/OS_Project"])
# subprocess.Popen(["/opt/google/chrome/chrome", "https://github.com/vyaskartik20/OS_Project"])


# command to get binary location of any process using process id
# https://askubuntu.com/questions/49024/how-do-i-determine-the-path-to-a-binary-of-a-process
# https://stackoverflow.com/questions/606041/how-do-i-get-the-path-of-a-process-in-unix-linux#:~:text=11%20Answers&text=On%20Linux%2C%20the%20symlink%20%2Fproc,exe%20to%20get%20the%20value.