from pwn import *
from base64 import b64decode
from PIL import Image, ImageDraw
from io import BytesIO
from solve import solve

conn = remote('challenges1.france-cybersecurity-challenge.fr', 7002)
conn.recvuntil('Press a key when you are ready...')
conn.send('\n')

while True:
    try:
        conn.recvuntil('------------------------ BEGIN MAZE ------------------------')
        maze = b64decode(conn.recvuntil('------------------------- END MAZE -------------------------', drop=True))
        print(conn.recvuntil(':').decode())
        img = Image.open(BytesIO(maze))
        img.save("maze2.png")
        path = solve(img)
        print(path)
        conn.send(path+'\n')
        print(conn.recvuntil('...').decode())
    except EOFError:
        print(conn.recv().decode())
        break
