# Git de France - 128 pts

>  J'ai perdu mon flag quelque part dans ce projet.. 
>  Pas moyen de remettre la main dessus :( 
>
>  Artiste : `@Pdrooo`
>
> [chall.zip](./chall.zip)

On extrait l'archive et l'on voit des fichiers PHP, HTML, CSS et quelques images. Rien d'intéressant dans ces fichiers mais vu le nom du challenge il va surtout falloir s'intéresser au dossier caché `.git`.

Un petit `git log -p` permet d'afficher l'historique des modifications mais malheureusement on y trouve rien d'intéressant... Heureusement la commande `git reflog` est beaucoup plus bavarde et l'on voit qu'il y a des commits sur 4 branches (la commande précédente ne montraient que les commit dans la branche *master*). Au lieu de toutes les explorer on va chercher un flag en clair :

```
$ git reflog -p | grep PHACK
-// PHACK{Z2l0IGNvbW1pdCAtbSAiRXogZ2l0IDp0YWRhOiI=}
-// PHACK{Z2l0IGNvbW1pdCAtbSAiRXogZ2l0IDp0YWRhOiI=}
+// PHACK{Z2l0IGNvbW1pdCAtbSAiRXogZ2l0IDp0YWRhOiI=}
```

Le décodage du base 64 est laissé en exercice au lecteur :)