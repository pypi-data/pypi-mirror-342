import unittest
from dosip.core import PyDOSIP


class TestCore(unittest.TestCase):

    def test_core(self) -> None:
        app = PyDOSIP()
        with self.subTest("Test PyDOSIP Instance"):
            self.assertIsInstance(app, PyDOSIP)

        with self.subTest("Test PyDOSIP Singleton"):
            self.assertIs(app, PyDOSIP())

            