# 17. The Trojan Pixel

**Author**: ryd3r <br>
**Category**: Forensics <br>
**Difficulty**: Medium

## Description
The walls of the labyrinth stand intact, but a deceptive format at the entrance scrambles the path inside. Can you get past these gates?

## Solve

- We are given a QR code image titled `broken.png`. On trying to scan it, we can see that the QR code does not lead to anything and is likely *broken*.
- On searching for *QR code recovery*, we can find [**QrazyBox**](https://merri.cx/qrazybox/). We can upload the given image there.
- Click on the any of the finder patterns of the QR, we can change it's format information.
- Bruting it for all combinations the *error correction level* and *mask pattern*, we can try to extract information from *Tools > Extract QR Information*.
- The value *M, 1* lets you decode the QR and find the flag.

## Flag: `labyrinth{i_l0v3_7his_ch3ckm473_p4773rn}`
