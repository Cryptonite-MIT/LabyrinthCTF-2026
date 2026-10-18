# 02. parent=hidden?

Author: ric0

Phase 1 | webex

Flag: `labyrinth{norse_gods_know_how_to_talk_to_their_parents}`

## Description

When doing an initial recon, you come across an innocent looking website about the gods you fear. But investigate and you might find the a file that will lead you forward.

https://parent-dr.vercel.app/

## Solve

- Must do basic LFI to access parent directory, and get the hidden file <br>
`/read.php?path=../NotGreekMyth.txt`

