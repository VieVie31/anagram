from p11 import *

def presque_anagrammes(word, tlr):
    """Prend en marametre un mot word et un entier tlr (comme tolerance a l'erreur)
    avec tlr >= 0 et renvoie la de tous les n-presque-anagrammes."""
    L = []
    word_key, word_ln = hash_dict(word)
    for k, ln in  dictionnaire:
        if abs(ln - word_ln) == tlr:
            p = pgcd(word_key, k)
            d_sups = list(decompose(k // p))
            word_sups = list(decompose(word_key // p))
            if len(d_sups) + len(word_sups) == tlr:
                L.extend(dictionnaire[(k, ln)])
    return L

def est_presque_anagramme(w1, w2, n):
    return est_anagrame(w1, w2, tlr=n)



dictionnaire = load_lexicon()
