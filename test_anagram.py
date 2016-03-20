from anagram import \
     est_anagrame, \
     est_presque_anagramme, \
     anagrammes, \
     best, \
     anagrammes_maximaux

import random
import unittest


class TestEstAnagrame(unittest.TestCase):
    NB_TESTS = 100
    
    def test_with_anagrammes(self):
        for i in range(TestEstAnagrame.NB_TESTS):
            ln = random.randint(1, 100)
            w1 = [chr(65 + random.randrange(26)) for i in range(ln)]
            w2 = w1[:]
            random.shuffle(w2)
            w1, w2 = "".join(w1), "".join(w2)
            self.assertEqual(est_anagrame(w1, w2), True)

    def test_with_not_anagrammes(self):
        for i in range(TestEstAnagrame.NB_TESTS):
            ln = random.randint(1, 100)
            if random.randint(1, 10) == 1: #test with differents sizes...
                w1 = [chr(65 + random.randrange(26)) for i in range(ln)]
                w2 = w1[:]
                w2 = w2[random.randint(1, ln - 2):]
                random.shuffle(w2)
                w1, w2 = "".join(w1), "".join(w2)
                self.assertEqual(est_anagrame(w1, w2), False)
            else: #test with 1 random different letter
                w1 = [chr(65 + random.randrange(26)) for i in range(ln)]
                w2 = w1[:-1]
                c = chr(65 + random.randrange(26))
                while c == w1[-1]:
                    c = chr(65 + random.randrange(26))
                w2.append(c)
                random.shuffle(w2)
                w1, w2 = "".join(w1), "".join(w2)
                self.assertEqual(est_anagrame(w1, w2), False)

    def test_with_random_words_same_size(self):
        for i in range(TestEstAnagrame.NB_TESTS):
            ln = random.randint(1, 10)
            w1 = [chr(65 + random.randrange(26)) for i in range(ln)]
            w2 = [chr(65 + random.randrange(26)) for i in range(ln)]
            w1, w2 = "".join(w1), "".join(w2)
            self.assertEqual(est_anagrame(w1, w2), sorted(w1) == sorted(w2))


if __name__ == '__main__':
    unittest.main()
