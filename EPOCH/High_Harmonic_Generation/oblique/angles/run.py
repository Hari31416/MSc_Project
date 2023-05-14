import os
import glob
from style import *

folders = glob.glob("*/*")
command = "epoch1d < deck.file"
for folder in folders:
    cprint(f"Running {folder}", "red")
    if "images" in folder:
        continue
    os.chdir(folder)
    os.system(command)
    os.chdir("../..")
