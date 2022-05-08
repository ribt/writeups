# Échec OP

Tous ces challenges se jouent sur une image de disque de 10 Go que je ne vais pas mettre sur GitHub...

## Partie 0/3

Difficulté : intro

#### Énoncé

> Quel est l'identifiant unique (UUID) de la table de partition de ce disque ? Une fois que vous l'aurez trouvé, encadrez le dans `FCSC{}` pour obtenir le flag. Par exemple `FCSC{1111-2222-3333-4444}`.

#### Résolution

La commande de base pour avoir des infos sur un disque :

```
$ fdisk -l fcsc.raw
Disque fcsc.raw : 10 GiB, 10737418240 octets, 20971520 secteurs
Unités : secteur de 1 × 512 = 512 octets
Taille de secteur (logique / physique) : 512 octets / 512 octets
taille d'E/S (minimale / optimale) : 512 octets / 512 octets
Type d'étiquette de disque : gpt
Identifiant de disque : 60DA4A85-6F6F-4043-8A38-0AB83853E6DC

Périphérique   Début      Fin Secteurs Taille Type
fcsc.raw1       2048     4095     2048     1M Amorçage BIOS
fcsc.raw2       4096  1861631  1857536   907M Système de fichiers Linux
fcsc.raw3    1861632 20969471 19107840   9,1G Système de fichiers Linux
```

flag : `FCSC{60DA4A85-6F6F-4043-8A38-0AB83853E6DC}`



## Partie 1/3

Difficulté : :star:

#### Énoncé

> L'administrateur de ce serveur a chiffré son disque, le mot de passe est `fcsc2022`. Quelle est la date de la création du système de fichiers en `UTC` ? Le flag est au format `ISO 8601`, tel que dans l'exemple suivant : `FCSC{2022-04-22T06:59:59Z}`.

#### Résolution

Je commence par extraire les différentes partitions du disque à l'aide des infos de la commande précédente. Cela va me permettre de travailler sur une seule partition en gardant une copie du disque original.

```
$ dd if=fcsc.raw of=fcsc.raw1 bs=512 skip=2048 count=2048 status=progress
$ dd if=fcsc.raw of=fcsc.raw2 bs=512 skip=4096 count=1857536 status=progress
$ dd if=fcsc.raw of=fcsc.raw3 bs=512 skip=1861632 count=19107840 status=progress
```

On voit que la partition qui contient les fichiers est en effet chiffrée :

```
$ file fcsc.raw3
fcsc.raw3: LUKS encrypted file, ver 2 [, , sha256] UUID: 45e2f0c4-6640-453d-8b7a-8a60bd61c63d
```

On la monte :

```
$ sudo cryptsetup open --type luks fcsc.raw3 fcsc2022
```

