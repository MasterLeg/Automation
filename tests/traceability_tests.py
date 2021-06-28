import unittest
import xlwings as xw

class MyTestCase(unittest.TestCase):
    def test_something(self):
        app = xw.apps.active
        location = app.selection
        # Location: "$A$1"

        # Get location value
        value = location.value
        column = location.column
        row = location.row

        self.assertEqual(column, 1)
        self.assertEqual(row, 1)


if __name__ == '__main__':
    unittest.main()
