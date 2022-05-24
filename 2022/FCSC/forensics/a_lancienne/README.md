# À l'ancienne

Difficulté : :star:

#### Énoncé

> Vous devez récupérer et analyser les données échangées dans cette capture. On préfère prévenir, avant de paniquer, il va falloir se décontracter et décompresser pour faire ça tranquillement.

fichier : [cap](./cap)

#### Découverte

Le fichier ouvert dans Wireshark ne laisse aucun doute : c'est de l'exfiltration DNS.

Extrayons les requêtes :

```
tshark -r cap -T fields -e dns.qry.name -Y "dns && ip.src == 172.16.76.135" > queries.txt
```

Voici les premières lignes :

```
H4sICFctM2IAA3Bhc3N3ZACVVl9v4zYMf++n0OMG1H-.BsJ2mjt9sCbMNde0FT3Oug2GosxJY8SU7SffqRlPOv-.1nY3SHVFiqQo8icy1hjPj3wCw+IyDd+N0ulGuPquEr-.I1GiQyGAOR9s6mDkQuq1SbxmyVvkPukecwaD8u5N4d-.cGFzc3dk
CBUwcJVWch8V0iVITfl8NiumnMj0ZDRF8m4rWomWZn-.w+4YEgO1fLG5OtQOfmPMs5LtO9sGkpylqmRI7kmw7E-.H2DAgoRdZ0yTNl0VNa4aEH+EQUtSCKuRrJYH9HsBg5-.ZXxgM90uj7Ep3JJjiJuNIJ9Eins+b4jkoFzkD9S0YO-.cGFzc3dk
h0NSCS8wLQXOM4OOASqWa1HuevQK0gNzIEkhrGMXaZ-.RDwBWPOJ8gPEpv2RdgsiehxVbaYIDExtrKIiaKBU5Y-.V0HY9joN1Ehhq4XHUE8znL8hxX7pt8mL7Iz1ePb63X-.nZsp9E1Sr98+n0TRo0I7kzG1NhWAMuw3dggpCWR3Bd-.cGFzc3dk
6pj3jo6qEi39wdgd5RMTmvNhhz2HnSEWLZi5v7/ndM-.FB5D/MWulMs5dkFp7rpDibfQk79n8Y8wreUHiC6GA2-.mZ6tvcIWhE2XtTVa/S28MvoHLIM9B5fa9I5sAignc/-.4DIYMFKUx5BtjnaW1amQ78scKfovMkPhtS870TvAv+-.cGFzc3dk
QFnIMv66emLOvPmDsJI5DzCmm51A4bs21J830TgJr1-.JVFWk/gDaehSEI3MhJZVf1bXjGjyA/+65vYi9qlYje-.G9WFcxagN+efkM8Cn4WqfOPmrV6kmrhN2x/RIER0Ou-.eBjlkaJMcmrN8pCjQELcse+IsUDWLmswqQhXJTRtQq-.cGFzc3dk
7Vrh/iLFfMjQwLs5t1Uupl5CUUm6XVLLpoNSgVYARz-.mURCctezOW3UowYO9VKck2AeeDhQjiOinLOqmU64SH-.3hBOmfJ8wde0xZbnrQvqR0pXKKFskJUZ+JoN2WuXz+-.uPEUdTIXcfW+3ZvZ202piOMAtICBH8DEzZsK/AZ68W-.cGFzc3dk
QIuFbXmxHbum0JIgBbnL8oJfQh92IoWvTUwn9b6jnw-.MZIDif8qFgDbWbfQWBb6vnm1QOSimWCxNDed01il5F-.toBe+/vqyx8rFsoIw7SegxzkrgJ7qDESiioeYCDLRy-./qIlvCYZYuDBnI8jkPDIb/esvac8GNvYJBOdJepCmb-.cGFzc3dk
PjgARTJ/uIrjaS/SmHvwiHQQvI98hfSnvlImBoggHW-.ttgOdEaeWVaBInPfViTMqp8KF2RCq9jsu2akkLoFlM-.oEGCNAG8Ee8fOzJcqWqLa2XnXAgpFM8i4+v1ejnK3B-.lWLtZN3/Z5aIOT8AH68lZx8/JT9NSZSmPlUEcXiwX9-.cGFzc3dk
nTrTr7DFlrCHTkdO+wfTUcW67goAAA==-.cGFzc3dk
```

Dans ce premier bloc, chaque ligne se termine par `cGFzc3dk` qui signifie `passwd` en base64. Si on enlève ces fins de ligne, qu'on remplace les `*` par des `+` et qu'on enlève les `-.` on obtient du base64 valide qui donne un drôle de fichier :

