# 28. thread.sock

Author: pin3apple07

Phase 3 | crypto

Flag: `labyrinth{n07_3x4c7ly_bu7_y34h_k1nd4_l1k3_bl31ch3nb4ch3r}`

## Description

Your journey into Daedalus' ex-sanctuary didn't lead to any information about his potential whereabouts. However, you do find a series of chambers which seem different from the rest. You decide to investigate. There are three chambers. The first two are not the real challenge. However, the third will test your mettle. That is if you do manage to reach it.

## Solve

From the first look, there's 3 chambers mentioned at the top as written in the description aswell, its a normal looking web interface:


<img width="1458" height="650" alt="Screenshot 2026-10-13 at 11 15 47 AM" src="https://github.com/user-attachments/assets/13c1c4d3-8ccf-4c64-a82a-648b97578a69" />

So looking at it there's two things `THE THREAD` and `THE RITE`, The rite expects an input as it says _The altar is bare. Bring it what it asks for_, 2 fields separated by a colon, one would try to type random stuff like guest admin etc. as it says _whisper a name_

<img width="509" height="390" alt="Screenshot 2026-10-13 at 1 53 51 PM" src="https://github.com/user-attachments/assets/e06c9ae3-3810-4a41-8937-35950ba17614" />

It gave an output for guest, role and username.

<img width="527" height="305" alt="Screenshot 2026-10-13 at 1 54 20 PM" src="https://github.com/user-attachments/assets/059f31a0-d8fd-48cc-b481-cd12d7840046" />

It says there's nothing for admin.

Then one would type in a quote and the query fails, says refuse to answer to that:

<img width="493" height="295" alt="Screenshot 2026-10-13 at 11 16 33 AM" src="https://github.com/user-attachments/assets/10974f31-a23c-4710-a7b6-21dcfbaa2247" />

This hints towards SQLi vulnerability, so the confirmation step would be typing `' OR 1=1--` and we get this:

<img width="467" height="527" alt="Screenshot 2026-10-13 at 1 57 15 PM" src="https://github.com/user-attachments/assets/09223c0c-63c0-4e2b-96f3-f69f893feb14" />

So the rite asks us for `(sentinel_alias:sigil)`, one can notice sentinel as role for the username warden, so that could be the answer for that.

But we also need one `sigil` which might be a column for another table in the db, so to list that out one would now want to check which database is it, so lets try different sql injections, but before that we need to know how many columns does the query return, then we'll be able to perform a UNION attack getting the type of db first and then listing the tables from the db, so I ran the query `' UNION SELECT NULL, NULL--`, after using NULL once, it give an output, that means it returns 2 columns, this was confirmed earlier aswell when role and username were displayed, so now we can run different queries to check db type:

- `SELECT @@version;` is used for MySQL and MariaDB.
- `SELECT version();` for PostgreSQL.
- `SELECT * FROM v$version;` for Oracle databases.
- `SELECT sqlite_version();` for sqlite databases.


Now these will be used using the UNION keyword to select null and the specific version like `' UNION SELECT NULL, sqlite_version()--`
Now on running them all one would find that it gives a valid output and a version number for the sqlite command, otherwise the query fails:

<img width="465" height="287" alt="Screenshot 2026-10-13 at 2 11 35 PM" src="https://github.com/user-attachments/assets/9c91c375-6b4d-43fa-84c1-c24a1a47ab22" />

For the sqlite command:

<img width="464" height="355" alt="Screenshot 2026-10-13 at 2 13 09 PM" src="https://github.com/user-attachments/assets/c5974cb1-e029-4b97-a287-2abe86e551cc" />

Now this confirms that the database is sqlite, now the command for listing all tables here is `' UNION SELECT sql, name FROM sqlite_master WHERE type='table'--`, we're querying the sqlite_master here, now this outputs in the table names and its columns get listed:

<img width="464" height="485" alt="Screenshot 2026-10-13 at 2 16 33 PM" src="https://github.com/user-attachments/assets/05ecaba6-3ece-422d-85e5-7d9b44b53730" />

After this now we need to query the murmurs table to get the sigil, so our injection will be `' UNION SELECT glyph, sigil FROM murmurs--`, this gives us the sigil:

<img width="459" height="378" alt="Screenshot 2026-10-13 at 2 18 16 PM" src="https://github.com/user-attachments/assets/9af189ff-d2bc-45fc-939d-bf878bf0c5e6" />

Similarly querying the other table we get the alias and status:

