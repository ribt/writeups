tshark -r ping_pong.pcapng -T fields -e data -Y "ip.src==10.5.0.2" | xxd -r -ps -c 1
