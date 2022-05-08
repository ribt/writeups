# Never Skip Class Nor Squaring

Difficulté : :star::star:

Énoncé :

> Nous avons accès à un serveur qui permet de signer des messages avec RSA. Lors de la connexion, ce serveur nous transmet un message chiffré que nous voulons déchiffrer.
>
> Le serveur est compromis et il est possible d'injecter des *glitchs* pour sauter les opérations **de mise au carré** dans l'algorithme *square and multiply* utilisé pour réaliser l'exponentiation modulaire du RSA.
>
> Retrouvez la clé de déchiffrement et récupérez le message.
>
> `nc challenges.france-cybersecurity-challenge.fr 2255`

Fichier : [nscns.py](./nscns.py)



### Théorie 

Ce challenge est vraiment très similaire [au challenge précédent](../nscnm/README.md) donc je vous invite à d'abord lire l'autre write-up avant de revenir ici :slightly_smiling_face:

Voici la seule fonction qui diffère

```python
def exp_mod_skip_squ(x, y, n, skip = -1):
    fmt = f"{{:0{2*BITS}b}}"
    exp = fmt.format(y)

    value = 1
    for i, e in enumerate(exp):
        if skip != i:
            value *= value
        if e == "1":
            value *= x
        value %= n
    return value
```



Cette fois-ci on a le pouvoir de dire *à telle étape de l'exponentiation, tu ne mets pas le résultat au carré*. Cela va donc impacter toute la suite du calcul. 



### Résolution

La résolution est exactement similaire au challenge précédent sauf qu'au lieu de comparer toutes les valeurs à la référence demandée au début, on compare chaque réponse du serveur avec la précédente qu'il avait donnée :

```python
from pwn import remote

BITS = 512

conn = remote("challenges.france-cybersecurity-challenge.fr", 2255)

n = int(conn.recvline().decode().strip()[4:])
e = int(conn.recvline().decode().strip()[4:])

conn.recvuntil("= ")

msg = 42
conn.send(str(msg)+"\n")
conn.recvuntil("= ")
conn.send("0\n")

ref = int(conn.recvline().decode().strip())
ans = ""

for i in range(1, 2 * BITS + 1):
    conn.recvuntil("= ")
    conn.send(str(msg)+"\n")
    conn.recvuntil("= ")
    conn.send(str(i)+"\n")
    t = int(conn.recvline().decode().strip())
    if t != ref:
        ans +="1"
    else:
        ans += "0"
    ref = t
    print(ans)

d = int(ans, 2)
c = int(conn.recvline().decode().strip()[4:])

conn.close()

m = pow(c, d, n)

print(bytes.fromhex(hex(m)[2:]).decode())
```

