# 27. noties

Author: Hitu1197

Phase 3 | webex

Flag: `labyrinth{y0u_n0t13s_th3_3rr0r}`

## Description

Yet another note taking app...
hyphen (-) in username are not allowed!

https://noties.labyrinthctf.live

## Solve

- Create an account on website
- You will get a YAML config and notes creator:

<img width="2222" height="1213" alt="image" src="https://github.com/user-attachments/assets/6db77856-4689-47b9-ab3e-6784c8601892" />


- You are aware that `-` (hyphen) aren't allowed in username
- If you just use it in username then it splits it and capitalizes the words next to it, so if you enter something like `test-with-hyphen`, you get:

<img width="1107" height="1026" alt="image" src="https://github.com/user-attachments/assets/fd524f1e-5297-4bda-a4c9-a7ef8dc1155f" />


- Also on a blind challenge, you must try different types of exploit, so you may try things such as sqli, xss or lfi on such a website
- When you try to lfi with `../../flag.txt`, you get an error that you are hacking it will be reported:

<img width="2231" height="1305" alt="image" src="https://github.com/user-attachments/assets/25ca7e90-6e4a-4215-b74b-85aefd4fdc34" />


- Now you know you gotta bypass that!
- There is a niche yaml feature called yaml aliasing: https://www.akamai.com/cloud/guides/yaml-anchors-aliases-overrides-extensions
- You can use this feature to your advantage here, as you know the hyphen quirk which lets you put lfi path without it detecting as a hacking attempt, and after they are removed, you can use aliasing to copy it to notes
- So bundle all the info you know and you can use this payload to bypass LFI check and get the flag:
```
user: &u
  name: "..-/-..-/-..-/flag.txt"
  password: "password"
  title: "test"
notes:
  - *u
```
- Just go to your notes page for flag :D

