import os
import shutil
import sys
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Copys directorys and files without the exclude_dir


def copytree(src, dst, exclude_dir='.git'):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        if item == exclude_dir:
            continue

        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            copytree(s, d)  # Rekursiv für Unterordner
        else:
            shutil.copy2(s, d)  # Dateien kopieren


if is_admin():
    print("The script is running with administrator priviliges")
else:
    print("The script is not running with administrator priviliges. Requesting admin priviliges... ")
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
script_path = os.path.abspath(__file__)

source = os.path.dirname(os.path.dirname(script_path))

program_files = os.environ.get('ProgramFiles')

copytree(source, program_files)