<img width="461" height="526" alt="Screenshot 2026-10-13 at 2 19 41 PM" src="https://github.com/user-attachments/assets/ad31d6a5-052c-4977-bba6-1bc970829f68" />

The some thing we got for the `or 1=1` injection, so the rite should take the answer `warden:4fadb907764cfc94c47d937e8d850b76375558f8`, it does and chamber 2 lightens up saying _a seam splits the stone and the passage opens — descend into the vault._

Now this time asks for `(sentinel_alias:key_ref:seal)`, lets do the same thing again listing the tables querying each table accordingly for the root account, we'll get the answer, we had to query for the seal and ref look for the particular key_ref we found earlier


<img width="939" height="689" alt="Screenshot 2026-10-13 at 2 26 06 PM" src="https://github.com/user-attachments/assets/6afee69c-0527-4779-b6e2-71e51c48cc42" />

`keeper:af6c6afb:98c81e08` is taken as the offering, it opens the 3rd chamber which looks like:

<img width="944" height="619" alt="Screenshot 2026-10-13 at 2 27 21 PM" src="https://github.com/user-attachments/assets/c2077d0e-8a71-4570-a6ac-541f17c0e0ba" />

An then there is another part to this:

<img width="1001" height="431" alt="Screenshot 2026-10-13 at 2 27 43 PM" src="https://github.com/user-attachments/assets/861bd679-f7e8-4f82-9c6a-4f55c6c89a73" />

Here it is written _the vault yields — Daedalus's own key is now yours. the forge unseals behind you, and it already knows your thread._, and we have big hex number called modulus and then there is a source file attached with it.

It looks like this:

```
import hashlib
DIGESTINFO_SHA256=bytes.fromhex('3031300d060960864801650304020105000420')
SECRET_BYTES=b'???'
def verify(sig,e,n,nonce):
    k=(n.bit_length()+7)//8
    m=pow(sig,e,n)
    mb=m.to_bytes(k,'big')
    if not mb.startswith(b'\x00\x01'):return False
    i=2
    while i<len(mb) and mb[i]==0xff:i+=1
    if i==2 or i>=len(mb):return False
    if mb[i]!=0x00:return False
    i+=1
    expected=DIGESTINFO_SHA256+hashlib.sha256(nonce).digest()+SECRET_BYTES
    return mb[i:i+len(expected)]==expected
```

Then for the ***FORGE***, after connecting to it prints the following:

<img width="956" height="395" alt="Screenshot 2026-10-13 at 2 45 20 PM" src="https://github.com/user-attachments/assets/8ee6e091-75c3-4a2a-8c2b-6b4e23059c66" />

There's some stuff written about a signature a signing exponent, in the python snippet above there's a verify() function, so this setup looks like a signature verification service, one would put some random number say 1 2 or 3, where its asking for a signing exponent, lets see what happens:


```
[connected]
D A E D A L U S   F O R G E
beyond the vault stands one door left unopened.
it answers to no name but his, and no word but a
signature only he could make.
signing exponent e: 
> -1
the forge refuses so weak a hand.
[closed]
[connected]
D A E D A L U S   F O R G E
beyond the vault stands one door left unopened.
it answers to no name but his, and no word but a
signature only he could make.
signing exponent e: 
> 2
the forge refuses so weak a hand.
[closed]
```

So it rejects everything below 3 and accepts 3 and above:

```
[connected]
D A E D A L U S   F O R G E
beyond the vault stands one door left unopened.
it answers to no name but his, and no word but a
signature only he could make.
signing exponent e: 
> 3
challenge: a7d83f48fa5e1075d87ab089b2e3201a
send one or more signature guesses (hex), one per line, per message.
> 45671234
no match in 1 attempts. the bull is not convinced.
> 12345678321
no match in 1 attempts. the bull is not convinced.
> 2345678987654323456789876543456789
no match in 1 attempts. the bull is not convinced.
> -1
no match in 1 attempts. the bull is not convinced.
```

On putting 3 it accepts and gives out a challenge, then It asks for signatures to verify.

So now there is some clarity to what exactly is this thing, it basically is asking for a signature to verify which should be a ***forged*** signature as there's written forge on multiple places aswell.

Lets start analyzing the verify function to forge a signature, start by looking up the digestinfo given: `3031300d060960864801650304020105000420`, one would look it up and find out that it is the ASN.1 DER encoding prefix used to identify a SHA-256 hash inside an RSASSA-PKCS1-v1_5 digital signature.

