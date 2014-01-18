"""
Launcher is used for running
all unit tests from current directory
and all tests from sub directories.
"""

import unittest


VERBOSITY = 2

loader = unittest.TestLoader()
suite = loader.discover(start_dir='.')
runner = unittest.TextTestRunner(verbosity=VERBOSITY)
result = runner.run(suite)