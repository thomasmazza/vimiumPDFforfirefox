import os
import shutil
import sys
import ctypes
import subprocess
import configparser

try:
    from win32com.client import Dispatch
except ImportError:
    print("win32com module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
    print("Restarting the script...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

config = configparser.ConfigParser()
config.read('config.ini')

PROGRAM_FILES = os.environ.get('ProgramFiles')
DESTINATION_FOLDER_NAME = config.get('general', 'destination_folder_name')
DESTINATION_PATH = os.path.join(PROGRAM_FILES, DESTINATION_FOLDER_NAME)
PDF_FOLDER_NAME = config.get('general', 'pdf_folder_name')
SERVER_PORT = config.getint('server', 'port')
AUTOSTART = config.getboolean('general', 'autostart')
SCRIPT_PATH = os.path.abspath(__file__)
SOURCE = os.path.dirname(os.path.dirname(SCRIPT_PATH))
TEMP_FOLDER = os.environ.get("TEMP")
PDF_FOLDER_PATH = os.path.join(TEMP_FOLDER, PDF_FOLDER_NAME)
PDF_FILES_FOLDER = "pdf"
PDF_FOLDER_SYMLINK_PATH = os.path.join(DESTINATION_PATH, PDF_FILES_FOLDER)


def create_shortcut(target, path, description):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(path)
    shortcut.TargetPath = "runas.exe"
    shortcut.Arguments = f'/savecred /user:Administrator "{target}"'
    shortcut.Description = description
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.IconLocation = target
    shortcut.save()


def install_dependencies():
    if is_npm_installed():
        print("npm is installed")
        if not (is_gulp_installed()):
            print("gulp-cli is not installed. Installing gulp-cli..")
            install_gulp

        os.chdir(DESTINATION_PATH)
        run_npm_install()
    else:
        print("npm is not installed. Please install npm and try again.")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def create_symlink(source_folder, target_folder, link_name):
    link_path = os.path.join(target_folder, link_name)
    try:
        subprocess.run(
            f'mklink /D "{link_path}" "{source_folder}"', shell=True, check=True)
    except Exception as e:
        print(f"Error occurred while creating the symlink: {e}")


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


def is_npm_installed():
    try:
        subprocess.check_output("npm --version", shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(
            f"Error occurred while checking npm version: {e.output.decode('utf-8')}")
        print("Please make sure npm is installed and available in your PATH")


def run_npm_install():
    try:
        subprocess.check_output("npm install --force", shell=True)
        print("npm install completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running 'npm install': {e}")


def is_gulp_installed():
    try:
        subprocess.check_output("gulp --version", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False


def install_gulp():
    try:
        subprocess.check_output("npm install -g gulp-cli", shell=True)
        print("gulp-cli has been installed globally.")
    except subprocess.CalledProcessError as e:
        print(f"Error eccoured while installing gulp: {e}")


def setup_folders():
    copytree(SOURCE, DESTINATION_PATH)
    print("Copying completed.")
    if not os.path.exists(PDF_FOLDER_PATH):
        os.makedirs(PDF_FOLDER_PATH)
    create_symlink(PDF_FOLDER_PATH, DESTINATION_PATH, PDF_FILES_FOLDER)


# Main Routine
if is_admin():
    print("The script is running with administrator privileges.")

    install_dependencies()
    setup_folders()

    # Create Shortcut in Autostart
    if (AUTOSTART):
        batch_file = os.path.join(
            os.environ['ProgramFiles'],
            r'VimiumPDFForFirefox\script',
            'run_gulp_server.bat')
        startup_folder = os.path.join(
            os.environ['APPDATA'],
            r'Microsoft\Windows\Start Menu\Programs\Startup')
        shortcut_path = os.path.join(startup_folder, 'GulpServerPDF.lnk')
        create_shortcut(batch_file, shortcut_path,
                        'Run Gulp server as administrator')
        print(f'Shortcut created at: {shortcut_path}')

else:
    print("The script is running without administrator privileges.")
    print("Administrator prvileges are required to install and configure VimiumPDFForFirefox.")
    print("Requesting administrator privileges...")
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
