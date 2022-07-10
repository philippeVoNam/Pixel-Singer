# author : Philippe Vo
# date   : Mon 04 Jul 2022 02:22:56 PM

# 3rd party imports
import unittest
# user imports
from src.core.driver import Driver

class TestDriver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = Driver()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_verify(self):
        # success case
        self.assertTrue(self.driver.verify("test/res/test.mp3"))

        # file error
        self.assertRaises(Driver.InputFileError, self.driver.verify, "test/res/test.txt")

    def test_run(self):
        # success case
        status = self.driver.run("test/res/test.mp3")

        # file error
        self.assertRaises(Driver.InputFileError, self.driver.run, "test/res/test.txt")
