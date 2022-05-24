# Shuffled

Difficulté : :star:

Énoncé :

> Oops, nous avons mélangé les caractères du flag. Pourrez-vous les remettre dans l'ordre ?

Fichiers :

- [output.txt](./output.txt)
- [shuffled.py](./shuffled.py)



### Découverte

Le fichier texte contient en effet les caractères typiques d'un flag mais dans le mauvaise ordre :

```
f668cf029d2dc4234394e3f7a8S9f15f626Cc257Ce64}2dcd93323933d2{F1a1cd29db
```



et le fichier Python :

```python
import random

flag = list(open("flag.txt", "rb").read().strip())
random.seed(random.randint(0, 256))
random.shuffle(flag)
print(bytes(flag).decode())
```

 

Rien de bien compliqué : on initialise random avec une seed entre 0 et 256 puis on *shuffle* les caractères donc ça fait peut de combinaisons à tester.



### Résolution

Il va falloir comprendre comment fonctionne `random.shuffle` pour faire la fonction inverse pour une seed donnée. Pour cela pas besoin de regarder le code de random, il suffier de créer une liste d'éléments numérotés dans l'ordre, de la *shuffle* et on a une map qui décrit comment faire l'opération inverse. On fait cela pour les 257 possibilités et comme on sait que le flag commence  forcément par `FCSC{` il devrait y avoir peu de solutions :

```python
import random

output = open("output.txt").read().strip()

l = list(range(len(output))) # liste triée qui sera copiée et mélangée
flag = list("x"*len(output))

for s in range(257):
    nl = l[:]
    random.seed(s)
    random.shuffle(nl)

    for i in range(len(output)):
        flag[nl[i]] = output[i]
    if flag[:4] == list("FCSC"):
        print("".join(flag))
```

En effet, une seule chaîne de caractère est print :  `FCSC{d93d32485aec7dc7622f13cd93b922363911c36d2ffd4f829f4e3264d0ac6952}`
