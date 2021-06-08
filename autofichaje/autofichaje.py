import pyautogui as auto
import webbrowser
import time

class Browser:
    def open_webpage(self):
        url = 'https://a3gt.wolterskluwer.es/gt#/clockings/78862'

        webbrowser.register('firefox',
                            None,
                            webbrowser.BackgroundBrowser("C://Program Files//Mozilla Firefox//firefox.exe"))

        webbrowser.get('firefox').open(url)


if __name__ == '__main__':
    firefox = Browser()
    firefox.open_webpage()

    # Wait until the page is loaded
    time.sleep(5)

    #  Select the fields to introduce the user and password
    user = '48605975Y'
    password = '23612wFVoi'

    # Click on user (User is autoselected)
    # auto.click(2309, 319)

    # Introduce user ID
    auto.write(user)

    # Click on password
    auto.click(2327, 487)

    # Introduce password
    auto.write(password)

    # Click on send
    auto.click(2378, 626)




