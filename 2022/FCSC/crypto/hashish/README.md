# Hash-ish

Difficulté : :star::star:

Énoncé :

>Savez-vous comment fonctionne la fonction `hash` de Python ?
>
>`nc challenges.france-cybersecurity-challenge.fr 2103`

Fichier : [hashish.py](./hashish.py)



 ### Découverte

Regardons le programme fourni :

```python
#!/usr/bin/env python3.9
import os

try:
	flag = open("flag.txt", "rb").read()
	assert len(flag) == 70

	flag = tuple(os.urandom(16) + flag)

	challenge = hash(flag)
	print(f"{challenge = }")

	a = int(input(">>> "))
	b = int(input(">>> "))

	if hash((a, b)) == challenge:
		print(flag)
	else:
		print("Try harder :-)")
except:
	print("Error: please check your input")
```

En résumé, nous devons trouver deux entiers `a` et `b` tels que `hash((a, b)) == challenge`, cela est cohérent avec l'énoncé du challenge :slightly_smiling_face:



Tout d'abord cherchons quelque chose du style *python tuple hash collision* sur notre moteur de recherche préféré.

On tombe rapidement sur ces deux liens :

- https://bugs.python.org/issue34751
- https://stackoverflow.com/questions/49722196/how-does-python-compute-the-hash-of-a-tuple

