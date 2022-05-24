# Never Skip Class Nor Multiplication

Difficulté : :star:

Énoncé :

> Nous avons accès à un serveur qui permet de signer des messages avec RSA. Lors de la connexion, ce serveur nous transmet un message chiffré que nous voulons déchiffrer.
>
> Le serveur est compromis et il est possible d'injecter des *glitchs* pour sauter les opérations **de multiplication** dans l'algorithme *square and multiply* utilisé pour réaliser l'exponentiation modulaire du RSA.
>
> Retrouvez la clé de déchiffrement et récupérez le message.
>
> `nc challenges.france-cybersecurity-challenge.fr 2254`

Fichier : [nscnm.py](./nscnm.py)



### Théorie 

Avant de commencer il faut être au point [le chiffrement RSA](https://fr.wikipedia.org/wiki/Chiffrement_RSA) mais si ça n'est pas le cas, on peut toujours deviner son fonctionnement grâce au code fourni :

```python
from Crypto.Util.number import getStrongPrime, bytes_to_long

BITS = 512

def exp_mod_skip_mul(x, y, n, skip = -1):
    fmt = f"{{:0{2*BITS}b}}"
    exp = fmt.format(y)

    value = 1
    for i, e in enumerate(exp):
        value *= value
        if e == "1":
            if skip != i:
                value *= x
        value %= n
    return value

if __name__ == "__main__":

    p, q = getStrongPrime(BITS), getStrongPrime(BITS)
    n = p * q
    e = 2 ** 16 + 1
    d = pow(e, -1, (p - 1) * (q - 1))

    print(f"{n = }")
    print(f"{e = }")

    try:
        for _ in range(2 * BITS + 1):
            msg = bytes_to_long(input("msg = ").encode())
            if msg == 0:
                break
            skip = int(input("skip = "))
            print(exp_mod_skip_mul(msg, d, n, skip))
    except:
        print("Please check your inputs.")
        exit(0)

    with open("flag.txt", "rb") as fp:
        m = bytes_to_long(fp.read())
        c = pow(m, e, n)
        print(f"{c = }")

```



La clé privée fait 1024 bits et on a le droit de poser 1025 questions au serveur, cela rappelle [un certain challenge misc](../../misc/guessme2/README.md)...

Dans le chiffrement RSA on a toujours besoin de mettre un nombre *exposant* un autre *modulo* un troisième. Tous ces nombres étant gigantesques (ordre de grandeur : $$ 2^{1024} $$) on a du trouver un moyen de faire cette opération beaucoup plus efficace que la méthode naïve : c'est [l'exponentiation modulaire](https://fr.wikipedia.org/wiki/Exponentiation_modulaire). Il se trouve que par hasard j'ai eu l'occasion de faire un oral sur le sujet cette année alors voici quelques slides pour aider à comprendre le principe :

![slide1](slide1.png)

![slide2](slide2.png)



La différence ici c'est qu'on a le droit de passer une étape dans l'exponentiation modulaire. La fonction `exp_mod_skip_mul` est appelée pour mettre  notre message à la puissance `d` (la clé privée) modulo `n` (la clé publique) et on peut lui dire *fais comme si le bit n°i de la clé privée était égal à `0`*.



### Résolution

La stratégie consiste donc a toujours envoyé le même message au serveur en faisant varier le paramètre skip. Au début on met `-1` pour avoir la vraie valeur de $$ msg ^ {d} \pmod n$$. Ensuite on va faire varier `skip` de 0 à 1023. Si le serveur nous répond la même chose que la 1ère fois alors le bit n°skip de la clé privée est à `0` sinon il est à `1`.

En Python, cela s'écrit :

```python
from pwn import remote

BITS = 512

conn = remote("challenges.france-cybersecurity-challenge.fr", 2254)

n = int(conn.recvline().decode().strip()[4:])
e = int(conn.recvline().decode().strip()[4:])

conn.recvuntil("= ")

msg = 42
conn.send(str(msg)+"\n")
conn.recvuntil("= ")
conn.send("-1\n")

ref = int(conn.recvline().decode().strip())
ans = ""

for i in range(2 * BITS):
    conn.recvuntil("= ")
    conn.send(str(msg)+"\n")
    conn.recvuntil("= ")
    conn.send(str(i)+"\n")
    t = int(conn.recvline().decode().strip())
    if t != ref:
        ans +="1"
    else:
        ans += "0"
    print(ans)

d = int(ans, 2)
c = int(conn.recvline().decode().strip()[4:])

conn.close()

m = pow(c, d, n)

print(bytes.fromhex(hex(m)[2:]).decode())
```

Notre programme dessine une jolie série de 0 et 1 dans le terminal puis affiche le flag : `FCSC{c78e6725a5056d13b63cc4e8a98f6f6f7c6c091ecf0523377035d8faf203b20d}`

Le [challenge suivant](../nscns/README.md) est très similaire.
