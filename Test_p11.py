from p11 import *

import random
import unittest


class TestEstAnagrame(unittest.TestCase):
    NB_TESTS = 1000
    
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
            ln = random.randint(3, 100)
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


class TestAnagrammes(unittest.TestCase):
    NB_TESTS = 100
    d = {}

    def make_random_lexicon(self, word_size_max, lexicon_size):
        d = {}
        for i in range(lexicon_size):
            ln = random.randint(3, word_size_max)
            w = "".join([chr(65 + random.randrange(26)) for i in range(ln)])
            h = hash_dict(w)
            if h in d:
                d[h].append(w)
            else:
                d[h] = [w]
        TestAnagrammes.d = d
        globals()["dictionnaire"] = d

    def all_dict_as_lst(self):
        L = []
        for v in TestAnagrammes.d.values():
            L.extend(v)
        return L

    def test_with_in_lexicon(self):
        self.make_random_lexicon(3, 1000)
        L = self.all_dict_as_lst()
        for i in range(TestAnagrammes.NB_TESTS):
            random.shuffle(L)
            w = L[0]
            tmp_lst = []
            for v in L:
                if est_anagrame(w, v):
                    tmp_lst.append(v)
            self.assertGreaterEqual(len(tmp_lst), 1)
            

    def test_with_no_anagram(self):
        self.make_random_lexicon(3, 1000)
        for i in range(TestAnagrammes.NB_TESTS):
            keys = list(zip(*TestAnagrammes.d.keys()))[0]
            key = random.randint(8, max(keys) + 100)
            while key in keys or not all([v in PRIMES for v in decompose(key)]):
                key = random.randint(8, max(keys) + 100)
            w = "".join(map(lambda v: table_chr_int[v], list(decompose(key))))
            self.assertEqual(len(anagrammes(w)), 0)

    def test_with_not_in_lexicon(self):
        L = self.all_dict_as_lst()
        for i in range(TestAnagrammes.NB_TESTS):
            random.shuffle(L)
            w1 = L[0]
            w2 = list(w1)
            random.shuffle(w2)
            w2 = "".join(w2)
            tmp = 0
            while tmp < 10 or w2 in L:
                tmp += 1
                w2 = list(w1)
                random.shuffle(w2)
                w2 = "".join(w2)


if __name__ == '__main__':
    unittest.main()
