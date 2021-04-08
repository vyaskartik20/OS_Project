# import win32gui

# def winEnumHandler( hwnd, ctx ):
#     if win32gui.IsWindowVisible( hwnd ):
#         print (hex(hwnd), win32gui.GetWindowText( hwnd ))

# win32gui.EnumWindows( winEnumHandler, None )


# import wmi
 
# # Initializing the wmi constructor
# f = wmi.WMI()
 
# # Printing the header for the later columns
# print("pid   Process name")
 
# # Iterating through all the running processes
# for process in f.Win32_Process():
     
#     # Displaying the P_ID and P_Name of the process
#     print(f"{process.ProcessId:<10} {process.Name}")

# import subprocess
# cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
# proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# for line in proc.stdout:
#     print(line)

# import subprocess
# cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
# proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# for line in proc.stdout:
#     if line.rstrip():
#         # only print lines that are not empty
#         # decode() is necessary to get rid of the binary string (b')
#         # rstrip() to remove `\r\n`
#         print(line.decode().rstrip())

import subprocess
cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,Path'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
for line in proc.stdout:
    if not line.decode()[0].isspace():
        print(line.decode().rstrip())