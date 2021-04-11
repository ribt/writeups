# Caumunikassion - 128 pts

> Le nouveau stagiaire en communication du  P'Hack CTF nous semble étrange. Nous avons peur qu'il utilise ses  compétences pour exfiltrer des informations sensibles. Il a  principalement travaillé sur le site https://ctf.phack.fr. 
>  
>
>  Artiste : `@Eagleslam`

La page web en question est la page d'accueil du CTFd et elle semble parfaitement normale. Rien dans le code de la page. Essayons de télécharger le gros logo PNG qui est affiché sur cette page : [phack_white.png](./phack_white.png).

On rappelle la règle n°1 de tout bon CTF : toujours commencé par un `strings` :

```
$ strings phack_white.png 
IHDR
sRGB
	pHYs
PLTE
TtRNS
[...]
Bw&q
)tEXtComment
https://pastebin.com/raw/xjyzhxYZ
IEND
```

Un petit tour sur l'URL donnée nous offre le flag :

```
  BRAVO ! Voici le flag :  
PHACK{e4sy_st3g4n0_rigH7?}
```



