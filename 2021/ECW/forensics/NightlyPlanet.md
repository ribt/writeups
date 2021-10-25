# Nightly Planet

## Part 1/2

```
The Nightly Planet is a famous Gotham NewsPaper. Its redaction team has noticed suspicious activity on their computers, and require your help to find out what happened, and lead the investigation!

They have provided you with a network capture taken on their main server. Can you discover all the steps of the attack?
```

File: [ECW_chall_JBV.pcapng](ECW_chall_JBV.pcapng)



For this challenge, we got a 13 MB pcapng file we can open with WIreshark. It's really long. My first reflex is to apply the filter `dns` to look for a strange domain name in the requests. I notice 2 domains : `wpad.home` and `evil.com`. The second one is a joke but if we scroll down from the `wpad.home` request without any filter we can see an HTTP request to `http://192.168.1.54/MonSuperCMS/Internal/login.php `. With the filter `ip.addr == 192.168.1.54` we can see interesting stuff !

There are a lot of requests like `GET /MonSuperCMS/Public/articles.php?id=1'%20AND%20(ASCII(SUBSTR((SELECT%20password%20FROM%20users%20LIMIT%200,1),3,1)))%20=%2038%20AND%20'1'='1`. It is SQL injection. For this example the server will respond the first article if the 3rd character of the user's password is a `&` (char 38 in the ASCII table). We export these requests (filter `ip.addr == 192.168.1.54 && http`) to a file called [lite.pcapng](lite.pcapng) and we can write an ugly Python code to extract the password :

```python
from scapy.all import *

packets = rdpcap('lite.pcapng')

for packet in packets:
    req = packet[Raw].load.decode().split(" ")[1].split("/")[-1]
    if req.startswith("articles.php"):
        c = int(req.split("%20")[9])
    if "Scribes" in packet[Raw].load.decode():
        print(chr(c), end="")
```

And the flag is `ECW1{AlwaysThatBooleanBasedSQLi` (the chall maker said that's normal if it is truncated).



## Part 2/2

The capture is the same file and we don't have further information but it is easy to see a `POST /MonSuperCMS/Intranet/upload.php` to the same server just after the SQL injection. With Wireshark we can export the [uploaded PDF document](CONFIDENTIAL.pdf). Its name is `CONFIDENTIAL.pdf` but when we open it, it is pretty disappointing.

When we open the PDF with a text editor, we can see this line : `/JS <6170702E616C65727428224F6F70732021204E6F7468696E6720746F20736565206865726522293B0A2F2F57656C6C20446F6E652021204465636F64652074686520666F6C6C6F77696E6720737472696E672066726F6D2062617365363420746F206765742074686520326E6420666C61670A2F2F2052554E584D6E744E5957787059326C7664584E5152455A42636D565464476C736245465561476C755A7A39390A>` but I don't know what it means... It's obvious that it is hexadecimal. Let's open a shell to convert that :

```
$ echo "6170702E616C65727428224F6F70732021204E6F7468696E6720746F20736565206865726522293B0A2F2F57656C6C20446F6E652021204465636F64652074686520666F6C6C6F77696E6720737472696E672066726F6D2062617365363420746F206765742074686520326E6420666C61670A2F2F2052554E584D6E744E5957787059326C7664584E5152455A42636D565464476C736245465561476C755A7A39390A" | xxd -r -ps
app.alert("Oops ! Nothing to see here");
//Well Done ! Decode the following string from base64 to get the 2nd flag
// RUNXMntNYWxpY2lvdXNQREZBcmVTdGlsbEFUaGluZz99

$ echo "RUNXMntNYWxpY2lvdXNQREZBcmVTdGlsbEFUaGluZz99" | base64 -d
ECW2{MaliciousPDFAreStillAThing?}
```



