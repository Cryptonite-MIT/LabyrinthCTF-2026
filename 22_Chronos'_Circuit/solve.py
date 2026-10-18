from Crypto.Cipher import AES 

RAND_MAX = 0x7FFF
USE_WEAK_SEEDING = False  
_next = 1 

def _to_signed32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


def _c_div(a, b):
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def _c_mod(a, b):
    return a - b * _c_div(a, b)


def _do_rand(ctx):
    if USE_WEAK_SEEDING:
        ctx[0] = (ctx[0] * 1103515245 + 12345) & 0xFFFFFFFF
        return ctx[0] % (RAND_MAX + 1)

    x = _to_signed32(ctx[0])
    if x == 0:
        x = 123459876
    hi = _c_div(x, 127773)
    lo = _c_mod(x, 127773)
    x = _to_signed32(16807 * lo - 2836 * hi)
    if x < 0:
        x = _to_signed32(x + 0x7FFFFFFF)
    ctx[0] = x & 0xFFFFFFFF
    return ctx[0] % (RAND_MAX + 1)



def rand():
    global _next
    state = [_next]
    value = _do_rand(state)
    _next = state[0]
    return value


def srand(seed):
    global _next
    _next = seed & 0xFFFF


srand(0)
key = bytearray([(rand() % 256) for _ in range(16)])
print("Key: ", key.hex())
cipher = AES.new(key, AES.MODE_CBC, b'\x00'*16)
ciphertext = bytes.fromhex("4B0D83DAA4C29BE7882623C3BEB0AE5FEB3DDFDC71BC4BF6CED1C416547A9419")
plaintext = cipher.decrypt(ciphertext)
print("Recovered plaintext: ", plaintext.decode())
print("\nFinal Flag: labyrinth{" + plaintext.decode() + "}\n")

