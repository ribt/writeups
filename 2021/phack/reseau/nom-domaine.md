# Système de nom de domaine - 128 pts		

> Votre équipe est sur le point de résoudre un nouveau challenge mais le nom de domaine `flag.phack.fr` ne semble pas fonctionner. Une analyse plus poussée est peut-être nécessaire. 
>
>  Artiste : `@Eagleslam`

```
$ dig ANY flag.phack.fr

; <<>> DiG 9.11.3-1ubuntu1.14-Ubuntu <<>> ANY flag.phack.fr
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 22788
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;flag.phack.fr.			IN	ANY

;; ANSWER SECTION:
flag.phack.fr.		3600	IN	TXT	"PHACK{diG_i7_4nD_f0uNd_i7_In_y0uR_dNs}"
flag.phack.fr.		3600	IN	RRSIG	TXT 8 3 3600 20210505095646 20210405095646 50625 phack.fr. 2aZq9mA4leRxEDKg8DRepFl0NZS5So+f1CyEKs+Gx2IHwNl8dmpaFoDy G7vb0uHxFEh0mb70vtRRCtn3lPneuwTmuFXB47Ra+VCPtCx6rrtw1K3J qQGHCoxz7r2FbLB9Eqz9aVTDsbKI5QX3coFYcfMwb4J28qYB0gZ00rnM fC4=

;; Query time: 70 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Sat Apr 10 23:02:40 CEST 2021
;; MSG SIZE  rcvd: 261
```

