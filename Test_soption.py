from option import *

import random
import unittest


class TestEstPresqueAnagramme(unittest.TestCase):
    def testParDrap(self):
        self.assertEqual(est_presque_anagramme("PAR", "DRAP", 1), True)
        
    def testParDrapa(self):
        self.assertEqual(est_presque_anagramme("PAR", "DRAPA", 2), True)

class TestPresqueAnagramme(unittest.TestCase):
    def testPar1(self):
        self.assertEqual(est_presque_anagramme("PAR", "DRAP", 1), True)
        
    def testParDrapa(self):
        self.assertEqual(len(presque_anagrammes("PAR", 1)), 20)

if __name__ == '__main__':
    dictionnaire = load_lexicon()
    unittest.main()
