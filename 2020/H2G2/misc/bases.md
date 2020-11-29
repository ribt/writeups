# 1110011 1100001 1101100 1110101 1110100 - 20 pts

>  2202 1110 10121 10220 11001 10202 11020 10121 10220 11021 1012  11021 10121 11101 11010 10220 11020 1012 10200 11010 11001 11001 10202  11002 11022 1012 10210 10121 10220 11020 10202 1012 11100 11002 10202  1012 10122 11010 11002 11002 10202 1012 11011 11100 11020 10202 10202
>
> salut.interiut.ctf:1337
>
> Hint: Bon, ok, ça respecte pas les RFC ... Mais c'est quand même plus logique

Mon premier réflexe est d'utiliser [CyberChef](https://gchq.github.io/CyberChef/) pour décoder le titre mais cela ne donne rien. En étant plus attentif (et grâce à l'indice) on voit que les bits sont regroupés par groupe de 7 ! Si on les décode indivuduellement, on obtient `115 97 108 117 116` soit les codes ASCII des lettres `s a l u t`.

La description semble être en base 3, on la convertit en entier en respectant les groupes puis on décode comme étant de l'ASCII : `J'aimerais savoir comment faire une bonne puree`.

Maintenant `nc salut.interiut.ctf 1337` pour discuter avec le serveur. Il envoie un texte encodé de façon similaire au titre (en binbaire) puis si on envoie la bonne réponse, il envoie un texte en base 3 puis en base 4... Il va falloir automatiser le décodage. En tatonnant on voit que le dernier challenge est de la base 31 puis le flag est envoyé.

```python
from pwn import remote

conn = remote('salut.interiut.ctf', 1337)

for base in range(2, 32):
    txt = conn.recvline().decode()[:-1]

    answer = ""
    for i in txt.split():
        answer += chr(int(i, base))
    print(answer)
    conn.send(answer.encode()+b'\n')

print("\n", conn.recvline().decode())

conn.close()
```

Résultat :

```
Je s4is dej4 f4ire l4 r4t4touille, les endives 4u j4mbon, le gr4tin
Et plein d'autres plats qui n'0nt rien a v0ir avec une b0nne puree
Qu3l 3st votr3 s3cr3t ?
Le l4it ? Le beurre ? L4 creme ?
Qu3l 3st votr3 s3cr3t ?
S'il v0us pl4it 4idez-m0i
Qu3l 3st votr3 s3cr3t ?
P0ur f4ire une b0nne puree, ce qui est p4s m4l qu4nd 0n cuit les p0mmes de terre
C'3st d3 m3ttr3 du lauri3r 3t du thym pour parfum3r 3n amont
Apres tu peux 4j0uter n'imp0rte quel epice
Tu p3ux m3ttr3 du safran, du curcuma, du ging3mbr3
Ou une g0usse d'4il une f0is que les p4t4tes s0nt petries
Et si la pur33 a cram3
Rec0uvre-l4 4vec un chiff0n m0uille
Et fais coul3r du s3l d3ssus
P0ur 4bs0rber les senteurs de brule
Excus3 moi, mais c'3st pas vraim3nt ca qu3 j'avais d3mand3
Le pr0bleme 4vec m4 puree c'est qu'elle n'est p4s 0nctueuse
P3ux-tu m'3xpliqu3r, comm3nt obt3nir un3 t3xtur3 parfait3 ?
P0ur l4 puree 0nctueuse ce qu'il f4ut dej4
C'3st pas trop la m3lang3r ou l'3cras3r
Puisque c0mme d4ns l4 puree il y 4 du gluten c4 v4 devenir tres el4stique
L'utilisation du pr3ss3-pur33 a l3vi3r p3rm3t d'obt3nir un3 pur33 plus fin3 3t l3g3r3
T0ut est d4ns l4 texture
Car la pur33 trop collant3 3st vraim3nt tr3s d3c3vant3
Pense 4 c4 4v4nt de cuisiner et tu reussir4s une b0nne puree
Tu v3rras, c'3st plus facil3 qu3 ca 3n a l'air
Et surt0ut, 4pres c4 tu ne v0udr4s plus d'une 4utre puree
J'ai 4 homm3s a la maison 3t ils s3 r3gal3nt tous
Il n'en reste j4m4is !

 H2G2{D0_y0u_l1k3_14_pur33_?}
```

Cela permet un bon rappel que les données informatiques ne sont que des chiffres et qu'il faut les considérer comme tel ;)