import unittest
from email_sender.LogicMaster import LogicMaster


class MyTestCase(unittest.TestCase):

    def test_something(self):

        LogicMaster()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