Lets learn about this rsa digital signature scheme:

### RSASSA-PKCS1-v1_5
Its a legacy digital signature scheme, that formats and signs a message hash using the RSA algorithm.

Signing process:

- Hash the message: Sender creates a message digest using a hash function like sha256.
- Format with ASN.1: The hash is prefixed with an ASN.1 structure that identifies the specific hash algorithm used.
- Apply passing: After we have the prefixed hash we need to create the bit length same as that of rsa modulus(n), for that we use a deterministic padding string(0x00, 0x01, a block of 0xff bytes and 0x00) prepended to the ASN.1 prefixed hash.
- Now that we have the padded block we do the RSA operation to generate the signature(s) by raising it to dth power and mod n: `s=m^d mod n`.

Verification process:

- RSA decryption: to get m back from s, raise s to the eth power and mod n.
- Check the padding structure, receiver inspects the resulting block to confirm it starts with 0x00, 0x01 followed by 0xff block and 0x00 separator.
- The compare hashes, receiver recomputes hash of the message and then compares it with the received one.

Alright so now that we know how this signature scheme works, let's continue analyzing the verify function, there is `SECRET_BYTES=b'???'`, which is later used in the expected value of the signature, so now for the verify function it take the signature, the public key, the modulus and the nonce, it does the rsa decryption process as mentioned above: `m=pow(sig,e,n)`, then it checks the first 2 prefix bytes as mentioned above: 

```
mb=m.to_bytes(k,'big')
if not mb.startswith(b'\x00\x01'):return False
```
The checks the padding bytes the block of 0xff bytes and the null separator at the end 0x00:

```
i=2
while i<len(mb) and mb[i]==0xff:i+=1
if i==2 or i>=len(mb):return False
if mb[i]!=0x00:return False
i+=1
```
The comes the actual part the digest info, hash of nonce, and the secret bytes: `expected=DIGESTINFO_SHA256+hashlib.sha256(nonce).digest()+SECRET_BYTES`, and the function finally returns `return mb[i:i+len(expected)]==expected`, which is nothing but check of everything after the null separator, by comparing it to the expected value.

Lets get to the solve part, how do we actually forge the signature, where is the vulnerability, the vulnerability lies in the fact that we have control over the public key, which in ideal cases shouldn't be like that, the service should have its own modulus and public key to check the received signature with, but when we have control over the public key we can easily forge the signature, like for the case of e=1, we can just submit the signature and the sever will raise it to 1 and find the same thing and will return that the signature is valid.

But this isnt the case here, as we checked nothing below 3 is accepted, so now forging becomes a little harder but still deterministic, coz as the powers rise we'll have to submit the cube root of the valid signature.

One last thing before we go deep into the math of forging, there's another vulnerability rooted in the algorithm itself, that this service checks only first 55+3 i.e 58 bytes of the signature whereas the signature's actual length is 256 bytes, this is just to make the process faster, but leaves out some room for forging.

Alright now that we understand most part, forget the 3 secret bytes for now, lets say we're giving the 55 bytes which are deterministic how do we calculate them? Lets first set a range for a valid signature, as the server checks only first 55 bytes, the next 201 bytes can be anything from 201 0x00 bytes to 201 0xff bytes, so the low becomes: 

```
pad=k-len(prefix)
low=int.from_bytes(prefix+b'\x00'*pad,'big')
```
where k is the modulus bit length, and the upper limit would replace ,`b'\x00'` with `b'\xff'`, now assume that we've submitted 3 as the public exponent, we can just run a loop taking cube root of the sig we make deterministically, and keep submitting it until one of them cubed mod n gives the right byte structure, to do that we use the low and high we've created and keeping adding one to low until the condition is satisfied.

You could write a basic cube root function and generate a valid signature with a given nonce, `49428acbfac916aace8c3434b578364c` in this case.

