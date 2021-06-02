import pyautogui as auto
import time


class Pointer:
    def get_current_position(self):
        current_mouse_x, current_mouse_y = auto.position()
        time.sleep(0.5)
        print('Posición actual: X = ', current_mouse_x, '; Y = ', current_mouse_y)


if __name__ == '__main__':
    p = Pointer()

    while True:
        p.get_current_position()