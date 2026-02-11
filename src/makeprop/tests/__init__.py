import unittest

__all__ = ["test"]


def test() -> unittest.TextTestRunner:
    loader: unittest.TestLoader
    tests: unittest.TestSuite
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir="makeprop.tests")
    return unittest.TextTestRunner().run(tests)
