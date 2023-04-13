import os
import shutil

script_path = os.path.abspath(__file__)

source = os.path.dirname(os.path.dirname(script_path))

program_files = os.environ.get('ProgramFiles')

shutil.move(source, program_files)
