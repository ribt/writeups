# Le SAGE doré - 20 pts

> Le vieux sage du village se rappelle avoir reçu un message  chiffré il y a longtemps par l'un de ses disciples, mais a  malheureusement depuis perdu la clé privé correspondante. Il a directement pensé à vous et pense que cet mission sera parfaite  pour débuter votre ascension vers la voie du SAGE, retrouvez la clé  privé ainsi que le contenu du message.
>
> Commencez votre aventure ici : https://tinyurl.com/y4qvu9lv
>
> Voilà quelques ressources pour vous aider dans cette tâche :
>
> - http://doc.sagemath.org/html/en/reference/cryptography/index.html
>
> - https://www.unilim.fr/pages_perso/vincent.jalby/resources/commun/IntroSage2.pdf

Le premier lien mène vers ce code :

```python
# CHALLENGE
from sage.crypto.public_key.blum_goldwasser import BlumGoldwasser
from sage.crypto.util import bin_to_ascii, ascii_to_bin

encrypted_flag = ([[1, 1, 1, 1, 0, 0], [1, 1, 1, 0, 1, 1], [1, 0, 1, 1, 1, 0], [0, 1, 1, 1, 0, 1], [0, 0, 0, 1, 1, 1], [0, 1, 0, 1, 1, 0], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 1, 1], [1, 0, 1, 0, 0, 0], [0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1], [1, 0, 0, 1, 0, 1], [1, 1, 1, 1, 0, 0], [0, 1, 1, 0, 0, 1], [1, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1], [1, 0, 0, 1, 0, 1]], 6049402465830679674781261764183)
pub_key = 8054793366550713418339620131461
```

On retrouve la page de la documentation correspondant à [sage.crypto.public_key.blum_goldwasser](https://doc.sagemath.org/html/en/reference/cryptography/sage/crypto/public_key/blum_goldwasser.html#module-sage.crypto.public_key.blum_goldwasser). La clé publique est le produit de deux nombres premiers. Vu la taille du nombre, [WolframAlpha](https://www.wolframalpha.com/input/?i=factorize+8054793366550713418339620131461) retrouve les facteurs : `1489304211816227` et `5408427171993143`. Ne reste plus qu'à décoder :

```python
bg = BlumGoldwasser()

p, q = 1489304211816227, 5408427171993143

print(bg.public_key(p, q)) # on retrouve bien la même clé publique

flag_bits = bg.decrypt(encrypted_flag, bg.private_key(p, q))

print(bin_to_ascii(flatten(flag_bits)))
```
