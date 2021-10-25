from scapy.all import *

packets = rdpcap('lite.pcapng')

for packet in packets:
    req = packet[Raw].load.decode().split(" ")[1].split("/")[-1]
    if req.startswith("articles.php"):
        c = int(req.split("%20")[9])
    if "Scribes" in packet[Raw].load.decode():
        print(chr(c), end="")
