# 09. quick-fate

Author: bitf1ip

Phase 1 | rev

Flag: `LABYRINTH{0H_Y0U_ALM0ST_D13D_TH3R3}`

Handout: [rev-quick-fate.7z](./handout/rev-quick-fate.7z)

## Description

You come to another one of labyrinth's rooms. A room that seems endless to you and you try to find a way through it but on the way you have to dodge obstacles that will define your fate

Are you quick enough to dodge them??

Flag Format: `LABYRINTH{<change spaces to _>}`

> Disclaimer: All the files are safe to download and run

## Solve

- Open `main.exe` in IDA and in the strings subview search for `VICTORY` or `FLAG`

- xrefs take you to the function `sub_401DC0`

- in which you can see just before printing of win the function `sub_4011B0` is called in which `sub_401130` is called

> sub_401130
```c
char *sub_401130()
{
  int i; // [esp+4h] [ebp-4h]

  if ( !dword_41EAB4 )
  {
    for ( i = 0; i < 24; ++i )
      byte_41EA98[i] = byte_416210[i] ^ 0x5A;
    unk_41EAB0 = 0;
    dword_41EAB4 = 1;
  }
  return byte_41EA98;
}
```

> byte_416210
```text
.rdata:00416210 ; char byte_416210[24]
.rdata:00416210 byte_416210     db 6Ah                  ; DATA XREF: sub_401130+2A↑r
.rdata:00416211                 db  12h
.rdata:00416212                 db  7Ah ; z
.rdata:00416213                 db    3
.rdata:00416214                 db  6Ah ; j
.rdata:00416215                 db  0Fh
.rdata:00416216                 db  7Ah ; z
.rdata:00416217                 db  1Bh
.rdata:00416218                 db  16h
.rdata:00416219                 db  17h
.rdata:0041621A                 db  6Ah ; j
.rdata:0041621B                 db    9
.rdata:0041621C                 db  0Eh
.rdata:0041621D                 db  7Ah ; z
.rdata:0041621E                 db  1Eh
.rdata:0041621F                 db  6Bh ; k
.rdata:00416220                 db  69h ; i
.rdata:00416221                 db  1Eh
.rdata:00416222                 db  7Ah ; z
.rdata:00416223                 db  0Eh
.rdata:00416224                 db  12h
.rdata:00416225                 db  69h ; i
.rdata:00416226                 db    8
.rdata:00416227                 db  69h ; i
```

- Now we can just get the flag by xor-ing the found byte against 0x5a

> sol.py
```python
encoded = [
    0x6A, 0x12, 0x7A, 0x03, 0x6A, 0x0F, 0x7A, 0x1B,
    0x16, 0x17, 0x6A, 0x09, 0x0E, 0x7A, 0x1E, 0x6B,
    0x69, 0x1E, 0x7A, 0x0E, 0x12, 0x69, 0x08, 0x69
]

decoded_bytes = bytes([b ^ 0x5A for b in encoded])

print("flag4u: ", decoded_bytes.decode('ascii'))
```

```bash
•  python3 sol.py
flag4u:  0H Y0U ALM0ST D13D TH3R3
```

- Adding the `LABYRINTH` flag format and changing ` ` to `_` gives us the flag

> flag
```
LABYRINTH{0H_Y0U_ALM0ST_D13D_TH3R3}
```

