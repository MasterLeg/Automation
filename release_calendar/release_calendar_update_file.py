import os
import shutil
from os.path import isfile, join
from pathlib import Path
import time
import pyautogui as auto

def open_desktop():
    """
    Returns to desktop
    :return: None
    """
    auto.click(1918, 1054)
    auto.click()

def automated_cartridge_release_calendar_saving():
    # open_desktop()
    # Open Teams
    # os.startfile('C:\\Users\\epardo\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe')

    # Select Teams
    auto.click(859, 1061)
    auto.PAUSE = 1.5

    # Select "Equipos"
    auto.click(33, 187)
    auto.PAUSE = 0.7

    # Select "Manufacturing BCN"
    auto.click(170, 163)
    auto.PAUSE = 0.8

    # Select "Archivos"
    auto.click(698, 82)
    time.sleep(0.8)

    # Select the folder "01 Cartridge Release Calendar"
    auto.click(661, 477)
    time.sleep(1)

    # Select the Excel "Cartridge Release Calendar BCN.xlsx"
    auto.click(662, 477)
    time.sleep(3)

    # Select "Archivo"
    auto.click(95, 64)

    # Select "Guardar como"
    auto.click(160, 300)

    # Select "Descargar una copia"
    auto.click(400, 300)

def cut_and_paste_downloaded_file(original_path, directory_target):
    # Delete current file saved
    if os.path.exists(directory_target):
        print('\tOK => Removing file from 3.KPI')
        os.remove(directory_target)
    else:
        print('\tOK => No removing file from 3.KPI. It was already removed')

    # Copy the new file to another directory
    if os.path.exists(original_path):
        print('\tOK => Copying file from Downloads to 3.KPI')
        shutil.copyfile(original_path, directory_target)
    else:
        print('\tFAIL = > File from Downloads does not exist. Retrying in 1 second')
        onlyfiles = [f for f in os.listdir(original_path) if isfile(join(original_path, f))]
        print(onlyfiles)
        time.sleep(1)
        cut_and_paste_downloaded_file(original_path, directory_target)


def main():
    my_file = Path(r'C:\Users\Epardo\Downloads\Cartridge Release Calendar BCN.xlsx')
    my_file2 = Path(r'J:\48 Documentation\3.KPI\Cartridge Release Calendar BCN - Copia.xlsx')

    # First removing if the file exists in Downloads
    if my_file.exists():
        print('OK => Removing file from folder Downloads')
        os.remove(my_file)

    # Delete if there is a copy in 3.KPI
    if os.path.exists(my_file2):
        print('OK => Removing file from 3.KPIs')
        os.remove(my_file2)
    else:
        print('OK => 3.KPI No file to remove')

    # Download new file
    print('OK => Executing the Automated Scratching script')
    automated_cartridge_release_calendar_saving()
    time.sleep(3)
    print('OK => Data downloaded correctly!')

    print('OK => File appears in Downloads' if my_file.exists()
          else ' FAIL => Error: File not downloaded in Downloads')

    cut_and_paste_downloaded_file(my_file, my_file2)

    print('OK => Downloaded file in Downloads' if my_file.exists() else 'FAIL => Removed file in Downloads')
    print('OK => Copied file in 3.KPI' if my_file2.exists() else 'FAIL => Critical Error: Not copied new file in KPIs')


if __name__ == '__main__':
    executed = False

    # Repeat until it raises no error
    while not executed:
        try:
            main()
        except Exception:
            pass
        else:
            executed = True
