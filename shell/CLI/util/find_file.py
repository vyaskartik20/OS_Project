import json
import os
from signal import SIGINT
from subprocess import PIPE, STDOUT, Popen, TimeoutExpired
from threading import Thread
from time import sleep
import time

from ewmh import EWMH

class sharedInfo:
    def __init__(self):
        self.titles = []

def get_children(pid):
    cmd = f"ps --ppid {pid}"
    output, _ = Popen(cmd.split(" "), stdout=PIPE).communicate()
    # print(output.decode())
    return int(output.decode().split("\n")[1].split()[0])


def sudo_kill(strace_pid):
    kill_cmd = f"sudo kill {strace_pid}"
    kill_proc = Popen(kill_cmd.split(" "), stderr=STDOUT, stdout=PIPE)
    kill_out, kill_err = kill_proc.communicate()


def monitor_title_bar(window_manager: EWMH, pid: int, title_bar_info: sharedInfo):
    open_windows = window_manager.getClientList()
    # get window object from PID
    curr_window = None
    for w in open_windows:
        if window_manager.getWmPid(w) == pid:
            curr_window = w
            break

    if curr_window != None:
        
        # activate the window
        window_manager.setActiveWindow(curr_window)

        # run for 10 seconds, the while loop
        # to accumulate title bars
        titles = set()
        init_time = time.time()
        while time.time() - init_time < 10:
            titles.add(window_manager.getWmName(curr_window))
    
    else:
        print("Well this shouldn't have happened.")
        print(f"Something went wrong while trying to find the window with PID {pid}.")

    if len(titles)==0:
        print("I'm empty :(")
        exit(1)
    for k in titles:
        title_bar_info.titles.append(k)
    
    return

def main() :

    common_exes = ['mkv', 'mp4', 'mp3', 'flac', 'aac', 'wav', 'mov', ]

    # get open windows
    window_manager = EWMH()
    open_windows = window_manager.getClientList()

    title_bars = []
    pids = []
    for window in open_windows:
        title_bars.append(window_manager.getWmName(window))
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
    count = 0
    # get the open files for the PIDs
    for i1, (id, name) in enumerate(zip(pids_to_transfer, processes_to_transfer)):
        # first attach strace to the process
        cmd = f"sudo strace -I 1 -e trace=file,open,close,write -p {id} -f"
        strace_proc = Popen(cmd.split(" "), stderr=STDOUT, stdout=PIPE)
        strace_pid = strace_proc.pid
        print("Strace PID:", strace_pid)

        # wait for some time
        print(f"Go to {name} and save your work")
        
        # get title bars in the meantime
        title_bar_info = sharedInfo()
        t1 = Thread(target=monitor_title_bar, args=(window_manager, id, title_bar_info))
        t1.start()

        # sleep(10)

        t1.join()
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

        files_found = []
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
                                if p not in files_found:
                                    files_found.append(p)

        # see if any file was found or should I run the title bar check?
        if len(files_found) == 0:
            # no files were found, get data from the title bar checks
            for t in title_bar_info.titles:
                # print(t)
                tokens = t.split()
                for p in tokens:
                    if p.startswith(("/home/", "~/")):
                        # add to set
                        if os.path.isfile(os.path.abspath(os.path.expanduser(p))):
                            if p not in files_found:
                                files_found.append(os.path.abspath(os.path.expanduser(p)))

        if len(files_found)>0:
            print("Files in use: ")
            for i, f in enumerate(set(files_found)):
                print(f"[{i}]: {f}")

            f_idx = input("Enter the indices of the file to transfer: ")
            
            for f in f_idx.strip().split():
                result[count] = {"process": name, "file": files_found[int(f)]}
                count+=1
        else:
            print(f"Couldn't find any open files for process: [{name}]")
            file_alt = input("Enter a path instead (enter to skip)")
            if not(file_alt == '-' or file_alt == ''):
                result[count] = {"process": name, "file": file_alt}
                count += 1

    with open("transfer1.json", "w") as f:
        json.dump(result, f, indent=4)

    # with open("transfer.json", "r") as f:
        # contents = json.load(f)

    # print(contents)


if __name__ == "__main__" :
    main()


