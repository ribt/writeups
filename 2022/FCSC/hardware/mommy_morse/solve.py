from pwn import *
import numpy as np
import base64

SAMP_RATE = 24e3

TIMING_DOT = 1/1000
TIMING_DASH = 5/1000
TIMING_SEP_LETTER = 5/1000
TIMING_SPACE = 20/1000

alphabet = { 'A':'.-', 'B':'-...',
            'C':'-.-.', 'D':'-..', 'E':'.',
            'F':'..-.', 'G':'--.', 'H':'....',
            'I':'..', 'J':'.---', 'K':'-.-',
            'L':'.-..', 'M':'--', 'N':'-.',
            'O':'---', 'P':'.--.', 'Q':'--.-',
            'R':'.-.', 'S':'...', 'T':'-',
            'U':'..-', 'V':'...-', 'W':'.--',
            'X':'-..-', 'Y':'-.--', 'Z':'--..',
            '1':'.----', '2':'..---', '3':'...--',
            '4':'....-', '5':'.....', '6':'-....',
            '7':'--...', '8':'---..', '9':'----.',
            '0':'-----', ', ':'--..--', '.':'.-.-.-',
            '?':'..--..', '/':'-..-.', '-':'-....-',
            '(':'-.--.', ')':'-.--.-'}

HOST = "challenges.france-cybersecurity-challenge.fr"
PORT = 2251
conn = remote(HOST, PORT)

message = "CAN I GET THE FLAG"
bits = []

for letter in message:
    if letter == " ":
        bits += [0] * int((TIMING_SPACE-TIMING_SEP_LETTER)*SAMP_RATE)
        continue
    for i, c in enumerate(alphabet[letter]):
        if c == ".":
            bits += [1+1j] * int(TIMING_DOT*SAMP_RATE)
        else:
            bits += [1+1j] * int(TIMING_DASH*SAMP_RATE)
        if i < len(alphabet[letter])-1:
            bits += [0] * int(TIMING_DOT*SAMP_RATE)
    bits += [0] * int(TIMING_SEP_LETTER*SAMP_RATE)
    
signal = np.array(bits, dtype=np.complex64).tobytes()

with open("signal2.iq", "wb") as f:
    f.write(signal)

encoded_signal = base64.b64encode(signal)
conn.recvuntil(b"> ")
conn.sendline(encoded_signal)
print(conn.recvline())

