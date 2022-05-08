from pwn import remote

BITS = 512

conn = remote("challenges.france-cybersecurity-challenge.fr", 2255)

n = int(conn.recvline().decode().strip()[4:])
e = int(conn.recvline().decode().strip()[4:])

conn.recvuntil("= ")

msg = 42
conn.send(str(msg)+"\n")
conn.recvuntil("= ")
conn.send("0\n")

ref = int(conn.recvline().decode().strip())
ans = ""

for i in range(1, 2 * BITS + 1):
    conn.recvuntil("= ")
    conn.send(str(msg)+"\n")
    conn.recvuntil("= ")
    conn.send(str(i)+"\n")
    t = int(conn.recvline().decode().strip())
    if t != ref:
        ans +="1"
    else:
        ans += "0"
    ref = t
    print(ans)

d = int(ans, 2)
c = int(conn.recvline().decode().strip()[4:])

conn.close()

m = pow(c, d, n)

print(bytes.fromhex(hex(m)[2:]).decode())
