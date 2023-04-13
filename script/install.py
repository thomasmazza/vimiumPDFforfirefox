import os
import shutil
import sys
import ctypes
import subprocess

try:
    from win32com.client import Dispatch
except ImportError:
    print("win32com module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
    print("Restarting the script...")
    os.execv(sys.executable, [sys.executable] + sys.argv)


def create_shortcut(target, shortcut_path, description='', run_as_admin=True):
    shell = Dispatch('WScript.Shell')

    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.Description = description

    if run_as_admin:
        hres = shell.CreateShortcut(shortcut_path)
        shell.SHGetSetShortcut(hres, "RunStyle", 1)
        hres.Save()
    shortcut.Save()


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
        print(e)


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
    except subprocess.CalledProcessError:
        return False


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
    except subprocess.CalledProcessErrori as e:
        print(f"Error eccoured while installing gulp: {e}")


# Main Routine
if is_admin():
    print("The script is running with administrator privileges.")

    script_path = os.path.abspath(__file__)
    source = os.path.dirname(os.path.dirname(script_path))
    program_files = os.environ.get('ProgramFiles')

    # Specify the target folder name inside the Program Files folder
    destination_folder_name = "VimiumPDFForFirefox"
    destination_path = os.path.join(program_files, destination_folder_name)

    print(f"Source: {source}")
    print(f"Destination: {destination_path}")

    copytree(source, destination_path)
    print("Copying completed.")

    if is_npm_installed():
        print("npm is installed.")
        if not (is_gulp_installed()):
            print("gulp-cli is not installed. Installing gulp-cli..")
            install_gulp()

        os.chdir(destination_path)
        run_npm_install()

        # Create Symlink to a TEMP Folder for the pdfs
        temp_folder = os.environ.get("TEMP")
        pdf_folder_name = "VimiumPDFForFirefox"
        pdf_folder_path = os.path.join(temp_folder, pdf_folder_name)
        print("Before copying")
        if not os.path.exists(pdf_folder_path):
            os.makedirs(pdf_folder_path)
            print(pdf_folder_path)

        # Create pdf folder in Program Files for symlink
        pdf_files_folder = "pdf"
        pdf_folder_symlink_path = os.path.join(
            destination_path, pdf_files_folder)

        create_symlink(pdf_folder_path, destination_path, "pdf")

        # Create Shortcut in Autostart
        batch_file = os.path.join(
            os.environ['ProgramFiles'], 'VimiumForPdf', 'run_gulp_server.bat')
        startup_folder = os.path.join(
            os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')
        shortcut_path = os.path.join(startup_folder, 'GulpServerPDF.lnk')
        create_shortcut(batch_file, shortcut_path,
                        'Run Gulp server as administrator', run_as_admin=True)

        print(f'Shortcut created at: {shortcut_path}')

    else:
        print("npm is not installed. Please install npm and try again.")

else:
    print("The script is running without administrator privileges. Requesting administrator privileges...")
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
