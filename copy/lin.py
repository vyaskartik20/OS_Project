#!/usr/bin/python



# from dragonfly import Window
# listt = Window.get_all_windows()

# print(listt)

# pgrep -af python #CL

#     """
#     Return status of process based on process name.
#     """
# import psutil

# def check_process_status(process_name):
#     process_status = [ proc for proc in psutil.process_iter() if proc.name() == process_name ]
#     if process_status:
#         for current_process in process_status:
#             print("Process id is %s, name is %s, staus is %s"%(current_process.pid, current_process.name(), current_process.status()))
#     else:
#         print("Process name not valid", process_name)

# # def main():
# check_process_status("chrome")



# import subprocess
# cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
# proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# for line in proc.stdout:
#     if line.rstrip():
#         # only print lines that are not empty
#         # decode() is necessary to get rid of the binary string (b')
#         # rstrip() to remove `\r\n`
#         print(line.decode().rstrip())


# import subprocess
# cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,Path'
# proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# for line in proc.stdout:
#     if not line.decode()[0].isspace():
#         print(line.decode().rstrip())



# void CSoftwareInfoLinux::enumerateWindows(Display *display, Window rootWindow)
# {
#     Window parent;
#     Window *children;
#     Window *child;
#     quint32 nNumChildren;

#     XTextProperty wmName;
#     XTextProperty wmCommand;

#     int status = XGetWMName(display, rootWindow, &wmName);
#     if (status && wmName.value && wmName.nitems)
#     {
#         int i;
#         char **list;
#         status = XmbTextPropertyToTextList(display, &wmName, &list, &i);
#         if (status >= Success && i && *list)
#         {
#             qDebug() << "Found window with name:" << (char*) *list;
#         }

#         status = XGetCommand(display, rootWindow, &list, &i);
#         if (status >= Success && i && *list)
#         {
#             qDebug() << "... and Command:" << i << (char*) *list;
#         }

#         Window tf;
#         status = XGetTransientForHint(display, rootWindow, &tf);
#         if (status >= Success && tf)
#         {
#             qDebug() << "TF set!";
#         }

#         XWMHints *pHints = XGetWMHints(display, rootWindow);
#         if (pHints)
#         {
#             qDebug() << "Flags:" << pHints->flags
#                     << "Window group:" << pHints->window_group;
#         }
#     }

#     status = XQueryTree(display, rootWindow, &rootWindow, &parent, &children, &nNumChildren);
#     if (status == 0)
#     {
#         // Could not query window tree further, aborting
#         return;
#     }

#     if (nNumChildren == 0)
#     {
#         // No more children found. Aborting
#         return;
#     }

#     for (int i = 0; i < nNumChildren; i++)
#     {
#         enumerateWindows(display, children[i]);
#     }

#     XFree((char*) children);
# }

# # def main():
# enumerateWindows()




# Atom a = XInternAtom(m_pDisplay, "_NET_CLIENT_LIST" , true);
# Atom actualType;
# int format;
# unsigned long numItems, bytesAfter;
# unsigned char *data =0;
# int status = XGetWindowProperty(m_pDisplay,
#                             rootWindow,
#                             a,
#                             0L,
#                             (~0L),
#                             false,
#                             AnyPropertyType,
#                             &actualType,
#                             &format,
#                             &numItems,
#                             &bytesAfter,
#                             &data);

# if (status >= Success && numItems)
# {
#     // success - we have data: Format should always be 32:
#     Q_ASSERT(format == 32);
#     // cast to proper format, and iterate through values:
#     quint32 *array = (quint32*) data;
#     for (quint32 k = 0; k < numItems; k++)
#     {
#         // get window Id:
#         Window w = (Window) array[k];

#         qDebug() << "Scanned client window:" << w;
#     }
#     XFree(data);
# }



#######################3
'''
gives list of processes [only names] from title bar
'''
# from ewmh import EWMH