```
import hashlib
DIGESTINFO_SHA256=bytes.fromhex('3031300d060960864801650304020105000420')
def icbrt(n):
    x=1<<((n.bit_length()+2)//3+1)
    while True:
        y=(2*x+n//(x*x))//3
        if y>=x:return x
        x=y
def forge(n,nonce):
    k=(n.bit_length()+7)//8
    h=hashlib.sha256(nonce).digest()
    prefix=b'\x00\x01\xff\x00'+DIGESTINFO_SHA256+h
    pad=k-len(prefix)
    low=int.from_bytes(prefix+b'\x00'*pad,'big')
    high=int.from_bytes(prefix+b'\xff'*pad,'big')
    s=icbrt(low)
    while s**3<low:s+=1
    assert s**3<high
    return s
n=0x640f13a4bf68fc5926bc3d8acca7d598c9a4a598ada6a6994355e280e48ed6387c9bd4a2957b7310a6b03492988b6f09abb229f8c0636f8d001f4dfb8bd3837014fe5ac4f805717559ab192ff857d39ed1a506160209e669d62974a13994be7423a010a0f9efee7500a01c2275c4f62f5f98762f29aa9dbca82cfdcfc4aa9872c2d662b1134430a69fbe2cd56fac98dfcd7236abf454d317a026b8721a6a3872327ecbba42aaf1d8e1360d141adadb9b9cfccf62bd7f68ecf449ccd6da24b236c17ee35616e1b6c16eb5c51a6a5b2815b25cec9dfa96ecdec38f8b82948e81518b5665d6b3c00070190cc6a39459259064d4d6507282b404c87d8d1f954b8bc9
nonce=bytes.fromhex('49428acbfac916aace8c3434b578364c')
s=forge(n,nonce)
print(hex(s)[2:])
```
I think we understand that the ultimate target is to generate a validly padded nonce and we need the particular byte structure to appear at the sever's end depending on what power it raises it to, also this: `while s**3<low:s+=1` was the main part that I was talking about.

Lets now get to the actual challenge condition not forgetting the 3 secret bytes, we know that the server is not only checking the first 55 bytes but 58 bytes so its not all deterministic, but its not that hard aswell, all we need to do is include those 3 guess bytes in low while continuously changing that part to brute, something like this:

```
secret=guess.to_bytes(3,'big')
prefix=b'\x00\x01\xff\x00'+DIGESTINFO_SHA256+h+secret
pad=k-len(prefix)
low=int.from_bytes(prefix+b'\x00'*pad,'big')
sig=icbrt(low)
while sig**3<low:sig+=1
```
lets assume it was on normal nc a raw socket a basic pwntools solve script would look like this:

```
from pwn import *
import hashlib,gmpy2
HOST='127.0.0.1'
PORT=1337
ADMIN_N=0x640f13a4bf68fc5926bc3d8acca7d598c9a4a598ada6a6994355e280e48ed6387c9bd4a2957b7310a6b03492988b6f09abb229f8c0636f8d001f4dfb8bd3837014fe5ac4f805717559ab192ff857d39ed1a506160209e669d62974a13994be7423a010a0f9efee7500a01c2275c4f62f5f98762f29aa9dbca82cfdcfc4aa9872c2d662b1134430a69fbe2cd56fac98dfcd7236abf454d317a026b8721a6a3872327ecbba42aaf1d8e1360d141adadb9b9cfccf62bd7f68ecf449ccd6da24b236c17ee35616e1b6c16eb5c51a6a5b2815b25cec9dfa96ecdec38f8b82948e81518b5665d6b3c00070190cc6a39459259064d4d6507282b404c87d8d1f954b8bc9
DIGESTINFO_SHA256=bytes.fromhex('3031300d060960864801650304020105000420')
BATCH=4096
MAX_GUESS=1<<24

r=remote(HOST,PORT)
r.recvuntil(b'signing exponent e: ')
r.sendline(b'3')
r.recvuntil(b'a challenge glows into being: ')
nonce=bytes.fromhex(r.recvline().strip().decode())
r.recvline()

k=(ADMIN_N.bit_length()+7)//8
h=hashlib.sha256(nonce).digest()

flag=None
guess=0
while guess<MAX_GUESS and flag is None:
    n=min(BATCH,MAX_GUESS-guess)
    lines=[]
    for _ in range(n):
        secret=guess.to_bytes(3,'big')
        prefix=b'\x00\x01\xff\x00'+DIGESTINFO_SHA256+h+secret
        pad=k-len(prefix)
        low=int.from_bytes(prefix+b'\x00'*pad,'big')
        sig,exact=gmpy2.iroot(low,3)
        sig=int(sig)
        if sig**3<low:sig+=1
        lines.append(hex(sig)[2:])
        guess+=1
    r.send(('\n'.join(lines)+'\n').encode())
    data=r.recvrepeat(0.2)
    if b'labyrinth{' in data:
        flag=data.decode()

print(flag)
r.close()
```
I user iroot for this because its way faster than a manually written icbrt() function.

