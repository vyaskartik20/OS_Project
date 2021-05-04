from subprocess import Popen, STDOUT, TimeoutExpired, PIPE
from signal import SIGINT
from threading import Thread
from ewmh import EWMH
from time import sleep

window_manager = EWMH()
open_windows = window_manager.getClientList()
print(open_windows)

pids = []
title_bars = []

processNames = []
for window in open_windows:
    title_bars.append(window_manager.getWmName(window).decode())
    pids.append(window_manager.getWmPid(window))
    window_manager.setMoveResizeWindow(window,0,50,50,50,50)

# get the process names for the PIDs
process_names = []
for pid in pids:
    cmd = f"ps -p {pid}"
    pid_retrieving_proc = Popen(cmd.split(' '), stdout=PIPE)
    out, err = pid_retrieving_proc.communicate()
    # print(out)
    process_names.append(out.decode().strip().split('\n')[1].split()[-1])

print("Process names with PIDs:")
for i, (id, name) in enumerate(zip(pids, process_names)):
    print(i, f"[{id}]", name)

window_manager.display.flush()