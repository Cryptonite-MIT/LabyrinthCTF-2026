# 06. its2low

Author: ric0

Phase 1 | crypto

Flag: `labyrinth{itsCeaser_just_little_different_with_vignere}`

## Description

I made the key using this song, but remember we have to sing key or two higher
and now that the keys hidden, none of you will find the secret message.

(note we represent notes in western notation. C sharp `C#` is written as Cs)

flag has to be wrapped in the wrapper labyrinth{}

## Solve

## flag

`labyrinth{itsCeaser_just_little_different_with_vignere}`

## Solve

- This is an audio steganography challenge. The first step is to inspect the spectrogram of challenge.wav
- The original notes of the key are hidden in the frequencies of the file
- You can do audio spectography using an application like audactiy, which gives you the base64 (a form of encoding) of the original notes: `Y2JnZWNkZWZnYw==`
- This decodes to `cbgecdefgc` (you can do this using cyberchef or many other resources)
- The description of the challenge (and the name) hints that the challenge has to be sung 2 semitones higher, or in D major scale. So we shift it (akin to a ceaser cipher with musical notation)
- key: `DCsAFsDEFsGAD` (following the format)
- Thus we can use this key to decrypt the ciphertext which is encrypted using a vignere cipher. 

