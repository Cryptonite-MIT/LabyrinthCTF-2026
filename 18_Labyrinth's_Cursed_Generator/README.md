# 18. Labyrinth's Cursed Generator

**Author**: ryd3r <br>
**Category**: Cryptography <br>
**Difficulty**: Medium

## Description

dEEp wiThiN ThE maZe LIEs A cursEd BROnzE MaCHine IT GRinDs eNdLESSlY IN a sTRiCT maThemATicAL loOP tO lOCk AWAy tHE cORe BluepRInt we ReCOrdEd the exact acoustic echoes of three gear shifts before the vault sealed shut can you find the hidden dimensions and break this curse forever?

## Solve

- Since there are no attached files, we only go off of the description. We can see the strange capitalization of the description.
- We can try a couple of things, but extracting bits from the upper/lower casing is the way to go. The script for it is -
```python3
sentence = "dEEp wiThiN ThE maZe LIEs A cursEd BROnzE MaCHine IT GRinDs eNdLESSlY IN a sTRiCT maThemATicAL loOP tO lOCk AWAy tHE cORe BluepRInt we ReCOrdEd the exact acoustic echoes of three gear shifts before the vault sealed shut. Can you find the hidden dimensions and break this curse forever?"
a = sentence.replace(" ", "")
out = [1 if char.isupper() else 0 for char in a]
bit_string = "".join(str(o) for o in out)

chars = []
for i in range(0, len(bit_string), 8):
    byte = bit_string[i:i+8]
    if len(byte) == 8 and int(byte, 2) > 0:
        chars.append(chr(int(byte, 2)))

print("".join(chars))
```
- This leads us to a *bit.ly* link: `bit.ly/sdfkshad`. This leads us to 2 files, `chall.py` and `out.txt`.
- From chall.py, we can see the hardcoded value of `n`. In `build_mechanism` we can see the equation -
```java
state = (state * a + b) % n
```
- This is the standard equation of an LCG, Linear Congruential Generator. It is way to generate pseudo-random numbers, often insecure due to their direct mathematical relation to the previous states value.
- Now since we have 3 states given to us, we can find a and b as -
```
s2 = s1*a + b mod n
s3 = s2*a + b mod n

a = (s3 - s2) / (s2 - s1) mod n
b = s2 - s1*a mod n
```
- Once we recover `a` and `b`, we can apply the same key mask -
```
mask = (state ^ (state >> 8)) & 0xFF
```
- Then we XOR the mask with the encrypted flag to decrypt it.

```python3
n = 18446744073709551557

encrypted_blueprint = [216, 20, 49, 49, 80, 243, 133, 22, 25, 222, 219, 95, 7, 18, 60, 164, 7, 135, 245, 32, 129, 61, 24, 134, 241, 213, 127, 172, 116, 196, 168, 221, 241, 31, 121, 119, 146, 164, 133, 25]
s0 = 13860788416516638766
s1 = 12414024853170952812
s2 = 14460300224643902914

a = ((s2 - s1) * pow((s1 - s0) % n, -1, n)) % n
b = (s1 - s0 * a) % n
state = s2

decrypted_flag = []
for encrypted_byte in encrypted_blueprint:                                                                                                                    state = (state * a + b) % n
    mask = (state ^ (state >> 8)) & 0xFF

    decrypted_flag.append(chr(encrypted_byte ^ mask))

print("".join(decrypted_flag))
```

## Flag: `labyrinth{g00d_j0b_y0U_cR4ack3d_7he_LCG}`
