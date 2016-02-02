#!/usr/bin/env python3

import unittest
import subprocess
from subprocess import PIPE
# import argparse
import sys

# def get_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('test_op', type=str, choices=['lscpu', 'configure', 'make', 'sahex1'], help="Type of build to test.")
#     return parser.parse_args()

class ConfigureTestBase(unittest.TestCase):

    args = []
    in_stdout = False
    in_stderr = False

    @classmethod
    def setUpClass(cls):
        with    open('foobar.stdout', 'w') as stdout_log, \
                open('foobar.stderr', 'w') as stderr_log, \
                subprocess.Popen(cls.args, 
                        stdout=PIPE, stderr=PIPE, universal_newlines=True) as proc:

            for line in proc.stdout:
                print(line.rstrip() + ' out')
                stdout_log.write(line.rstrip() + ' out\n')
                if 'L2' in line:
                    cls.in_stdout = True

            for line in proc.stderr:
                print(line.rstrip() + ' err')
                stderr_log.write(line.rstrip() + ' err\n')
                if 'L2' in line:
                    cls.in_stderr = True

    def test_L2_in_stdout(self):
        cls = self.__class__
        self.assertTrue(cls.in_stdout)

    def test_L2_in_stderr(self):
        cls = self.__class__
        self.assertTrue(cls.in_stderr)
    

if __name__ == "__main__":
    suite = unittest.TestSuite()

    NewTestCase = type('ConfigureTest', (ConfigureTestBase,), dict(args=sys.argv[1:]))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(NewTestCase))

    unittest.TextTestRunner(verbosity=2).run(suite)
