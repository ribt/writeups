# **This** destroyes the RSA cryptosystem.

from Crypto.Util.number import isPrime, bytes_to_long
from Crypto.Random.random import getrandbits

def fastPrime(bits, eps = 32):
	while True:
		a, e, u = getrandbits(eps), getrandbits(eps), getrandbits(4 * eps)
		p = a * (2 ** bits - e) + u
		if isPrime(p):
			return p

def generate(bits = 2048):
	p = fastPrime(bits // 2)
	q = fastPrime(bits // 2)
	return p * q, 2 ** 16 + 1

n, e = generate()

p = bytes_to_long(open("flag.txt", "rb").read())
c = pow(p, e, n)

print(f"e = {e}")
print(f"n = {n}")
print(f"c = {c}")
