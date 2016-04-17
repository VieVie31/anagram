from time import *
from math import factorial
from collections import Counter

def check_word(reference, possible):
    tmp = reference[:]
    
    for c in possible:  # enough characters
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
 
def gen_anagram(anagram, possible_words):
    for word in possible_words:
        x = check_word(anagram, word)
        if x == True:
            yield [word]
        elif x:
            for y in gen_anagram(x, possible_words):
                yield [word] + y


dictionary = open("ods.txt").readlines()
anagram = ''.join(sorted("CHAMPOLLOIN"))
possible_words = set() #plus rapide

lexique = {}

for word in dictionary:
    
    word = word.upper().strip()
    #if len(word) < 4: 
    #    continue

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

print "go"
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
print "nombre de combinaisons possible : ", c
print "trouve en : ", start
print '=' * 30
print "solutions :"

def perms(L, sol=[]):
    if len(L) == 1:
        for v in lexique[L[0]]:
            sol.append(v)
            print " ".join(sol)
            sol.remove(v)
    else:
        k = L[-1]
        for k in lexique[k]:
            sol.append(k)
            perms(L[:-1], sol)
            sol.remove(k)
            
for L in res:
    L = list(L)
    perms(L)
