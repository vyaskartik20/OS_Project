from subprocess import Popen, STDOUT, TimeoutExpired, PIPE
from signal import SIGINT
from threading import Thread
from ewmh import EWMH
from time import sleep


def get_children(pid):
    cmd = f"ps --ppid {pid}"
    output, _ = Popen(cmd.split(" "), stdout=PIPE).communicate()
    # print(output.decode())
    return int(output.decode().split("\n")[1].split()[0])

def sudo_kill(strace_pid):
    kill_cmd = f"sudo kill {strace_pid}"
    kill_proc = Popen(kill_cmd.split(" "), stderr=STDOUT, stdout=PIPE)
    kill_out, kill_err = kill_proc.communicate()

# get open windows
window_manager = EWMH()
open_windows = window_manager.getClientList()

title_bars = []
pids = []
for window in open_windows:
    title_bars.append(window_manager.getWmName(window).decode())
    pids.append(window_manager.getWmPid(window))

# get the process names for the PIDs
process_names = []
for pid in pids:
    cmd = f"ps -p {pid}"
    pid_retrieving_proc = Popen(cmd.split(' '), stdout=PIPE)
    out, err = pid_retrieving_proc.communicate()
    process_names.append(out.decode().strip().split('\n')[1].split()[-1])

print("Process names with PIDs:")
for i, (id, name) in enumerate(zip(pids, process_names)):
    print(i, f"[{id}]", name)

# ask the usr to list processes to transfer
idx_to_transfer = input("Enter indices of the process you wish to transfer: ")

# get the PIDs to transfer
pids_to_transfer = []
for i in map(int, idx_to_transfer.split(" ")):
    pids_to_transfer.append(pids[i])

# get the open files for the PIDs

for id in pids_to_transfer:
    # first attach strace to the process
    cmd = f"sudo strace -I 1 -e trace=file -p {id} -f"
    strace_proc = Popen(cmd.split(" "), stderr=STDOUT, stdout=PIPE)
    strace_pid = strace_proc.pid
    print("Strace PID:", strace_pid)
    # wait for 5 seconds
    sleep(7)

    # kill the trace
    # obtain the child of the strace_proc 
    # because that is the one we want to kill
    strace_pid = get_children(strace_pid)
    sudo_kill(strace_pid)

    # get the output from the buffer
    out=''
    err=''
    out, err = strace_proc.communicate()
    
    # parse the trace
    out = out.decode()
    # print(out)
    # exit(1)
    for line in out.strip().split("\n")[1:]:
        if  "(" in line and ")" in line:
            line = line.split("(")[1].split(")")[0]
            if "home/devin" in line and "\"" in line:
                line = line.split(",")[0]
                print(line)


