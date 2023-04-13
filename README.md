This program is a fork of mozilla/pdf.js that allows you to host your own instance of pdf.js. Once set up, you can use Vimium in the Firefox PDF viewer.Vimium PDF for Firefox
Requirements

    Node.js
    Python 3

Installation

 Install Node.js and Python 3 on your system.

 Run the install.py script in the script folder as administrator. This script will set up the necessary files and folders for the program to function properly.


    python3 script/install.py

 Execute the start_gulp_server.bat file in the script folder to start the Gulp server.



    script/start_gulp_server.bat

Usage

To use Vimium PDF for Firefox as your PDF reader, follow the steps below:

   Locate a PDF file on your system.

   Right-click on the PDF file, and select "Open with..."

   Click "Choose another app" or "Browse" (depending on your OS) and navigate to the vimpdf.exe file located in the script\dist folder.

   Select vimpdf.exe and click "Open" or "OK" to open the PDF file with Vimium PDF for Firefox.
    
To set VimPDF as the default PDF viewer in Firefox, follow these steps:

   Open Firefox and click the menu button in the top right corner.
   Click "Options" and then click "General" in the left-hand menu.
   Scroll down to the "Applications" section.
   In the search bar, type "PDF".
   In the "Portable Document Format (PDF)" row, click the drop-down menu and select "Use VimPDF".
   Close the settings tab and reload Firefox.

Note: If you want to switch back to the default PDF viewer, simply follow the same steps and select "Preview in Firefox" instead.

Generate vimpdf.exe (Optional)

If you wish to generate the vimpdf.exe file yourself, you can use PyInstaller.

   Install PyInstaller using pip:


    pip install pyinstaller

  Navigate to the script folder and run PyInstaller to create the vimpdf.exe file:


    cd script
    pyinstaller --onefile vimpdf.py

The vimpdf.exe file will be created in the script\dist folder.
