import os
import shutil
import sys
import webbrowser


def move_pdf(pdf_file, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    filename = os.path.basename(pdf_file)
    new_path = os.path.join(target_folder, filename)
    shutil.move(pdf_file, new_path)
    return new_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the PDF file as an argument.")
        sys.exit(1)
    temp_folder = os.environ.get("TEMP")
    pdf_folder_name = "VimiumPDFForFirefox"
    pdf_folder_path = os.path.join(temp_folder, pdf_folder_name)
    print("Before copying")
    if not os.path.exists(pdf_folder_path):
        os.makedirs(pdf_folder_path)
        print(pdf_folder_path)
    pdf_file = sys.argv[1]
    new_pdf_path = move_pdf(pdf_file, pdf_folder_path)

    url = f"localhost:8888/web/viewer.html?file=%2Fpdf%2F{os.path.basename(pdf_file}"
    webbrowser.open(url)