Now that we completely understand the solve, we know that this was not a raw socket, it was a web socket that we had to deal with, serious speed and connection issues one might face, if the solve is not optimized enough, the solve script for that was:

```
import websocket,hashlib,gmpy2,ssl
from gmpy2 import mpz

BASE='thread-sock-8788ca030fa8c26f.chalz.labyrinthctf.live'
ADMIN_N=0x640f13a4bf68fc5926bc3d8acca7d598c9a4a598ada6a6994355e280e48ed6387c9bd4a2957b7310a6b03492988b6f09abb229f8c0636f8d001f4dfb8bd3837014fe5ac4f805717559ab192ff857d39ed1a506160209e669d62974a13994be7423a010a0f9efee7500a01c2275c4f62f5f98762f29aa9dbca82cfdcfc4aa9872c2d662b1134430a69fbe2cd56fac98dfcd7236abf454d317a026b8721a6a3872327ecbba42aaf1d8e1360d141adadb9b9cfccf62bd7f68ecf449ccd6da24b236c17ee35616e1b6c16eb5c51a6a5b2815b25cec9dfa96ecdec38f8b82948e81518b5665d6b3c00070190cc6a39459259064d4d6507282b404c87d8d1f954b8bc9
SESSION_COOKIE='eyJzdGFnZSI6M30.astmJw.B--mCcAfQGWE_9kqJt7Iluv2EVY'
DIGESTINFO_SHA256=bytes.fromhex('3031300d060960864801650304020105000420')
BATCH=16384
MAX_GUESS=1<<24

def read_batch_response(ws):
    msg=ws.recv()
    if 'labyrinth{' in msg:return msg
    ws.settimeout(0.05)
    try:
        msg2=ws.recv()
        if 'labyrinth{' in msg2:return msg2
    except Exception:
        pass
    finally:
        ws.settimeout(None)
    return None

def main():
    ws=websocket.create_connection('wss://'+BASE+'/ws/forge',header=[f'Cookie: session={SESSION_COOKIE}'],sslopt={'cert_reqs':ssl.CERT_NONE})
    banner=ws.recv()
    if 'does not yet know you' in banner:
        print(banner)
        ws.close()
        return
    ws.send('3')
    ws.recv()
    challenge=ws.recv()
    nonce=bytes.fromhex(challenge.split('challenge: ')[1].strip())
    ws.recv()
    k=(ADMIN_N.bit_length()+7)//8
    h=hashlib.sha256(nonce).digest()
    header=b'\x00\x01\xff\x00'+DIGESTINFO_SHA256+h
    pad=k-len(header)-3
    delta=mpz(1)<<(8*pad)
    low=mpz(int.from_bytes(header+b'\x00'*3+b'\x00'*pad,'big'))
    flag=None
    guess=0
    try:
        while guess<MAX_GUESS and flag is None:
            n=min(BATCH,MAX_GUESS-guess)
            lines=[]
            for _ in range(n):
                sig,exact=gmpy2.iroot(low,3)
                if sig**3<low:sig+=1
                lines.append(gmpy2.digits(sig,16))
                low+=delta
            ws.send('\n'.join(lines))
            guess+=n
            resp=read_batch_response(ws)
            if resp and 'labyrinth{' in resp:flag=resp
    finally:
        ws.close()
    print(flag if flag else 'no match')

if __name__=='__main__':
    main()
```

This does the same thing just on a web socket and using its syntax, we need the base url and the session cookie once you reach chamber 3 to run this.

Running this gives the flag: `labyrinth{n07_3x4c7ly_bu7_y34h_k1nd4_l1k3_bl31ch3nb4ch3r}`

Read about the [Bleichenbacher attack](https://medium.com/@c0D3M/bleichenbacher-attack-explained-bc630f88ff25)

### Some thoghts on making of the challenge

The part about the user having control over the public exponent was inspired from: [CVE-2026-67276](https://cert.pl/en/posts/2026/09/vulnerabilities-in-mikrotik-routeros-actively-exploited/), surprisingly such very easy to identify vulnerabilities are still out there.


### Resources

[Hashes](https://www.geeksforgeeks.org/dsa/hash-functions-and-list-types-of-hash-functions/), [websockets](https://pypi.org/project/websockets/#description), [SQLi UNION attacks](https://portswigger.net/web-security/sql-injection/union-attacks), can also look up RSA signature and encryption schemes, to understand math, for basics of RSA refer to [this](https://en.wikipedia.org/wiki/RSA_cryptosystem) and nothing else.