```
$ xxd passwd
00000000: 1f8b 0808 572d 3362 0003 7061 7373 7764  ....W-3b..passwd
00000010: 0095 565f 6fe3 360c 7fef a7d0 e306 d470  ..V_o.6........p
00000020: 6c27 69a3 b7db 026c c35d 7b41 53dc eba0  l'i....l.]{AS...
00000030: d86a 2cc4 963c 494e d27d fa91 94f3 afd6  .j,..<IN.}......
00000040: 7637 4875 458a a428 f227 32d6 18cf 8f7c  v7HuE..(.'2....|
00000050: 02c3 e232 0ddf 8dd2 e946 b8fa ae12 b235  ...2.....F.....5
00000060: 1a24 3218 0391 f6ce a60e 442e ab54 9bc6  .$2.......D..T..
00000070: 6c95 be43 ee91 e730 683f 2ee4 de1d 0815  l..C...0h?......
00000080: 3070 9556 721f 15d2 2548 4df9 7c36 2ba6  0p.Vr...%HM.|6+.
00000090: 9cc8 f464 3445 f26e 2b5a 8996 667c 3ee1  ...d4E.n+Z..f|>.
000000a0: 8120 3b57 cb1b 93ad 40e7 e63c cb39 2ed3  . ;W....@..<.9..
000000b0: bdb0 6929 ca5a a644 8ee4 9b0e c41f 60c0  ..i).Z.D......`.
000000c0: 8284 5d67 4c93 365d 1535 ae1a 107f 8441  ..]gL.6].5.....A
000000d0: 4b52 08ab 91ac 9607 f47b 0183 9657 c603  KR.......{...W..
000000e0: 3dd2 e8fb 129d c926 3889 b8d2 09f4 48a7  =......&8.....H.
000000f0: b3e6 f88e 4a05 ce40 fd4b 460e 8743 5209  ....J..@.KF..CR.
00000100: 2f30 2d05 ce33 838e 012a 966b 51ee 7af4  /0-..3...*.kQ.z.
00000110: 0ad2 0373 2049 21ac 6317 6994 43c0 158f  ...s I!.c.i.C...
00000120: 389f 203c 4a6f d917 60b2 27a1 c556 da60  8. <Jo..`.'..V.`
00000130: 80c4 c6da ca22 268a 054e 5857 41d8 f63a  ....."&..NXWA..:
00000140: 0dd4 4861 ab85 c750 4f33 9cbf 21c5 7ee9  ..Ha...PO3..!.~.
00000150: b7c9 8bec 8cf5 78f6 fadd 79d9 b29f 44d5  ......x...y...D.
00000160: 2afd f3e9 f44d 1a34 23b9 331b 5361 5803  *....M.4#.3.SaX.
00000170: 2ec3 7760 8290 9647 705d ea98 f78e 8eaa  ..w`...Gp]......
00000180: 122d fdc1 d81d e513 139a f361 873d 879d  .-.........a.=..
00000190: 2116 2d98 b9bf bfe7 74c1 41e4 3fcc 5ae9  !.-.....t.A.?.Z.
000001a0: 4cb3 9764 169e eba4 389b 7d09 3bf6 7f18  L..d....8.}.;...
000001b0: f30a de50 7882 e860 3699 9ead bdc2 1684  ...Px..`6.......
000001c0: 4d97 b535 5afd 2dbc 32fa 072c 833d 0797  M..5Z.-.2..,.=..
000001d0: daf4 8e6c 0228 2773 fe03 2183 0529 4c79  ...l.('s..!..)Ly
000001e0: 06d8 e769 6d5a 990e fcb1 c29f a2f3 243e  ...imZ........$>
000001f0: 1b52 f3bd 13bc 0bfe 4059 c832 feba 7a62  .R......@Y.2..zb
00000200: cebc f983 b092 390f 30a6 9b9d 40e1 bb36  ......9.0...@..6
00000210: d49f 37d1 3809 af52 5515 693f 8036 9e85  ..7.8..RU.i?.6..
00000220: 2108 dcc8 4965 57f5 6d78 c68f 203f fbae  !...IeW.mx.. ?..
00000230: 6f62 2f6a 9588 de1b d585 7316 a037 e79f  ob/j......s..7..
00000240: 90cf 029f 85aa 7ce3 e6ad 5ea4 9ab8 4ddb  ......|...^...M.
00000250: 1fd1 2044 743a e781 8e59 1a24 c726 acdf  .. Dt:...Y.$.&..
00000260: 290a 3404 2dcb 1ef8 8b14 0d62 e6b3 0a90  ).4.-......b....
00000270: 8572 5346 d42a ed5a e1fe 22c5 7cc8 d0c0  .rSF.*.Z..".|...
00000280: bb39 b755 2ea6 5e42 5149 ba5d 52cb a683  .9.U..^BQI.]R...
00000290: 5281 5600 4739 9444 272d 7b33 96dd 4a30  R.V.G9.D'-{3..J0
000002a0: 60ef 5529 c936 01e7 8385 08e2 3a29 cb3a  `.U).6......:).:
000002b0: a994 eb84 87de 104e 99f2 7cc1 d7b4 c596  .......N..|.....
000002c0: e7ad 0bea 474a 5728 a16c 9095 19f8 9a0d  ....GJW(.l......
000002d0: d96b 97cf eb8f 1147 5321 771f 5bed d9bd  .k.....GS!w.[...
000002e0: 9db4 da98 8e30 0b48 0811 fc0c 4cd9 b0af  .....0.H....L...
000002f0: c067 af16 408b 856d 79b1 1dbb a6d0 9220  .g..@..my...... 
00000300: 05b9 cbf2 825f 421f 7622 85af 4d4c 27f5  ....._B.v"..ML'.
00000310: bea3 9f03 1920 389f f2a1 600d b59b 7d05  ..... 8...`...}.
00000320: 816f abe7 9b54 0e4a 2996 0b13 4379 dd35  .o...T.J)...Cy.5
00000330: 8a5e 45b6 805e fbfb eacb 1f2b 16ca 08c3  .^E..^.....+....
00000340: b49e 831c e4ae 027b a831 128a 2a1e 6020  .......{.1..*.` 
00000350: cb47 2fea 225b c261 962e 0c19 c8f2 390f  .G/."[.a......9.
00000360: 0c86 ff7a cbda 73c1 8dbd 8241 39d2 5ea4  ...z..s....A9.^.
00000370: 299b 3e38 0045 327f b88a e369 2fd2 987b  ).>8.E2....i/..{
00000380: f088 7410 bc8f 7c85 f4a7 be52 2606 8820  ..t...|....R&.. 
00000390: 1d6b 6d80 e744 69e5 9568 1227 3df5 624c  .km..Di..h.'=.bL
000003a0: caa9 f0a1 7644 2abd 8ecb b66a 490b a059  ....vD*....jI..Y
000003b0: 4ca0 4182 3401 bc11 ef1f 3b32 5ca9 6a8b  L.A.4.....;2\.j.
000003c0: 6b65 e75c 0829 14cf 22e3 ebf5 7a39 cadc  ke.\.).."...z9..
000003d0: 1956 2ed6 4ddf f679 6883 93f0 01fa f256  .V..M..yh......V
000003e0: 71f3 f253 f4d4 994a 63e5 5047 178b 05fd  q..S...Jc.PG....
000003f0: 9d3a d3af b0c5 96b0 874e 474e fb07 d351  .:.......NGN...Q
00000400: c5ba ee0a 0000                           ......
```

On voit que la capture envoie plusieurs fichiers de la sorte : `file1` puis `file3`  puis `file4`  et enfin `file2` .

Chaque fichier ressemble à du bruit sauf `file3` qui a un hexdump intéressant :

```
$ xxd file3
00000000: 1f8b 0808 cf62 3362 0003 6669 6c65 3300  .....b3b..file3.
00000010: 016e 3191 ce89 504e 470d 0a1a 0a00 0000  .n1...PNG.......
00000020: 0d49 4844 5200 0000 5000 0000 5008 0600  .IHDR...P...P...
00000030: 0000 8e11 f2ad 0000 3135 4944 4154 789c  ........15IDATx.
[...]
00003150: 6eca a68d 1826 6148 2907 4174 0821 ea46  n....&aH).At.!.F
00003160: b226 0741 9c02 86cf 00e6 5f00 e0ff 03c0  .&.A......_.....
00003170: b87d 1748 d009 1300 0000 0049 454e 44ae  .}.H.......IEND.
00003180: 4260 82da c6ad 866e 3100 00              B`.....n1..

```

On reconnaît la signature de début et de fin du PNG. Si on vire les 21 premiers octets on a un PNG qui s'affiche bien :

![logo ANSSI](file3_crop.png)

Malheureusement je n'ai réussi à rien récupérer autre chose que ce logo...



Edit : Comme l'énoncé le laissait entrevoir, il fallait **décompresser** (les fichiers). En plus j'avais bien vu le `gzip compressed data` en faisant un `file` sur les fichiers mais c'était pour moi un faux positif car des méta-données étaient ajouées en début de fichier et étaient interprétées à tort comme un *magic number* gzip. Comme expliqué dans [ce WU](https://gitlab.com/ctfun/ctf-writeups/-/blob/master/fcsc2022/forensic/%C3%80%20l'ancienne/alancienne.md) il fallait renommer les fichiers avec `.gz` pour pouvoir les ouvrir et on récupérait 2 autres images lié au FCSC et un fichier Word (file4) contenant le flag : `FCSC{18e955473d2e12feea922df7e1f578d27ffe977e7fa5b6f066f7f145e2543a92}`.
