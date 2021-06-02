import unittest
import os
from os.path import isfile, join
from pathlib import Path


class MyTestCase(unittest.TestCase):


    def test_existence_downloaded_file(self):
        mypath = r'C:\Users\epardo\Downloads'
        path_str = r'C:\Users\epardo\Downloads\Cartridge Release Calendar BCN.xlsx'
        my_file = Path(path_str)
        onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
        print(onlyfiles)
        self.assertEqual(my_file.exists(), True)

    def test_existence_template_source_file(self):
        my_file2 = Path(r'J:\48 Documentation\3.KPI\Cartridge Release Calendar BCN - Copia.xlsx')
        self.assertEqual(my_file2.exists(), True)

if __name__ == '__main__':
    unittest.main()
