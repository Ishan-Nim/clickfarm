import unittest
import logging

from trustie import *

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s')

class test_trustie(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        obj = trustie()


if __name__ == '__main__':
    unittest.main()
