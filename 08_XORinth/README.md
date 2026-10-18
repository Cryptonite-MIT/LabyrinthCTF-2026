# 08. XORinth

Author: pin3apple07

Phase 1 | crypto

Flag: `labyrinth{n07_60nn4_b3_ju57_b451c_r07_7h15_71m3}`

## Description

The next turn presents you with a text file containing numbers and a python script that seems to have generated them. But the encryption Daedalus chose seems abit weak. Can you figure out his intentions and find the way forward?

## Solve

So the challenge was just a 2 byte xor with the flag, and the output was given, so could either brute for odd and even places using k1 and k2 or the way it is in the following script, ideal method was to use a valid character set, not assuming English prose because the flag was in leetspeak, so it'd be `a-z0-9_` as used in the following script:


```
ct = [167, 108, 254, 3, 255, 108, 167, 50, 253, 3, 171, 111, 150, 54, 188, 105, 254, 3, 171, 104, 252, 109, 170, 3, 187, 108, 254, 3, 254, 52, 248, 105, 150, 107, 248, 49, 250]
ok = set(b"abcdefghijklmnopqrstuvwxyz0123456789_")
cand = [[k for k in range(256) if all(c ^ k in ok for c in ct[i::2])] for i in range(2)]
for a in cand[0]:
    for b in cand[1]:
        print(a, b, bytes(c ^ (a, b)[i % 2] for i, c in enumerate(ct)).decode())
```

This'll return `201 92 n07_60nn4_b3_ju57_b451c_r07_7h15_71m3`, wrap in labyrinth{} to get the flag: 

```labyrinth{n07_60nn4_b3_ju57_b451c_r07_7h15_71m3}```

