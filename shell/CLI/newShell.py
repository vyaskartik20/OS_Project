from os.path import expanduser
import shutil
import os
from subprocess import Popen, PIPE, STDOUT
import getpass
import socket
from colorama import init
from termcolor import colored

def shorten_path(path: str, usr: str) -> str:
    if path.startswith(f"/home/{usr}"):
        shortened_path = path.replace(f"/home/{usr}", "~")
        return shortened_path
    else:
        return path

def expand_path(path: str) -> str:
    expanded_path = os.path.expanduser(path)
    if os.path.exists(expanded_path):
        expanded_path = os.path.abspath(expanded_path)
        if os.path.exists(expanded_path):
            return expanded_path
        else:
            print(colored("[ERROR]", "red")+f" [{expanded_path}] doesn't exist.")
            return None
    else:
        print(colored("[ERROR]", "red")+f" [{expanded_path}] doesn't exist.")
        return None


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
                return
            
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

    dst = expand_path(dst)
    if dst==None:
        return
    if os.path.exists(dst):
        if os.path.isdir(dst):
            pass
        else:
            print(colored("[ERROR]", "red")+" The destination path is a file.")
            exit(1)
    
    else:
        os.makedirs(dst)
        print(colored("[INFO]", "yellow")+" The destination folder has been created.")

    # copy the srces one by one
    for s in src:
        if os.path.exists(s):
            s = expand_path(s)
            if s==None:
                continue
            copy_cmd(s, dst, 0)
        else:
            print(colored("[INFO]", "yellow")+f" [{s}] - no such file .")


    print()
    return

# TODO: Make it verbose
def move_handler(cmd: str, bg: bool):
    """
    Handle the move command
    """
    cmd = cmd.strip()
    out, err = Popen(cmd, shell=True).communicate()
    # print(out.decode())
    return

def change_dir_handler(cmd: str, bg: bool):
    """
    Handle the change directory command
    """
    # get rid of the command name
    cmd = cmd.strip().split()

    if len(cmd)==1:
        os.chdir(expand_path("~"))

    else:
        if len(cmd)>2:
            print(colored("[ERROR]", "red")+" Too many arguments to cd.")
        else:
            dst = expand_path(cmd[1])
            if dst==None:
                return
            os.chdir(dst)
    return

def make_dir_handler(cmd: str, bg: bool):
    """
    Handle the make directory command
    """
    cmd = cmd.strip().split()
    if len(cmd)==1:
        print(colored("[ERROR]", "red")+" No operand to make dir.")
    else:
        for c in cmd[1:]:
            dst = expand_path(c)
            if dst==None:
                print(colored("[ERROR]", "yellow")+f" Invalid request [{c}].")
            else:
                try:
                    os.makedirs(dst)
                except FileExistsError:
                    print(colored("[INFO]", "yellow")+f" Dir already present [{dst}].")
    return

def list_handler(cmd: str, bg: bool):
    """
    Handle the list files command
    """
    cmd = cmd.strip()
    out, err = Popen(cmd, shell=True).communicate()
    # print(out.decode())
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
    pwd = shorten_path(os.getcwd(), user)

    # print the user and machine
    print(colored(f"{user}@{machine}", "yellow", attrs=["bold"])+":", end='')

    # print the current path
    print(colored(f"{pwd}", "cyan", attrs=["bold"])+colored("$ ", "green", attrs=["bold"]), end='')

    # get command
    try:
        cmd = input()
    # print(cmd.strip().split())
    except KeyboardInterrupt:
        print("\nExiting.")
        exit(0)
    
    cmd = cmd.strip()
    if cmd.startswith("exit"):
        print("Exiting")
        exit(0)

    # check if background run is needed
    run_in_background = False
    if cmd.endswith("&"):
        run_in_background=True
        cmd = cmd.replace("&", "").strip()

    if "|" in cmd:
        out, err = Popen(cmd, shell=True, stderr = STDOUT, stdout = PIPE).communicate()
        print(out)
    elif cmd.startswith("ls"):
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
    else:
        out, err = Popen(cmd, shell=True, stderr = STDOUT, stdout = PIPE).communicate()

    # handle simple commands


    # carryon
    # listen
    # handle exceptions