Mais n'oublions pas que l'on cherche la date de création du système de fichier. En cherchant sur notre moteur de recherche préféré on trouve rapidement [un post StackOverflow](https://stackoverflow.com/questions/41240068/how-to-to-find-out-the-creation-time-of-the-filesystem-in-linux) qui se pose exactement la même question. Cependant, la commande proposée (`tune2fs`) ne marche pas sur la partition chiffrée. Essayons sur la partition n°2 :

```
$ sudo tune2fs -l fcsc.raw2
tune2fs 1.44.1 (24-Mar-2018)
Filesystem volume name:   <none>
Last mounted on:          /boot
Filesystem UUID:          427db55e-1263-43a4-9005-dfb083639311
Filesystem magic number:  0xEF53
Filesystem revision #:    1 (dynamic)
Filesystem features:      has_journal ext_attr resize_inode dir_index filetype extent 64bit flex_bg sparse_super large_file huge_file dir_nlink extra_isize metadata_csum
Filesystem flags:         signed_directory_hash 
Default mount options:    user_xattr acl
Filesystem state:         clean
Errors behavior:          Continue
Filesystem OS type:       Linux
Inode count:              58112
Block count:              232192
Reserved block count:     11609
Free blocks:              196899
Free inodes:              57800
First block:              0
Block size:               4096
Fragment size:            4096
Group descriptor size:    64
Reserved GDT blocks:      113
Blocks per group:         32768
Fragments per group:      32768
Inodes per group:         7264
Inode blocks per group:   454
Flex block group size:    16
Filesystem created:       Sun Mar 27 05:44:35 2022
Last mount time:          Sun Mar 27 19:28:30 2022
Last write time:          Sun Mar 27 23:51:46 2022
Mount count:              8
Maximum mount count:      -1
Last checked:             Sun Mar 27 05:44:35 2022
Check interval:           0 (<none>)
Lifetime writes:          133 MB
Reserved blocks uid:      0 (user root)
Reserved blocks gid:      0 (group root)
First inode:              11
Inode size:	          256
Required extra isize:     32
Desired extra isize:      32
Journal inode:            8
Default directory hash:   half_md4
Directory Hash Seed:      2f2e268d-6ddb-4519-b720-e261122bf2f9
Journal backup:           inode blocks
Checksum type:            crc32c
Checksum:                 0x27d43b44

```

Le flag `FCSC{2022-03-27T05:44:35Z}` ne passe pas :confused: Sans doute une histoire de fuseau horaire...

Je ne sais pas comment demander le fuseau horaire à `tune2fs` donc on va essayer de monter la partition et faire un `ls` car je sais que cette commande permet d'aficher le temps au format ISO.

```
$ sudo mkdir /mnt/fcsc2
$ sudo mount fcsc.raw2 /mnt/fcsc2
$ ls -l --time-style=full-iso --time=ctime /mnt/fcsc2/
total 100672
-rw-r--r-- 1 root root   237973 2022-03-27 05:45:34.680029702 +0200 config-5.4.0-105-generic
drwxr-xr-x 4 root root     4096 2022-03-27 05:46:10.212028535 +0200 grub
lrwxrwxrwx 1 root root       28 2022-03-27 05:45:44.496029379 +0200 initrd.img -> initrd.img-5.4.0-105-generic
-rw-r--r-- 1 root root 84394982 2022-03-27 05:46:06.492028657 +0200 initrd.img-5.4.0-105-generic
lrwxrwxrwx 1 root root       28 2022-03-27 05:45:44.496029379 +0200 initrd.img.old -> initrd.img-5.4.0-105-generic
drwx------ 2 root root    16384 2022-03-27 05:44:35.000000000 +0200 lost+found
-rw------- 1 root root  4759409 2022-03-27 05:45:34.680029702 +0200 System.map-5.4.0-105-generic
lrwxrwxrwx 1 root root       25 2022-03-27 05:45:44.496029379 +0200 vmlinuz -> vmlinuz-5.4.0-105-generic
-rw------- 1 root root 13664512 2022-03-27 05:45:35.472029676 +0200 vmlinuz-5.4.0-105-generic
lrwxrwxrwx 1 root root       25 2022-03-27 05:45:44.496029379 +0200 vmlinuz.old -> vmlinuz-5.4.0-105-generic
```

Tous les fichiers ont un décalage de +2h donc l'heure de `tune2fs` donnerait `FCSC{2022-03-27T03:44:35Z}` en UTC . Ce flag ne passe pas non plus :sob:

On remarque cependant que le fichier `lost+found` semble indiquer pile poil la même heure que celle de `tune2fs`. Essayons de voir si notre partition n°3 a un tel fichier :

```
$ ls -l --time-style=full-iso --time=ctime /media/ribt/20e4352b-6b51-4a6c-91ec-a0c76bfdea06/
total 1777748
lrwxrwxrwx   1 root root          7 2022-03-27 05:44:51.332031125 +0200 bin -> usr/bin
drwxr-xr-x   2 root root       4096 2022-03-27 05:44:50.412031155 +0200 boot
drwxr-xr-x   5 root root       4096 2022-03-27 05:44:51.332031125 +0200 dev
drwxr-xr-x 100 root root       4096 2022-03-27 23:39:07.554445479 +0200 etc
drwxr-xr-x   3 root root       4096 2022-03-27 05:49:23.153214128 +0200 home
lrwxrwxrwx   1 root root          7 2022-03-27 05:44:51.332031125 +0200 lib -> usr/lib
lrwxrwxrwx   1 root root          9 2022-03-27 05:44:51.332031125 +0200 lib32 -> usr/lib32
lrwxrwxrwx   1 root root          9 2022-03-27 05:44:51.332031125 +0200 lib64 -> usr/lib64
lrwxrwxrwx   1 root root         10 2022-03-27 05:44:51.332031125 +0200 libx32 -> usr/libx32
drwx------   2 root root      16384 2022-03-27 05:44:49.000000000 +0200 lost+found
drwxr-xr-x   2 root root       4096 2022-03-27 05:44:51.376031124 +0200 media
drwxr-xr-x   2 root root       4096 2022-03-27 05:44:51.376031124 +0200 mnt
drwxr-xr-x   2 root root       4096 2022-03-27 05:44:51.376031124 +0200 opt
drwxr-xr-x   2 root root       4096 2022-03-27 05:44:51.376031124 +0200 proc
drwx------   4 root root       4096 2022-03-27 06:14:39.169771855 +0200 root
drwxr-xr-x  11 root root       4096 2022-03-27 05:44:51.460031121 +0200 run
lrwxrwxrwx   1 root root          8 2022-03-27 05:44:51.332031125 +0200 sbin -> usr/sbin
drwxr-xr-x   6 root root       4096 2022-03-27 05:44:51.460031121 +0200 snap
drwxr-xr-x   2 root root       4096 2022-03-27 05:44:51.404031123 +0200 srv
-rw-------   1 root root 1820327936 2022-03-27 05:45:49.444029217 +0200 swap.img
drwxr-xr-x   2 root root       4096 2022-03-27 05:44:51.404031123 +0200 sys
drwxrwxrwt   9 root root       4096 2022-03-27 23:51:46.150479405 +0200 tmp
drwxr-xr-x  14 root root       4096 2022-03-27 05:44:51.460031121 +0200 usr
drwxr-xr-x  14 root root       4096 2022-03-27 06:13:45.793769799 +0200 var
```

Yes, et le flag `FCSC{2022-03-27T03:44:49Z}` passe !



## Partie 2/3

Difficulté : :star:

#### Énoncé

> Retrouvez le mot de passe de l'utilisateur principal de ce serveur. La force ne résout pas tout... Le mot de passe correspond au flag, entouré de `FCSC{}`, par exemple : `FCSC{password}`. Aussi, l'administrateur de ce serveur a chiffré son disque et le mot de passe est `fcsc2022`.

#### Essais infructueux

On récupère les fichiers `/etc/passwd` et `/etc/shadow` de la partition chiffrée, on utilise `unshadowed` pour transformer cela en hash pour JohnTheRipper et on lance ce dernier avec [rockyou.txt](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt). John annonce 23h pour tester toute la liste et vu l'énoncé ça serait peu probable que le mot de passe de l'admin soit dans cette liste :confused:

Ensuite je me balade dans les fichiers de config. Je vois un dossier `/etc/ssh` avec plein de clés privées mais impossible d'en tirer quoi que ce soit.

#### Résolution

Encore une fois je me résigne à faire un gros grep à la racine (avec le nom du seul utilisateur qui a un dossier dans `/home/`) :

```
$ sudo grep "obob" -r *
[...]
root/.bash_history:passwd obob 
[...]
```

Intéressant, regardons plus en détail :

```
$ sudo cat root/.bash_history
exit
passwd obob 
CZSITvQm2MBT+n1nxgghCJ
exit
```

Et voilà !

flag: `FCSC{CZSITvQm2MBT+n1nxgghCJ}`



## Partie 3/3

Difficulté : :star::star:

#### Énoncé

> L'administrateur semble avoir essayé de dissimuler l'une de ses adresses IP avec laquelle il a administré ce serveur. Aidez nous à retrouver cette adresse. Une fois l'IP trouvée, encadrez-la dans `FCSC{}` pour avoir le flag (par exemple : `FCSC{1.2.3.4}`).
>
> **Attention :** vous n'avez que 5 essais.

#### Essais infructueux

En regardant les logs de nginx on voit :

```
$ cat var/log/nginx/access.log 
172.16.123.130 - - [27/Mar/2022:21:44:19 +0000] "GET / HTTP/1.1" 200 396 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
172.16.123.130 - - [27/Mar/2022:21:44:19 +0000] "GET /favicon.ico HTTP/1.1" 404 134 "http://172.16.123.129/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
172.16.123.130 - - [27/Mar/2022:21:44:23 +0000] "GET /coucou HTTP/1.1" 404 134 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
```

J'essaye bêtement cette adresse et je me rends compte que le nombre d'essais est limité !

J'épluche ensuite tous les fichiers dans `/var/log` sans succès.

Je tente désespérément un énorme grep sur tous les fichiers àa la recherche d'une adresse IP en claire :

```
$ sudo grep "\([0-9]\{1,3\}\.\)\{3\}[0-9]\{1,3\}" -r * | grep -v "Fichier binaire" | grep -v "127.0" | grep -v "192.168" | grep -v ":\#" | more
```

Je regarde toutes les lignes mais rien à signaler...

