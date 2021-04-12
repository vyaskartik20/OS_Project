import subprocess
import os
import sys

# status stores success
# use whereis command to locate the process 
# output stores the location of process installed
status, output = subprocess.getstatusoutput("whereis " +sys.argv[1])
print(output)

#spliiting output to get process location
s = output.split(' ')

# print(s[1])

# opening file or url in process
subprocess.Popen([s[1],sys.argv[2]])
# use whereis command to locate the process
# s = os.system("whereis " +sys.argv[1])


# opening a process
# subprocess.Popen(["/usr/bin/libreoffice","presentation2.pptx"])
# subprocess.Popen(["/snap/bin/code","1.py"])
# opening a url in new chrome window
# subprocess.Popen(["/usr/bin/google-chrome", "https://github.com/vyaskartik20/OS_Project"])
