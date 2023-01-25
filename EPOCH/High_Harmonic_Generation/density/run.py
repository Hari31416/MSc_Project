import os
from style import cprint

directories = os.listdir()
directories = [dir for dir in directories if os.path.isdir(dir)]
directories = [dir for dir in directories if "run" in dir]
start = True
for dir in directories:
    if not start:
        cprint("\n")
        cprint("===" * 20, "green")
    cprint(f"Ruuning {dir}", "green")
    start = False
    os.chdir(dir)
    os.system("epoch1d < deck.file")
    os.chdir("..")