Le 1er se plaint que la collision est trop facile et le 2e contient une réponse qui pointe vers le code C qui calcule le hash d'un tuple ! Cependant on voit que le lien pointe vers la branche `3.7` alors que le [shebang](https://fr.wikipedia.org/wiki/Shebang) de notre fichier indique clairement que c'est la version `3.9` qui est utilisée. Nous regardons donc [le code sur cette branche](https://github.com/python/cpython/blob/3.9/Objects/tupleobject.c#L359) et il a en effet subi d'importantes modifications par rapport à la 3.7 pour rendre les collisions plus difficiles.

Voici un extrait du code :

```c
#define _PyHASH_XXPRIME_1 ((Py_uhash_t)11400714785074694791ULL)
#define _PyHASH_XXPRIME_2 ((Py_uhash_t)14029467366897019727ULL)
#define _PyHASH_XXPRIME_5 ((Py_uhash_t)2870177450012600261ULL)
#define _PyHASH_XXROTATE(x) ((x << 31) | (x >> 33))  /* Rotate left 31 bits */

static Py_hash_t
tuplehash(PyTupleObject *v)
{
    Py_ssize_t i, len = Py_SIZE(v);
    PyObject **item = v->ob_item;

    Py_uhash_t acc = _PyHASH_XXPRIME_5;
    for (i = 0; i < len; i++) {
        Py_uhash_t lane = PyObject_Hash(item[i]);
        if (lane == (Py_uhash_t)-1) {
            return -1;
        }
        acc += lane * _PyHASH_XXPRIME_2;
        acc = _PyHASH_XXROTATE(acc);
        acc *= _PyHASH_XXPRIME_1;
    }

    /* Add input length, mangled to keep the historical value of hash(()). */
    acc += len ^ (_PyHASH_XXPRIME_5 ^ 3527539UL);

    if (acc == (Py_uhash_t)-1) {
        return 1546275796;
    }
    return acc;
}
```



N'étant pas très à l'aise en C, je vais traduire ce bout de code en Python. Le truc c'est que la taille des entiers est automatiquement adaptée en Python donc il faut sans arrêt appliquer un modulo $$ 2^{64} $$ à notre nombre.

```python
def tuple_hash(tup):
    acc = 2870177450012600261
    for i in range(len(tup)):
        lane = hash(tup[i])
        if lane == -1:
            return -1
        acc += lane * 14029467366897019727
        acc %= 2**64
        acc = ((acc << 31) | (acc >> 33))
        acc %= 2**64
        acc *= 11400714785074694791
        acc %= 2**64
    acc += len(tup) ^ (2870177450012600261 ^ 3527539)
    acc %= 2**64
    if acc == -1:
        return 1546275796
    return acc
```

Je vérifie que `tuple_hash((41, 42)) == hash((41, 42))` et ça fonctionne !



### Résolution

Notre tuple à hasher étant forcément de longueur 2, on peut même simplifier le code :

```python
def tuple_hash(a, b):
    acc = 2870177450012600261
    acc += a * 14029467366897019727
    acc %= 2**64
    acc = (((acc << 31)) | (acc >> 33))
    acc %= 2**64
    acc *= 11400714785074694791
    acc %= 2**64
    acc += b * 14029467366897019727
    acc %= 2**64
    acc = (((acc << 31)) | (acc >> 33))
    acc %= 2**64
    acc *= 11400714785074694791
    acc %= 2**64
    acc += 2 ^ (2870177450012600261 ^ 3527539)
    acc %= 2**64
    return acc
```

Certains modulos sont probablement inutiles mais on va les laisser par sécurité :wink:

Les plus attentifs auront remarqué que j'ai remplacé `hash(a)` par `a` et `hash(b)` par `b`. En effet, je n'ai pas pris le temps de comprendre comment Python calcule le hash d'un int mais j'ai pu remarqué que pour des valeurs inférieures à $$ 2^{62} $$ le hash renvoie le nombre lui-même. 



#### La solution miracle...

Plus qu'à mettre tout ça dans un solveur z3 :

```python
from z3 import *

a, b = BitVecs("a b", 64)
s = Solver()

challenge = 6422662251806978451  # TODO: récupérer le challenge avec netcat
if challenge < 0:
    challenge += 2**64

s.add(tuple_hash(a, b) == challenge)
print(s.check())
m = s.model()
print("a =", m[a])
print("b =", m[b])
```

La plupart du temps z3 nous dit qu'il a résolu le problème... mais ses solutions ne satisfont pas l'équation ! J'ai essayé plein de façons différente d'ajouter l'équation dans le solveur mais cela ne fonctionne jamais



#### ... la solution manuelle

Reprenons notre calcul de hash (écrite ici sans les modulos pour plus de lisibilité) :

```python
def tuple_hash(a, b):
    acc = 2870177450012600261
    acc += a * 14029467366897019727
    acc = (((acc << 31)) | (acc >> 33))
    acc *= 11400714785074694791
    acc += b * 14029467366897019727
    acc = (((acc << 31)) | (acc >> 33))
    acc *= 11400714785074694791
    acc += 2 ^ (2870177450012600261 ^ 3527539)
    return acc
```



Il faut maintenant faire l'inverse de cette fonction. Voici les étapes opposées dans l'odre inverse :

```
acc -= 2 ^ (2870177450012600261 ^ 3527539)
acc /= 11400714785074694791
acc = (((acc >> 31)) | (acc << 33))
acc -= b * 14029467366897019727
acc /= 11400714785074694791
acc = (((acc >> 31)) | (acc << 33))
acc -= a * 14029467366897019727
acc == 2870177450012600261
```

Les additions sont remplacées par des soustractions. Les multiplications seront remplacées par des *divisions modulaires* c'est à dire des multiplications par [l'inverse modulaire](https://fr.wikipedia.org/wiki/Inverse_modulaire). Et le décalage de 31 bits vers la gauche devient un décalage de 31 bits vers la droite.



En simplifiant les constantes et en extrayant `a`, cela donne :

```
acc -= 2870177450013471924
acc /= 11400714785074694791
acc = (((acc >> 31)) | (acc << 33))
acc -= b * 14029467366897019727
acc /= 11400714785074694791
acc = (((acc >> 31)) | (acc << 33))
acc -= 2870177450012600261
a = acc / 14029467366897019727
```



L'idée est donc de fixer arbitrairement une valeur pour `b` et de calculer la valeur de `a` correspondante. Plus exactement on va essayer plein de valeurs de `b` jusqu'à trouver une solution `a` égale à son hash.



Voici le code final :

```python
from pwn import remote

conn = remote("challenges.france-cybersecurity-challenge.fr", 2103)
conn.recvuntil(b"challenge = ")

challenge = int(conn.recvline().decode().strip())
if challenge < 0:
    challenge += 2**64

for b in range(999999):
    chall = challenge
    chall -= 2870177450013471924
    chall %= 2**64
    chall *= pow(11400714785074694791, -1, 2**64)
    chall %= 2**64
    chall = ((chall >> 31) | (chall << 33))
    chall %= 2**64
    chall -= b * 14029467366897019727
    chall %= 2**64
    chall *= pow(11400714785074694791, -1, 2**64)
    chall %= 2**64
    chall = ((chall >> 31) | (chall << 33))
    chall %= 2**64
    chall -= 2870177450012600261
    chall %= 2**64
    a = (chall * pow(14029467366897019727, -1, 2**64))%2**64
    if hash(a) == a:
        break
conn.recvuntil(b">>> ")
conn.send(str(a).encode()+b"\n")
conn.recvuntil(b">>> ")
conn.send(str(b).encode()+b"\n")
flag = bytes(map(int, conn.recvline().decode().strip()[1:-1].split(", ")))
print(flag[16:].decode())
```

flag : `FCSC{658232b18ebebc53c42dd373c6e9bc788f1fd5693cf8a45bcafbff46dae42e24}`
