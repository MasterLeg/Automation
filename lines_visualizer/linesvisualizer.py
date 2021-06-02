import webbrowser

class Opener:
    def __init__(self):
        urls = ['10.156.1.51:8000',
                '10.156.1.51:8001',
                '10.156.1.51:8002',
                '10.156.1.51:8003']

        webbrowser.register('firefox',
                            None,
                            webbrowser.BackgroundBrowser("C://Program Files//Mozilla Firefox//firefox.exe"))

        for url in urls:
            webbrowser.get('firefox').open(url)

if __name__ == '__main__':
    o = Opener()
