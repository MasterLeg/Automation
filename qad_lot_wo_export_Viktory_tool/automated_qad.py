import pyautogui as auto
import time
import pyperclip

def open_desktop():
    """
    Returns to desktop
    :return: None
    """
    auto.click(1918, 1054)
    auto.click()

def current_position():
    current_mouse_x, current_mouse_y = auto.position()
    print('Posición actual: X = ', current_mouse_x, '; Y = ',  current_mouse_y)

def screen_size():
    screen_width, screen_height = auto.size()
    print('Ancho pantalla: ', screen_width, ' Alto pantalla: ', screen_height)

def copy_selection():
    auto.hotkey('ctrl', 'c')
    time.sleep(.01)
    return pyperclip.paste()

def pointer_debugger():
    while True:
        current_position()

def steps(lot_number):
    # Go to desktop
    # open_desktop()

    # Get current position
    # while True:
    #     current_position()

    # Open the Lot Status Excel (located in the desktop matrix (nxm) position (n=1, m=3) => pos (x=325, y=50)
    # auto.doubleClick(325, 50)

    # Wait until the Excel opens
    # time.sleep(5)

    # Select the modes drop_down list: x,y = (552, 149)
    auto.click(552, 149)

    # Select "equals" in the drop down: x,y = (529, 166)
    auto.click(529, 166)

    # Click to drop down the fields list: x,y = (458, 149)
    auto.click(458, 149)

    # Click to select 'Lot/Serial' in drop-down: x,y = (408, 180)
    auto.click(408, 180)

    # Position searcher in Work Order: x,y = (421, 348)
    auto.doubleClick(421, 348)

    # Introduce the Lot serial number
    auto.write(lot_number, interval=0.01)
    # time.sleep(2)
    auto.press('enter')
    time.sleep(2)

    # Click on the Work Order number: x,y = (373, 232)
    auto.click(373, 232)
    time.sleep(0.7)

    # Copy Work Order number
    work_order_number = copy_selection()
    print('Work Order: ', work_order_number)

    # Select again the browser: x,y = (607, 147)
    time.sleep(0.2)
    auto.doubleClick(607, 147)

    # Delete the introduced lot serial
    auto.keyDown('delete')
    time.sleep(1.5)
    auto.keyUp('delete')

    # Introduce the selected Work Order number
    auto.write(work_order_number, interval=0.01)

    # Click to drop down the fields list: x,y = (458, 149)
    auto.click(458, 149)

    # Work Order position in the Drop-down: x,y = (438, 348)
    auto.click(438, 348)
    time.sleep(0.3)

    # Type 'Enter'
    auto.press('enter')

    # print('Sleeping 3 seconds')
    # time.sleep(3)

    # Open the "Actions" drop-down list: x,y = (374, 98)
    auto.click(374, 98)

    # Click on "Export": x,y = (405, 122)
    auto.click(405, 122)

    # Click on save as CSV file: x,y = (573, 122)
    auto.click(573, 122)
    time.sleep(0.5)

    # Write the file name, the same as the lot number
    auto.write(lot_number, 0.01)

    # Save the CSV Report file
    auto.press('enter')
    time.sleep(0.1)
    auto.press('enter')

    # Open the Firefox tab
    auto.click(556, 1065)
    time.sleep(0.1)

    # Click on "Raw Material"
    auto.click(1390, 686)
    time.sleep(0.3)

    # Click on "Import Raw Materials"
    auto.click(1223, 737)
    time.sleep(0.5)

    # Click on "Choose a file"
    auto.click(464, 264)
    time.sleep(0.5)

    # Click on "Nombre"
    auto.click(209, 476)
    auto.write(lot_number, 0.01)
    auto.press('enter')
    time.sleep(0.5)
    auto.press('enter')
    time.sleep(0.5)
    auto.press('enter')
    time.sleep(0.5)

    # Click on "Save to DB":
    auto.click(486, 255)
    time.sleep(0.3)

    # Click on "Go back to 'lot_number'"
    auto.click(383, 242)
    time.sleep(0.5)

    # Go back to QAD
    auto.click(567, 1055)


if __name__ == '__main__':

    print("""'Requiere en la pantalla principal:'
          '-  Firefox: abierta la ventana del lote a introducir, con el modo de usuario super activado'
          '-  QAD: abierta la transacción de "Work Trace" con la barra de búsqueda activada y sin modificar el tamaño de pantalla'""")

    lot_number = input('Introduce a lot number to get the data\t')

    steps(lot_number)
