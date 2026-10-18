# 11. Loom Of The Fates

Author: kMadScientist

Phase 2 | rev

Flag: `labyrinth{Cr0ch3t_W17h_7h3_7hr34d5_0f_F473}`

## Description

You descend the steps and are greeted by the Moirai. They welcome you to their floor. They require that you not proceed further. Can you untangle the weaves of the Fates themselves and complete your mission? 

Handout: [Examples.yarn](public/Examples.yarn)

## Solve

We have been given a mysterious file Examples.yarn. On reading the file, we see the following:

```
## Hello World

"Hello World!" INSPECT

## Hello User

"Hello " DRAFT TIE INSPECT

## Reverse

DRAFT REVERSE INSPECT

## Palindrome

DRAFT DOUBLE REVERSE DYE INSPECT

## Print Input

DRAFT DRAFT CROSS INSPECT INSPECT

## Reverse Halves

DRAFT SEVER CROSS TIE INSPECT

## Secret Note

DRAFT "13" SHIFT INSPECT
```

There is also an instance available. On connecting to the instance, we can see the following:

```
=== THE LOOM OF THE FATES ===
Welcome, mortal, to the weaving floor of the Moirai.
1. Practice at the Loom
2. Proceed forward
> 
```

If we select option 2, we are greeted with the following:

```
The thread leading you forward has been meddled with.
The Moirai in an attempt to stall you have:
  1. severed the thread, splitting it in half
  2. shifted the pattern of the left half by 10
  3. reversed the flow of the left half
  4. dyed the right half with the key "HADES"
  5. tied the broken ends back together

The mangled thread is currently at the top of your stack.
Your journey forward will be blind. How will you untangle the thread?
> 
```

We can deduce that it is telling us the way in which the flag has been mangled and that it is sitting on top of the stack.

If we choose option 1, we are shown the following prompt:

```
What will you weave?:
> 
```

If we enter any of the example programs provided to us, we can see their results. Utilising this, we can figure out that this is a stack based string manipulator where we can control what happens to the strings on the stack. With some trial and error, we can also figure out what each command does.

We can then use this knowledge to reverse the mangling of the flag that is on the stack by undoing the operations mentioned in the message that is printed on selecting option 2.

Solution program:

```
SEVER "HADES" DYE CROSS REVERSE "-10" SHIFT CROSS TIE INSPECT
```