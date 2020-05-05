# Quarantaine - 25 pts - 157 solves

Voici l'énoncé :

![Un de vos collègues a trouvé ce schéma de circuit électronique (circuit.pdf) dans une notice d'un produit et vous demande de l'aide pour le comprendre. La notice mentionne une fonction f appliquée à des nombres entiers, et donne un exemple f(19) = 581889079277. Votre collègue a besoin de trouver x tel que f(x) = 454088092903.](./enonce.png "énoncé")

Je vais utiliser un outil en ligne pour convertir le PDF en JPG et je vais l'analyser avec... GIMP pour pouvoir faire des points de couleur.

Ce circuit paraît à première vue très complexe : 40 entrées, 40 sorties et plein de portes compliquées. Mais on se rend vite compte que c'est le même bloc qui est copié partout. Après un rapide tour sur [Wikipedia](https://fr.wikipedia.org/wiki/Fonction_logique#Repr%C3%A9sentation_graphique) pour me remémorer les symboles, je fais la table de vérité du bloc récurent à droite. Il n'y a que deux entrées dont 4 combinaisons à tester, cela va vite avec GIMP et mes points rouges et bleus. On obtient la table de vérité suivante :
| e0 | e1 | s0 |
|:--:|:--:|:--:|
| 0  | 0  | 0  |
| 0  | 1  | 1  |
| 1  | 0  | 1  |
| 1  | 1  | 0  |

On peut donc simplifier ce gros bloc par un simple XOR !

On répète l'opération avec le bloc récurent à gauche (qui lui a deux sorties) et l'on obtient cela :
| e0 | e1 | s0 | s1 |
|:--:|:--:|:--:|:--:|
| 0  | 0  | 0  | 0  |
| 0  | 1  | 1  | 0  |
| 1  | 0  | 0  | 1  |
| 1  | 1  | 1  | 1  |

Cela revient donc simplement à croiser les fils !

Le circuit est grandement simplifié mais il faut remarquer auyre chose.

Oon constate que `x0` est xoré à lui-même. Cela fait donc forcément `0` ! On peut donc compléter une bonne partie du circuit qui est constante. Ensuite, le bloc en `x39` est presque identique au bloc récurent de droite mais sans l'inverseur final, c'est donc un NXOR. `x39 NXOR x39` cela fait forcément `1` donc on peut de nouveau compléter tout ce qui est lié au fil sortant de ce bloc.

On se rend compte que des inverseurs sont répartis le long de ces fils à valeur constante ce qui fait qu'un signal constant entre dans chaque XOR à droite. Et cela fait comme une clé que l'on XOR aux bits de `x` mais après les avoir légèrement mélanger. Cela fait :

```
y0 = x0 ^ 0
y1 = x2 ^ 0
y2 = x1 ^ 0
y3 = x4 ^ 0
y4 = x3 ^ 0
y5 = x6 ^ 1
y6 = x5 ^ 1
y7 = x8 ^ 1
y8 = x7 ^ 1
y9 = x10 ^ 1
y10 = x9 ^ 1
```

On pourrait continuer ainsi mais c'est long et chiant donc on va faire un script.

La clé constante est `0000011111101101010100101101111011100001`, de haut en bas. Le script simulant tout le circuit est donc :
```Python
x = [int(b) for b in "{:040b}".format(int(input("> ")))[::-1]]
y = [int(b) for b in "0"*40]

key = [int(b) for b in "0000011111101101010100101101111011100001"]

for i in range(40):
    if i == 0 or i == 39 :
        y[i] = x[i] ^ key[i]
    elif i%2 == 0:
        y[i] = x[i-1] ^ key[i]
    else:
        y[i] = x[i+1] ^ key[i]

print(int("".join([str(i) for i in y])[::-1], base=2))
```

On peut essayer et l'on retrouve bien `f(19) = 581889079277` !

Il ne reste plus qu'à faire un script qui fait le processus à l'envers :
```Python
y = [int(b) for b in "{:040b}".format(int(input("> ")))[::-1]]
x = [int(b) for b in "0"*40]

key = [int(b) for b in "0000011111101101010100101101111011100001"]

for i in range(40):
    if i == 0 or i == 39 :
        x[i] = y[i] ^ key[i]
    elif i%2 == 0:
        x[i] = y[i-1] ^ key[i-1]
    else:
        x[i] = y[i+1] ^ key[i+1]

print(int("".join([str(i) for i in x])[::-1], base=2))
```

Et ça marche !

