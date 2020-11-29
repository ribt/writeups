# Decryptor - 50 pts

> Un secret chiffré par le serveur suivant à été intercepté. D'apès les premières analyses de nos experts, ce serveur déchiffre tous ce que vous lui donnez, sauf le flag chiffré ! Nous avons besoin de vous pour réussir à tout de même déchiffrer ce secret !
>
> decryptor.interiut.ctf:1337
>
> - [public.pem](./public.pem)
> - [secret](./secret)

Nous avons une clé RSA publique et un nombre à décrypter. La clé fait 2048 bits, il est illusoire d'imaginer la casser.

Il faut probablement chercher du côté du serveur que l'on nous fournit et qui déchiffre tous les messages que l'on veut sauf notre numéro `secret` qui correspond au flag chiffré. Essayons de voir comment nous pourront exploiter cela. Le serveur demande un chiffre et ne réagit pas aux lettres ni aux nombres à virgule... mais il répond si on lui passe un nombre négatif !

Pour comprendre la suite, il est nécessaire de connaître la notion de *modulo* (reste dans la division euclidienne) et le [fonctionnement du RSA](https://fr.wikipedia.org/wiki/Chiffrement_RSA#Fonctionnement_d%C3%A9taill%C3%A9). Pour rappel, la clé publique contient les nombres `n` et `e`. Si `M` est le message en clair et `C` le message chiffré, nous faisons ce calcul pour chiffrer un message :

![M^e = C mod n](https://render.githubusercontent.com/render/math?math=M^e%20\equiv%20C%20\mod%20n)

Le serveur connaît un nombre `d`, incalculable pour nous, tel que :

![C^d = M mod n](https://render.githubusercontent.com/render/math?math=C^d%20\equiv%20M%20\mod%20n)

Si l'on envoie `-1` à déchiffrer par exemple, le serveur répond un nombre égal à `n - 1` car (`d` étant impair) :

![(-1)^d = -1 mod n](https://render.githubusercontent.com/render/math?math=(-1)^d%20\equiv%20-1%20\mod%20n)

Le reste dans la division euclidienne ne peut pas être négatif donc le serveur ajoute `n` une fois pour avoir un nombre tel que `0 <= C < n`.

Il suffit donc d'envoyer l'opposé de notre nombre secret et on pourra déduire le flag car :

![](https://render.githubusercontent.com/render/math?math=%5Cbegin%7Balign%7D%28-C%29%5Ed%20%5Cequiv%20-%28C%5Ed%29%20%5Cmod%20n%20%5Cnonumber%20%5C%5C%28-C%29%5Ed%20%5Cequiv%20-M%20%5Cmod%20n%20%5Cnonumber%20%5C%5C%28-C%29%5Ed%20%5Cequiv%20n%20-%20M%20%5Cmod%20n%20%5Cnonumber%20%5C%5C%5Cend%7Balign%7D)

Si on envoie `-secret`, le serveur nous répond `n - flag` !

Pour la forme je fais un joli script :

```python
from Crypto.PublicKey import RSA
from pwn import remote

with open("public.pem") as f:
    key = RSA.import_key(f.read())

with open("secret") as f:
    secret = f.read()

conn = remote("decryptor.interiut.ctf", 1337)

conn.send(b'-'+secret.encode())

flag = key.n - int(conn.recvline().decode()[:-1])

conn.close()

print(flag.to_bytes(39, 'big').decode())
```



