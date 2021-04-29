import shutil
import os
from subprocess import Popen, PIPE, STDOUT
import getpass
import socket
from colorama import init
from termcolor import colored

def format_path(path: str, usr: str) -> str:
    if path.startswith(f"/home/{usr}"):
        new_path = path.replace(f"/home/{usr}", "~")

    return new_path

# Courtesy: https://stackoverflow.com/a/1094933/15609488
def human(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def human_time(diff):
    res = ""
    days = diff // 86400
    hours = diff // 3600 % 24
    minutes = diff // 60 % 60
    seconds = diff % 60
    if days > 0:
        res += f"{days:.1f} days "
    if hours > 0:
        res += f"{hours:.1f} hours "
    if minutes > 0:
        res += f"{minutes:.1f} min "
    if seconds > 0:
        res += f"{seconds:.1f} sec "
    
    return res

def copy_cmd(src: str, dst: str, indent: int):
    # if it's a directory, ask for recursive copy
    if os.path.isdir(src):
        resp = input(" "*indent+f"{src} is a directory. Do you want to copy all its contents? (y/n) ")
        if resp.strip().lower() == 'y' or \
            resp.strip().lower() == 'yes':
            try:
                dir_name = src.split("/")[-1]
            except:
                dir_name = src
            os.makedirs(os.path.join(dst, dir_name), exist_ok=True)
            for f in os.listdir(src):
                copy_cmd(os.path.join(src, f), os.path.join(dst, dir_name), indent+1)
        else:
            print(" "*indent+"Ok. Nevermind then.")
    
    else:
        # if it's not a directory, check for conflict
        try:
            src_file_name = src.split("/")[-1]
        except:
            src_file_name = src
        
        for file in os.listdir(dst):
            if file==src_file_name:

                print(" "*indent+"A file by the same name is already present.")
                print(" "*indent+f"Src file size: [{human(os.path.getsize(src))}]")
                print(" "*indent+f"Dst file size: [{human(os.path.getsize(os.path.join(dst, file)))}]")
                
                # get last modified times
                src_time = os.path.getmtime(src)
                dst_time = os.path.getmtime(os.path.join(dst, file))

                diff = src_time-dst_time
                diff = human_time(diff)
                if src_time>dst_time:
                    print(" "*indent+"Src file is "+colored("newer", "green")+f" by {diff}")
                else:
                    print(" "*indent+"Src file is "+colored("newer", "orange")+f" by {diff}")
                resp2 = input(" "*indent+"Want to "+colored("overwrite", "red")+"? (y/n) ")
                if resp2.strip().lower() == 'y' or \
                    resp2.strip().lower() == 'yes':
                    shutil.copy(src, dst)
                    print(" "*indent+"Copied"+colored(f"[\"{src}\"]", "yellow")+" into "+colored(f"[\"{dst}\"]", "green"))
                else: 
                    print(" "*indent+"Ok. Nevermind then.")

        shutil.copy(src, dst)
        print(" "*indent+"Copied "+colored(f"[\"{src}\"]", "yellow")+" into "+colored(f"[\"{dst}\"]", "green"))

def copy_handler(cmd: str, bg: bool):
    """
    Handle the copy command
    
    Conditions: Options must be placed before src and dst

    """
    # get rid of the command name
    cmd = cmd.strip().split()[1:]

    options = []
    files = []
    options_done = False
    for tok in cmd:
        if tok.startswith("-") and not options_done:
            options.append(tok)
        else:
            options_done = True
            files.append(tok)

    # separate out the source and destination files
    dst = files[-1]
    src = files[:-1]

    # check if dst is dir
    if not os.path.isdir(dst):
        print("ERROR: The destination is not a directory")
        return

    # copy the srces one by one
    for s in src:
        copy_cmd(s, dst, 0)

    print()
    return

def move_handler(cmd: str, bg: bool):
    """
    Handle the move command
    """
    pass

def change_dir_handler(cmd: str, bg: bool):
    """
    Handle the change directory command
    """
    pass

def make_dir_handler(cmd: str, bg: bool):
    """
    Handle the make directory command
    """
    pass

def list_handler(cmd: str, bg: bool):
    """
    Handle the list files command
    """
    pass

def listener(cmd: str, bg: bool):
    """
    The voice commands module
    """
    pass

def carryOn(cmd: str):
    """
    carryOn module: pick up where you left off!
    """
    pass

user = getpass.getuser()
machine = socket.gethostname()

while(True):

    # get the current directory for the prompt
    pwd = format_path(os.getcwd(), user)

    # print the user and machine
    print(colored(f"{user}@{machine}", "yellow", attrs=["bold"])+":", end='')

    # print the current path
    print(colored(f"{pwd}", "cyan", attrs=["bold"])+colored("$ ", "green", attrs=["bold"]), end='')

    # get command
    cmd = input()
    print(cmd.strip().split())

    cmd = cmd.strip()
    if cmd.startswith("exit"):
        print("Exiting")
        exit(0)

    # check if background run is needed
    run_in_background = False
    if cmd.endswith("&"):
        run_in_background=True
        cmd = cmd.replace("&", "").strip()

    if cmd.startswith("ls"):
        list_handler(cmd, run_in_background)
    elif cmd.startswith("cd"):
        change_dir_handler(cmd, run_in_background)
    elif cmd.startswith("mkdir"):
        make_dir_handler(cmd, run_in_background)
    elif cmd.startswith("cp"):
        copy_handler(cmd, run_in_background)
    elif cmd.startswith("mv"):
        move_handler(cmd, run_in_background)
    elif cmd.startswith("listen"):
        listener(cmd, run_in_background)
    elif cmd.startswith("carryon"):
        if run_in_background==True:
            print("Cannot run carryOn module in the background.")
            print("Starting it now...")
        carryOn(cmd)

    # proc = Popen(cmd.strip().split(), stderr=STDOUT, stdout=PIPE)

    # out, err = proc.communicate()

    # if err is None:
    #     print(out.decode())
    # else:
    #     print("An error has occurred.")
    #     print(err)

    # handle simple commands

    # ls
    # cd
    # cp
    # mv
    # mkdir
    # exit
    # carryon
    # listen
    # handle exceptions

