# Journée portes ouvertes - 128 pts

> Il y a des courants d'air au niveau du serveur comme s'il y avait des port(e)s ouvert(e)s.
>  Url : `journees-portes-ouvertes.phack.fr` 
>
>  Artiste : `@Eagleslam`

On commence par un petit scan de la machine :

```
$ nmap -A journees-portes-ouvertes.phack.fr

Starting Nmap 7.60 ( https://nmap.org ) at 2021-04-10 22:55 CEST
Nmap scan report for journees-portes-ouvertes.phack.fr (12.42.0.16)
Host is up (0.065s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE   VERSION
80/tcp   open  http?
| fingerprint-strings: 
|   NULL: 
|_    NNNN
5000/tcp open  upnp?
| fingerprint-strings: 
|   DNSStatusRequest, DNSVersionBindReq, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, JavaRMI, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, NULL, NotesRPC, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, WMSRequest, X11Probe, ZendJavaBridge, afp, giop, oracle-tns: 
|_    ..................t_......
5555/tcp open  freeciv?
[...]
```

Houla, le rapport est très long et nmap est complètement perdu. Voyons voir pourquoi il ne détecte pas les protocoles :

```
$ nc journees-portes-ouvertes.phack.fr 5000
..................t_......
$ nc journees-portes-ouvertes.phack.fr 5555
There is nothing here... ¯\_(ツ)_/¯
$ nc journees-portes-ouvertes.phack.fr 5987
There is nothing here... ¯\_(ツ)_/¯
```

OK, OK on va devoir faire un scan nous même.

Voici un petit code Python qui fait ça bien proprement :

```python
import socket

flag = ["."]*26

hote = "12.42.0.16"
for port in range(5000, 6000):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hote, port))
        txt = s.recv(1024).decode()
        s.close()
        if not "nothing" in txt:
            for i in range(len(txt)):
                if txt[i] != ".":
                    flag[i] = txt[i]
            print(*flag, sep="")
    except ConnectionRefusedError:
        pass

```

```
..................t_......
..................t_..R}..
..................t_d'R}..
......s4..........t_d'R}..
......s4........4nt_d'R}..
......s4cr......4nt_d'R}..
......s4cr..c0..4nt_d'R}..
..AC..s4cr..c0..4nt_d'R}..
..ACK{s4cr..c0..4nt_d'R}..
..ACK{s4cr..c0ur4nt_d'R}..
PHACK{s4cr..c0ur4nt_d'R}..
PHACK{s4cr3_c0ur4nt_d'R}..
```

