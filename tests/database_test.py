import unittest
from table_sender.LogicMaster import LogicMaster
from table_sender.table import Table
import numpy as np

class MyTestCase(unittest.TestCase):

    def test_something(self):

        LogicMaster()
        self.assertEqual(True, True)
        # matrix = np.random.randint(800, size=(7, 10))
        # Table(matrix)


if __name__ == '__main__':
    unittest.main()
