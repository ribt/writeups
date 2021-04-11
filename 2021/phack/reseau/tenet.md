# Tenet - 128 pts

> Fan du film Tenet de 2020 tu as désormais  l'occasion dont tu rêvais d'aider ton héro préféré puisque tu viens  d'intercepter une communication venant du future. 
>
>  Artiste : `@Eagleslam`
>
> [tenet.pcapng](./tenet.pcapng)

On ouvre le fichier avec Wireshark. On voit du TCP et du TELNET. Clic droit sur le premier paquet Telnet, 

*Suivre le flux TCP*. En allant vers la fin, on peut lire :

```
root@e6a961d4e29f: ~/Documents.root@e6a961d4e29f:~/Documents# head secret.txt 
aVdzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLFdbCldAQFcuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZ0BAWwppQEBAQEBzICAgICAgICAgICAgICAgICAgICAgICAgICAgZ0BAQEBXCkBAQEBAQEBXLiAgICAgICAgICAgICAgICAgICAgICAgLFdAQEBAQEAKXUBAQEBAQEBAQFcuICAgLF9fX19fX18uICAgICAgICxtQEBAQEBAQEBpCixAQEBAQEBAQEBAQEBXQEBAQEBAQEBAQEBAQEBtbV9nQEBAQEBAQEBAQFsKZEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQAppQEBAQEBAQEEqfn5+fn5WTUBAQEBAQEBAQEBBZn5+fn5WKkBAQEBAQEBAQGkKQEBAQEBBfiAgICAgICAgICAnTUBAQEBAQEFgICAgICAgICAgJ1ZAQEBAQEBiCmRAQEAqYCAgICAgICAgICAgICAgWUBAQEBmICAgICAgICAgICAgICBWQEBAQEAuCmlAQEFgICAgICAgICAgICAgICAgICBNQEBQICAgICAgICAgICAgICAgICBWQEBAYgosQEBBICAgICAgICAgICAgICAgICAgICdAQCAgICAgICAgICAgICAgICAgICAhQEBALgpXQFAgICAgICAgICAgICAgICAgICAgICBAWyAgICAgICAgICAgICAgICAgICAgJ0BAVwpkQEAgICAgICAgICAgICAsICAgICAgICAgXSEgICAgICAgICAgICAgICAgICAgICBdQEBiCmdAQFsgICAgICAgICAgLFdAQHMgICAgICAgXSAgICAgICAsV0BAcyAgICAgICAgICAgQEBAaQppQEBAWyAgICAgICAgICBXQEBAQGkgICAgICBdICAgICAgIFdAQEBAaSAgICAgICAgICBAQEBAaQppQEBAQFsgICAgICAgICAgQEBAQEBbICAgICAgXSAgICAgICBAQEBAQFsgICAgICAgICAgQEBAQEBpCmdAQEBAQFsgICAgICAgICAgQEBAQEAhICAgICAgQFsgICAgICBAQEBAQFsgICAgICAgICAgQEBAQEBAaQpkQEBAQEBAQCAgICAgICAgICAhQEBAUCAgICAgIGlBVyAgICAgICFAQEBBICAgICAgICAgIF1AQEBAQEBAaQpXQEBAQEBAQEBiICAgICAgICAgICd+fiAgICAgICxaIFlpICAgICAgJ35+ICAgICAgICAgICxAQEBAQEBAQEAKJypAQEBAQEBAQHMgICAgICAgICAgICAgICAgICBaYCAgWS4gICAgICAgICAgICAgICAgICxXQEBAQEBAQEBBCidNQEBAKmYqKlcuICAgICAgICAgICAgICAsWiAgICAgVnMgICAgICAgICAgICAgICAsVyp+fn5NQEBAZgonTUAgICAgJ1ZzLiAgICAgICAgICAsen4gICAgICAgJ05fICAgICAgICAgICAsWn4gICAgIGRAUApNQEBAICAgICAgIH5cLV9fICBfX3ovYCAsZ21XQEBtbV8gJytlXy4gICBfXz0vYCAgICAgICxAQEBACidWTVcgICAgICAgICAgICAgICAgICBnQEBAQEBAQEBAVyAgICAgfn5+ICAgICAgICAgICxXQWYKfk4uICAgICAgICAgICAgICAgIEBAQEBAQEBAQEBAISAgICAgICAgICAgICAgICAsWmAKVi4gICAgICAgICAgICAgICAhTUBAQEBAQEBAZiAgICAgICAgICAgICAgICBnZi0KJ04uICAgICAgICAgICAgICAgJ34qKipmfiAgICAgICAgICAgICAgICAsWmAKVmMuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF9aZgp+ZV8gICAgICAgICAgICAgICAgICAgICAgICAgICAgICxnWX4KICAnVj1fICAgICAgICAgIC1AQEQgICAgICAgICAsZ1l+ICcKICAgICAgflw9X18uICAgICAgICAgICAsX196PX5gCiAgICAgICAgICAgJ35+fio9PVkqZn5+fgoKV2VsbCBkb25lLiBUaGUgZmxhZyBpcyBQSEFDS3tkMF9uMHRfdXMzXzFuczNjVXIzX3BSMHQwYzBsfQ==
```

Ce qui signifie :

```
iWs                                 ,W[
W@@W.                              g@@[
i@@@@@s                           g@@@@W
@@@@@@@W.                       ,W@@@@@@
]@@@@@@@@@W.   ,_______.       ,m@@@@@@@@i
,@@@@@@@@@@@@W@@@@@@@@@@@@@@mm_g@@@@@@@@@@[
d@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
i@@@@@@@A*~~~~~VM@@@@@@@@@@Af~~~~V*@@@@@@@@@i
@@@@@A~          'M@@@@@@A`         'V@@@@@@b
d@@@*`              Y@@@@f              V@@@@@.
i@@A`                 M@@P                 V@@@b
,@@A                   '@@                   !@@@.
W@P                     @[                    '@@W
d@@            ,         ]!                     ]@@b
g@@[          ,W@@s       ]       ,W@@s           @@@i
i@@@[          W@@@@i      ]       W@@@@i          @@@@i
i@@@@[          @@@@@[      ]       @@@@@[          @@@@@i
g@@@@@[          @@@@@!      @[      @@@@@[          @@@@@@i
d@@@@@@@          !@@@P      iAW      !@@@A          ]@@@@@@@i
W@@@@@@@@b          '~~      ,Z Yi      '~~          ,@@@@@@@@@
'*@@@@@@@@s                  Z`  Y.                 ,W@@@@@@@@A
'M@@@*f**W.              ,Z     Vs               ,W*~~~M@@@f
'M@    'Vs.          ,z~       'N_           ,Z~     d@P
M@@@       ~\-__  __z/` ,gmW@@mm_ '+e_.   __=/`      ,@@@@
'VMW                  g@@@@@@@@@W     ~~~          ,WAf
~N.                @@@@@@@@@@@!                ,Z`
V.               !M@@@@@@@@f                gf-
'N.               '~***f~                ,Z`
Vc.                                  _Zf
~e_                             ,gY~
  'V=_          -@@D         ,gY~ '
      ~\=__.           ,__z=~`
           '~~~*==Y*f~~~

Well done. The flag is PHACK{d0_n0t_us3_1ns3cUr3_pR0t0c0l}
```



