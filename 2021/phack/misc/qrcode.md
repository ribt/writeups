# Quick Response Code - 128 pts

>Philippe XXXIV, roi de Macédoine et  descendant de Philippe II, souhaiterais cacher son mot de passe sur son  ordinateur pour éviter qu'on puisse facilement lui dérober. Mais pas  question pour Philippe d'utiliser un gestionnaire de mot de passe (qui  serait digne de garder le précieux mot de passe d'un roi après tout ?).  Il décide donc d'appliquer le célèbre principe de son  arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-grand-père : diviser pour mieux... enfin vous avez compris. 
>
> Artiste : `@Pdrooo`
>
>[data.zip](./data.zip)

Parce que le shell c'est trop cool :

```
$ for i in {1..1962}; do zbarimg -q code${i}.png | grep -v Nothing >> flag.txt ; done
$ cat flag.txt 
QR-Code:Flag char 11 is "b" (id = 0xbd7c3a4df75441fca25be0a5e51a38d8)
QR-Code:Flag char 30 is "l" (id = 0x92f69371e3e84affa01749e9846d3f96)
QR-Code:Flag char 16 is "1" (id = 0x47a721d7275040e88cec9792022f620c)
QR-Code:Flag char 13 is "_" (id = 0x244aa09ccdc74b9c929de75c0173df53)
EAN-13:0071235000073
QR-Code:Flag char 34 is "}" (id = 0xebcffffd54dc40ae9118d31dd935c8c1)
QR-Code:Flag char 18 is "_" (id = 0x560d4c4876104d899328c30caa2a122e)
EAN-13:0015100001536
QR-Code:Flag char 0 is "P" (id = 0xd83fb7823c7047d28239ec57f936980c)
[...]
$ grep -v EAN flag.txt | cut -c 19- | sort -g | cut -d \" -f 2 | tr -d '\n'
PHACK{MaaaYb3_Th1s_Waas_Overk1lL?!}
```

