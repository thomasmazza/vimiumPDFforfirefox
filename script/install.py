import os
import shutil
import sys
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def copytree(src, dst, exclude_items=['.git', '.github', 'examples']):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        if item in exclude_items:
            continue

        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        # Add a print statement to track progress
        print(f"Copying: {s} -> {d}")

        if os.path.isdir(s):
            copytree(s, d)  # Recursively for subfolders
        else:
            shutil.copy2(s, d)  # Copy files


if is_admin():
    print("The script is running with administrator privileges.")

    script_path = os.path.abspath(__file__)
    source = os.path.dirname(os.path.dirname(script_path))
    program_files = os.environ.get('ProgramFiles')

    # Specify the target folder name inside the Program Files folder
    destination_folder_name = "VimiumForFirefox"
    destination_path = os.path.join(program_files, destination_folder_name)

    print(f"Source: {source}")  # Print source path
    print(f"Destination: {destination_path}")  # Print destination path

    copytree(source, destination_path)

    print("Copying completed.")  # Print a message when copying is done
else:
    print("The script is running without administrator privileges. Requesting administrator privileges...")
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
