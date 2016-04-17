from A import *

import random
import unittest


class TestA1(unittest.TestCase):
    def testROSE(self):
        A1("ROSE")
        self.assertEqual(fun_nb_sols(), 8)

    def testPROSE(self):
        A1("PROSE")
        self.assertEqual(fun_nb_sols(), 11)

    def testCHAMPOLION(self):
        A1("CHAMPOLION")
        self.assertEqual(fun_nb_sols(), 709)

class TestA2(unittest.TestCase):
    def testCHAMPOLLION(self):
        A2("CHAMPOLLION", 1)
        self.assertEqual(fun_nb_sols(), 0)

    def testCHAMPOLLION2(self):
        A2("CHAMPOLLION", 2)
        self.assertEqual(fun_nb_sols(), 11)

    def testCAROLINEETFLORIAN2(self):
        A2("CAROLINEETFLORIAN", 2)
        self.assertEqual(fun_nb_sols(), 445)



if __name__ == '__main__':
    unittest.main()
