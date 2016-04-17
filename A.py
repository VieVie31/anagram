from time import *
from math import factorial
from collections import Counter

dictionary = open("ods.txt").readlines()

print("dictionnaire charge...")

def check_word(reference, possible):
    """Fonction equivalente a ajout_possible quand on faisait les TP"""
    tmp = reference[:]
    
    for c in possible: #assez de caracteres
        if c not in reference:
            return False
        else:
            try:
                tmp.remove(c)
            except:
                return False
    if tmp == []:
        return True
    else: 
        return tmp

nb_sols = 0

def A1(mon_mot):
    """Prend un mot et affiche la liste des mots anagrammes du mot de depart
    si la variable DEBUG est a True sinon fait juste les caulcus et met dans
    la variable global nb_sols le nombre de solutions qui a ete trouve..."""
    global nb_sols
    
    def gen_anagram(anagram, possible_words):
        """La vraie fonction qui nous interresse qui genere
        recursivement les anagrammes"""
        for word in possible_words:
            x = check_word(anagram, word)
            if x == True:
                yield [word]
            elif x:
                for y in gen_anagram(x, possible_words):
                    yield [word] + y

    
    anagram = ''.join(sorted(mon_mot))
    possible_words = set() 
    lexique = {}

    for word in dictionary:
        word = word.upper().strip()
        key = ''.join(sorted(word))

        #contruire le lexique
        if key in lexique:
            lexique[key].append(word)
        else:
            lexique[key] = [word]

        #continuer a couper des branches
        tmp = list("".join(anagram.split()))
        skip = False
        for c in word:
            if c not in anagram:
                skip = True
                continue
            else:
                try:
                    tmp.remove(c)
                except:
                    skip = True
                    continue
        if skip:
            continue
        else:
            possible_words.add(key) #avant word mais keys compresse et va plus vite


    anagram = [x for x in anagram.strip() if x != ' ']

    start = time()

    res = set()
    for x in gen_anagram(anagram, possible_words):
        res.add(tuple(sorted(x)))

    c = 0
    for s in res:
        t = 1
        for k in s:
            t *= len(lexique[k])
        c += t
            
    start = time() - start
    nb_sols = c
    if DEBUG:
        print("nombre de combinaisons possible : ", c)
        print("trouve en : ", start)
        print('=' * 30)
        print("solutions :")

    def perms(L, sol=[]):
        "Recree tous les anagrammes a partir des clefs choisies par gen_anagrams"
        if len(L) == 1:
            for v in lexique[L[0]]:
                sol.append(v)
                print(" ".join(sol))
                sol.remove(v)
        else:
            k = L[-1]
            for k in lexique[k]:
                sol.append(k)
                perms(L[:-1], sol)
                sol.remove(k)
                
    for L in res:
        L = list(L)
        if DEBUG:
            perms(L)



def A2(mon_mot, nb_mots):
    """Prend un mot et affiche la liste des mots anagrammes du mot de depart
    constituees au plus de n mots si la variable DEBUG est a True sinon fait
    juste les caulcus et met dans la variable global nb_sols le nombre
    de solutions qui a ete trouve..."""
    global nb_sols
    
    def gen_anagram(anagram, possible_words, limit=0, rec=0):
        """La vraie fonction qui nous interresse qui genere
        recursivement les anagrammes"""
        for word in possible_words:
            x = check_word(anagram, word)
            if x == True:
                yield [word]
            elif x and rec < limit:
                    for y in gen_anagram(x, possible_words, limit-1, rec+1):
                        if len(y) < limit:
                            yield [word] + y

    anagram = ''.join(sorted(mon_mot))
    possible_words = set() 
    lexique = {}

    for word in dictionary:
        word = word.upper().strip()
        key = ''.join(sorted(word))

        #contruire le lexique
        if key in lexique:
            lexique[key].append(word)
        else:
            lexique[key] = [word]

        #continuer a couper des branches
        tmp = list("".join(anagram.split()))
        skip = False
        for c in word:
            if c not in anagram:
                skip = True
                continue
            else:
                try:
                    tmp.remove(c)
                except:
                    skip = True
                    continue
        if skip:
            continue
        else:
            possible_words.add(key) #avant word mais keys compresse et va plus vite


    anagram = [x for x in anagram.strip() if x != ' ']

    start = time()

    res = set()
    for x in gen_anagram(anagram, possible_words, nb_mots):
        res.add(tuple(sorted(x)))

    c = 0
    for s in res:
        t = 1
        for k in s:
            t *= len(lexique[k])
        c += t
            
    start = time() - start
    nb_sols = c
    if DEBUG:
        print("nombre de combinaisons possible : ", c)
        print("trouve en : ", start)
        print('=' * 30)
        print("solutions :")

    def perms(L, sol=[]):
        "Recree tous les anagrammes a partir des clefs choisies par gen_anagrams"
        if len(L) == 1:
            for v in lexique[L[0]]:
                sol.append(v)
                print(" ".join(sol))
                sol.remove(v)
        else:
            k = L[-1]
            for k in lexique[k]:
                sol.append(k)
                perms(L[:-1], sol)
                sol.remove(k)
                
    for L in res:
        L = list(L)
        if DEBUG:
            perms(L) #on affiche les solutions


def fun_nb_sols():
    global nb_sols
    return nb_sols

if __name__ == "__main__":
    DEBUG = True #on affiche les resultats trop styles !! :D
else: #bein on affiche aps tout pour les tests unitaires
    DEBUG = False
