# 12. Dyne doesn't like vinegar

Author: pin3apple07

Phase 2 | crypto

Flag: `labyrinth{metamorphosis_cryptography_conundrum}`

## Description

When you turn past the next corner, to your surprise you find a message though you cant possibly know from who. Could it possibly be from someone else who reached this point but could not find the way forward? Seems unlikely. The message is as follows:

***Ugw lkc jv cuvjc vme'n akukdtcz: kqerxkubm{axlpouweepazc_bzgctayltwwe_jjdtfkkus} Hxrn jw uapbgzn vgt ap lvfgznjtl wmbvjnm ld ljbqhdd mjl osnwh'u smdz idpow, fwptnctt nkk cgpy kdln kjdj mz gi jmn, kkob rdc fk elgjb?***

Labyrinth was nice, someone called Dyne and his gang have been screening it, there's gonna be one show on 9/11 I think, I can't remember the name of a place south of the music hall where the show is gonna be.

Probably the name of the town holds a way to find the secret.

You might wanna look for the theme song of the 80's classic maybe that's the key to the secret.

## Solve

The description mentions the movie _labyrinth_, and it being screened by someone called `Dyne` and his gang, here dyne is the name of one of the band members who've been performing for [this](https://www.labyrinthinconcert.com), then the show at 9/11 was mentioned which was meant to be interpreted as `9th November 2026`.

Further if you look for the show at that exact date you'll find that it's happening in ***Charleston Hall***, Charleston, South Carolina, USA, now the next part of the description mentioned that the name of the cipher is the name of a town south of this venue, then one would stumble upon ***Beaufort***.

After getting the name of the cipher, the solver will have to go to [dcode.fr](https://www.dcode.fr) or a related website to decipher the ciphertext, the key to be used was mentioned in the description's following line:

```
You might wanna look for the theme song of the 80's classic maybe that's the key to the secret.
```
The key to be used was `UNDERGROUND`, once you decipher you get the following:


```
Ahh the it still isn't readable: ubcarktci{ngtcsxsqjouob_dsapvupsbrha_ixovpdtav}

What is another way of ciphering similar to vinegar but doesn't like words, probably the show date will be of use, what was it again?
```

Now the next cipher was `vigenere` but for a number as key, and the key to be used was `9112026` i.e the date of the show, now the cipher was the _Gronsfeld cipher_, deciphering using the correct key you get the flag:

```
labyrinth{metamorphosis_cryptography_conundrum}
```