# window_manager_manager = EWMH()
# client_list = window_manager_manager.getClientList()

# for window in client_list:
#     print(window_manager_manager.getWmName(window))


########

'''
gives list of processes [only names] from title bar
'''
# from Xlib.display import Display
# from Xlib.X import AnyPropertyType

# display = Display()
# root = display.screen().root

# _NET_CLIENT_LIST = display.get_atom('_NET_CLIENT_LIST')
# _NET_WM_NAME = display.get_atom('_NET_WM_NAME')

# client_list = root.get_full_property(
#     _NET_CLIENT_LIST,
#     property_type=AnyPropertyType,
# ).value

# for window_id in client_list:
#     window = display.create_resource_object('window', window_id)
#     window_name = window.get_full_property(
#         _NET_WM_NAME,
#         property_type=AnyPropertyType,
#     ).value
#     print(window_name)


############


'''
gives geometry [dimnesions and coordinates] of current window already 
'''
# import gi
# gi.require_version('Wnck', '3.0')
# from gi.repository import Wnck
# screen = Wnck.Screen.get_default()
# screen.force_update()  # recommended per Wnck documentation

# # loop all windows
# for window in screen.get_windows():
#    if window.is_active() == True:
#         print (window.get_geometry())
#         window_name = window.get_name()
#         print (window_name)

# # clean up Wnck (saves resources, check documentation)
# window = None
# screen = None
# Wnck.shutdown()


############

#!/usr/bin/python
'''
gives geometry [dimnesions and coordinates] of all open windows already 
'''

# import gi
# gi.require_version('Wnck', '3.0')
# from gi.repository import Wnck
# screen = Wnck.Screen.get_default()
# screen.force_update()  # recommended per Wnck documentation

# # loop all windows
# for window in screen.get_windows():
# #    if window.is_active() == True:
#     print (window.get_geometry())
#     window_name = window.get_name()
#     print (window_name)

# # clean up Wnck (saves resources, check documentation)
# window = None
# screen = None
# Wnck.shutdown()

############

'''
windows only
'''

# import pygtk
# pygtk.require('2.0')
# import gtk


# lis = gtk.gdk.window_get_toplevels()
# print(lis)

###########3
'''
processes and their children
'''
# $ xwininfo -tree -root
########
'''
gives window IDs
'''
# xprop -root|grep ^_NET_CLIENT_LIST
#########
'''
gives geometry of windows, inspected by Window ID
'''
# xwininfo -id 0x2000007



############3
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver
# driver = webdriver.Chrome(executable_path="/home/vyas20/Downloads/chromedriver_linux64/chromedriver")
# # driver = webdriver.Chrome(ChromeDriverManager().install())
# # to maximize the browser window
# driver.maximize_window()
# #get method to launch the URL
# driver.get("https://the-internet.herokuapp.com/windows")
# #to refresh the browser
# driver.refresh()
# driver.find_element_by_link_text("Click Here").click()
# #prints the window handle in focus
# print(driver.current_window_handle)
# #to fetch the first child window handle
# chwnd = driver.window_handles[1]
# #to switch focus the first child window handle
# driver.switch_to.window(chwnd)
# print(driver.find_element_by_tag_name("h3").text)
# #to close the browser
#########



# import selenium
# from selenium import webdriver
# # import configreader
# # from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(executable_path="/home/vyas20/Downloads/chromedriver_linux64/chromedriver")

# # # options = webdriver.ChromeOptions()
# # driver = webdriver.Chrome(ChromeDriverManager().install())

# # lis = driver.get_all_windows()

# # for i in lis :
# #     driver.switch_to(i)
# #     tit = driver.current_url()
# #     print(tit)

# for handle in driver.window_handles:
#     print('ues')
#     driver.switch_to.window(handle)
#     print(driver.current_url)

# browser = webdriver.Chrome()

# tabs = driver.window_handles() 
# print(tabs)

# driver=webdriver.Chrome()
# print(driver.current_url)
# driver.quit()