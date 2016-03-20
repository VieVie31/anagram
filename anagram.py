import functools
import operator

from time import time
from math import factorial
from functools import reduce
from collections import Counter

DICO_PATH = "ods.txt"

PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101)

table_chr_int = {
    2: 'E', 3: 'S', 5: 'A', 7: 'I', 11: 'R', 13: 'N', 17: 'T', 19: 'O',
 23: 'L', 29: 'U', 31: 'C', 37: 'M', 41: 'P', 43: 'D', 47: 'G', 53: 'B',
 59: 'F', 61: 'H', 67: 'Z', 71: 'V', 73: 'Q', 79: 'Y', 83: 'X', 89: 'J',
 97: 'K', 101: 'W',
 'A': 5, 'B': 53, 'C': 31, 'D': 43, 'E': 2, 'F': 59, 'G': 47, 'H': 61,
 'I': 7, 'J': 89, 'K': 97, 'L': 23, 'M': 37, 'N': 13, 'O': 19, 'P': 41,
 'Q': 73, 'R': 11, 'S': 3, 'T': 17, 'U': 29, 'V': 71, 'W': 101, 'X': 83,
 'Y': 79, 'Z': 67}


class memoize(dict): #decorateur pour la memorisation
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result

def compute_hash(word):
    """Retourne la premiere partie de la clef de hashage.

    >>> compute_hash("OLIVIER")
    33447106
    >>> compute_hash("COOL") #car C * O * O * L == 31 * 19 * 19 * 23
    257393
    """
    r = 1
    for c in word.upper():
        r *= table_chr_int[c]
    return r

def hash_dict(word):
    return (compute_hash(word), len(word))

def anagrammes(word):
    """Retourne la liste de tous les anagrammes de word dans le dictionnaire
    sous forme de liste si il y en a, sinon une liste vide.

    >>> anagrammes("OLIVIER")
    ["OLIVIER", "VOILIER", "VIOLIER"]
    """
    try:    return dictionnaire[hash_dict(word)]
    except: return []

def pgcd(a, b): #http://python.jpvweb.com/mesrecettespython/doku.php?id=pgcd_ppcm
    """Retourne le pgcd de a et b. Version etendu du pgcd avec le 1er coef
    de bezout (pour inversion modulaire de a).

    >>> pgcd(35, 21)
    7
    >>> pgcd(2016, 1996)
    4
    """
    r, u = a, 1
    rp, up = b, 0
    while rp != 0:
        q = r // rp
        rs, us = r, u
        r, u = rp, up
        rp, up = (rs - q * rp), (us - q * up)
    return r

@memoize
def decompose(n):
    """Retourne un <generator object> permettant d'obtenir la decomposition
    de n en nombres premiers.
    <!> : dans ce cas, ne sont consideres comme premier seul les nombres
    permiers compris entre 2 et 101 (tous deux inclus).

    >>> list(decompose(20))
    [2, 2, 5]
    """
    for p in PRIMES:
        if p**2 > n:
            break
        while not n % p:
            yield p
            n //= p
    if n > 1:
        yield n

def est_anagrame(w1, w2, tlr=0):
    """Retourne True sir w1 est un anagrame de w2
    avec une tolerance d'erreur fixee par tlr.

    >>> est_anagrame("OLIVIER", "VOILIER") #tlr == 0
    True
    >>> est_anagrame("VOILER", "OLIVIER", tlr=0)
    False
    >>> est_anagrame("VOILER", "OLIVIER", tlr=1)
    True
    """
    w1, w2 = compute_hash(w1), compute_hash(w2)
    if not tlr:
        return w1 == w2
    p = pgcd(w1, w2)
    t = len(list(decompose(w1 // p)))
    if t > tlr:
        return False
    return t + len(list(decompose(w2 // p))) <= tlr

def est_presque_anagramme(w1, w2, n):
    return est_anagrame(w1, w2, tlr=n)


@memoize
def best(ln):
    d = {}
    for c in dictionnaire:
        if c[1] == ln:
            ldc = len(dictionnaire[c])
            if ldc in d:
                d[ldc].append(c)
            else:
                d[ldc] = [c]
    return [dictionnaire[c] for c in d[max(d)]]

@memoize
def compose(word_key, by_key, tlr=0):
    """Retourne True si pour les keys de type (hash_number, len) on a bien
    word_key qui est compose par by_key avec un excedent de lettre de tlr.

    >>> compose((compute_hash("OLIVIER"), 7), (compute_hash("OLIVE"), 5)) #tlr == 0
    True
    >>> compose((compute_hash("OLIVIER"), 7), (compute_hash("OLIVIA"), 6), tlr=0)
    False
    >>> compose((compute_hash("OLIVIER"), 7), (compute_hash("OLIVIA"), 6), tlr=2)
    True
    """
    #if word_key[1] < by_key[1]: #ne pas utiliser ? cf AVION et CAMION
    #    return False
    if not tlr:
        return word_key[0] % by_key[0] == 0
    p = by_key[0] // pgcd(word_key[0], by_key[0]) #utiliser compose_with_error ?
    return len(list(decompose(p))) <= tlr

def compose_with_error(word_key, by_key):
    """Retourne un entier qui dit combien d'eerreur(s) il faudrait retirer
    a by_key pou que by_key soit un sous ensemble de word_key.

    >>> compose_with_error((compute_hash("OLIVIER"), 7), (compute_hash("OLIVE"), 5))
    0 #olive est un sous ensemble de olivier
    >>> compose_with_error((compute_hash("AVION"), 7), (compute_hash("CAMION"), 5))
    2 #il faut retirer le M et le C pour que camion soit un sous ensemble de avion
    """
    p = by_key[0] // pgcd(word_key[0], by_key[0])
    return len(list(decompose(p)))

#@memoize #fait perdre du temps
def nb_permutations(word):
    """Retourne le nombre de permutations possibles d'un mot.

    >>> nb_permutations("AAB")
    3
    >>> nb_permutations("ABC")
    6
    """
    num = factorial(len(word))
    mults = Counter(word).values()
    den = reduce(operator.mul, (factorial(v) for v in mults), 1)
    return int(num / den)

def anagrammes_maximaux():
    """Retourne la liste de mot etant des anagrammes maximaux.
    Un anagramme maximal, est un mot qui a autant d'anagrammes
    que de permutations possibles de ses lettres."""
    L = []
    for key in dictionnaire:
        if len(dictionnaire[key]) == nb_permutations(dictionnaire[key][0]):
            L.append(dictionnaire[key][0])
    return L


def r(word_key, keys, tlr=0, erreur_cumulee=0):
    if word_key[1] == 0:
        return
    for k in keys:
        if compose(word_key, k, max(0, tlr - erreur_cumulee)):
            new_erreur_cumulee = erreur_cumulee + compose_with_error(word_key, k)
            new_tlr = tlr - new_erreur_cumulee
            print(str(k) + ", " + str(new_tlr) + " -> " + str(dictionnaire[k]))




s = time()
dictionnaire = {}
for v in open(DICO_PATH, 'r').read().split(chr(10)):
    ch = compute_hash(v)
    lv = len(v)
    if (ch, lv) in dictionnaire:
        dictionnaire[(ch, lv)].append(v)
    else:
        dictionnaire[(ch, lv)] = [v]
try:dictionnaire.pop((1, 0))
except: pass
s = time() - s
print(s)

s=time();best(4);s=time()-s;
print(s)
s=time();best(4);s=time()-s;
print(s)

import random
s=time();[pgcd(random.randrange(0, 500), random.randrange(0, 500)) for i in range(100000)];s=time()-s
print(s)
