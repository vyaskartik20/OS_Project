import json
import os
from signal import SIGINT
from subprocess import PIPE, STDOUT, Popen, TimeoutExpired
from threading import Thread
from time import sleep

from ewmh import EWMH


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
    pid_retrieving_proc = Popen(cmd.split(" "), stdout=PIPE)
    out, err = pid_retrieving_proc.communicate()
    process_names.append(out.decode().strip().split("\n")[1].split()[-1])

print("Process names with PIDs:")
for i, (id, name) in enumerate(zip(pids, process_names)):
    print(f"[{i}]: {name}, {id}")

# ask the usr to list processes to transfer
idx_to_transfer = input("Enter indices of the process you wish to transfer: ")
idx_to_transfer = map(int, idx_to_transfer.split())

# get the PIDs to transfer
pids_to_transfer = []
processes_to_transfer = []
for i in idx_to_transfer:
    # print(i)
    pids_to_transfer.append(pids[i])
    processes_to_transfer.append(process_names[i])

# user_name = "devin"

result = {}
# get the open files for the PIDs
for i1, (id, name) in enumerate(zip(pids_to_transfer, processes_to_transfer)):
    # first attach strace to the process
    cmd = f"sudo strace -I 1 -e trace=file,open,close,write -p {id} -f"
    strace_proc = Popen(cmd.split(" "), stderr=STDOUT, stdout=PIPE)
    strace_pid = strace_proc.pid
    print("Strace PID:", strace_pid)

    # wait for some time
    print(f"Go to {name} and save your work")
    sleep(10)

    # kill the trace
    # obtain the child of the strace_proc
    # because that is the one we want to kill
    strace_pid = get_children(strace_pid)
    sudo_kill(strace_pid)

    # get the output from the buffer
    out = ""
    err = ""
    out, err = strace_proc.communicate()

    # parse the trace
    out = out.decode()

    file_found = []
    for line in out.strip().split("\n")[1:]:
        if "(" in line and ")" in line:
            line = line.split("(")[1].split(")")[0]
            parts = line.split('"')
            for p in parts:
                if p.startswith("/home/"):
                    # get rid of paths that are hidden
                    tokens = p.split("/")
                    for t in tokens:
                        if t.startswith(
                            "."
                        ):  # why not t[0]=='.' => may be of zero length
                            # do nothing
                            break
                    else:
                        # add to set
                        if os.path.isfile(p):
                            if p not in file_found:
                                file_found.append(p)

    # see if any file was found or should I run the title bar check?
    if len(file_found) == 0:
        tokens = title_bars[pids.index(id)].split()
        for p in tokens:
            if p.startswith("/home/"):
                # add to set
                if os.path.isfile(p):
                    if p not in file_found:
                        file_found.append(p)

    print("Used files found: ")
    for i, f in enumerate(file_found):
        print(f"[{i}]: {f}")

    f_idx = input("Enter the index of the file to transfer: ")

    result[i1] = {"process": name, "file": file_found[int(f_idx)]}

with open("transfer.json", "w") as f:
    json.dump(result, f, indent=4)

with open("transfer.json", "r") as f:
    contents = json.load(f)

print(contents)
