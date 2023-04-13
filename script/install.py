import os
import shutil


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


script_path = os.path.abspath(__file__)

source = os.path.dirname(os.path.dirname(script_path))

program_files = os.environ.get('ProgramFiles')

copytree(source, program_files)
