# 30. The Bronze Maze

Author: Phoenix

Phase 3 | hardware

Flag: `labyrinth{11001011010}`

## Description

Daedalus built a labyrinth from bronze and glass. Eleven thresholds guard its mouth, just like Cerberus guards the gates of hell, each admitting only light or dark. The gate called Y stays bright for every traveller but one, whose path sinks it toward the river.

Find that path. Write the thresholds in order, light as 1 and dark as 0.
Daedalus's keepers are not mere switches. Each pair of bronze guardians speaks a single word -> AND, OR, NOT, XOR. Learn their language, and the labyrinth becomes a sentence.

## Notes
Every keeper in the labyrinth is a BC547, powered by 5 V.
The sinking is a shallow dip, not an abyss.

Flag -> labyrinth{a1a2...a11}

## Solve


### Step 1: Output gate

Y is the output of a 14-input NAND, so Y = 0 only when all 14 inputs are 1.

Each input is either a first-layer gate (G3, G12, G17, G24) or a second-layer gate S1..S10 that combines two first-layer gates.

### Step 2: Single-gate terms
These four feed the NAND directly:

 `G3` is ~a11 · a5 which means 
 `a11 = 0, a5 = 1`
 similirly 
 
`G24` ~a11 · a1
`a1 = 1`


`G17`
a2 · a1
`a2 = 1`


`G12`
a7 · a2
`a7 = 1`

Known so far: a1=1, a2=1, a5=1, a7=1, a11=0.

### Step 3: Second-layer terms
Substitute the known values. Each term forces one more input.

### Step 4: Remaining terms
Substitute all eleven values into the five terms not used above:

`S1 = G1 + G2 = (a2+a3) + XNOR(a4,a11) = 1 + … = 1`


` S2 = NAND(G4, G5), with G4 = ~a5 · a1 = 0, so S2 = 1`


`S5 = NAND(G10, G11), with G10 = XOR(a11,a4) = 0, so S5 = 1`


`S6 = G13 ⊕ G14 = XOR(a7,a2) ⊕ (a8 + ~a10) = 0 ⊕ 1 = 1`


`S7 = XNOR(G15, G16) = XNOR(XNOR(a8,a7), NAND(a5,a6)) = XNOR(1,1) = 1`



All 14 inputs of the NAND are 1, so Y = 0.
 

`11001011010`
