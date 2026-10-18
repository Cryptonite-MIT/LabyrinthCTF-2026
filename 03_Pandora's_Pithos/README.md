# 03. Pandora's Pithos

Author: Hitu1197

Phase 1 | forensics

Flag: `labyrinth{p4nd0r4s_s3cr3t_unl34sh3d}`

## Description

A forbidden container lies buried inside the artifact...

## Solve

- First binwalk, then extract to get a zip
- Then the zip has password
- Brute using rock you
- password will give a hit at `andreina`
- Btw extracted hash is `$pkzip$1*1*2*0*94*88*53071560*0*28*0*94*5307*b01c1b51a1d67d8150a94a9dae3791d9d9cefd7f8ee20d6e84710077ad00afe22af6252d605debb7add41b833eb5c0cbdeb501bd3158dfdedd847912dd116e80e853b874509c1e4ba49eb877cf37f7799fe7bd4cafda0f923af5459fb4927b3753491fbedaca074188f30afb4352e0639b8fca072bffcaa9b6fe3fcf26a3fb98d5fcdfcac9c258c775adbfd5bc5d7e44907e5c43*$/pkzip$`
- Flag: `labyrinth{p4nd0r4s_s3cr3t_unl34sh3d}`

