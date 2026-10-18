# 16. death-trap

Author: bitf1ip

Phase 2 | rev

Flag: `labyrinth{m1m1c_3nj0ys_d3ath_tr4ps}`

Handout: [deathtrap](./handout/deathtrap)

## Description

You stumble upon a room with a chest at the end of it. You think it might contain the next key. 
Just as you begin to make your way towards it, you recieve a mysterious warning. The source seems to be those who are dead. 
They scream to you from the abyss to tread carefully. They say "You can move to one of the 4 tiles in each row of the room but you may end up dead in the search for treasure."

Usage: `./deathtrap <moves>`

> Disclaimer: All the files are safe to download and run

## Solve

- Open the challenge file `deathtrap` in IDA

- You can see that there is a `reveal_flag` function

> reveal_flag
```c
unsigned __int64 __fastcall reveal_flag(int a1)
{
  int i; // [rsp+18h] [rbp-98h]
  char v3[136]; // [rsp+20h] [rbp-90h] BYREF
  unsigned __int64 v4; // [rsp+A8h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  for ( i = 0; i < 35; ++i )
    v3[i] = (a1 + i) ^ move_key((unsigned int)((i + a1) % 4)) ^ encoded_flag[i];
  v3[35] = 0;
  printf(
    "The chamber falls silent. The chest turns out to be a mimic but just before trying to eat you it says: \n%s\n",
    v3);
  return v4 - __readfsqword(0x28u);
}
```

- there you can trace the fsm logic through the function `move_key` and the byte array `encoded_flag`. You can also see that everything in reveal_flag is based on the input v7 which is checked based on `transitions`

- We can also observe in the `main` function that the inputs you enter are encoded before getting checked using `encode_move` 

- Using this we can just find out the valid move sequence required to get the flag

> input_finder.py
```python
from collections import deque

transitions = [
    0xFF, 1, 0xFF, 0xFF,
    2, 0xFF, 0xFF, 0,
    0xFF, 3, 1, 0xFF,
    0xFF, 0xFF, 4, 2,
    0xFF, 3, 0xFF, 5,
    6, 0xFF, 4, 0xFF,
    0xFF, 7, 5, 0xFF,
    0xFF, 0xFF, 8, 6,
    0xFF, 0xFF, 0xFF, 0xFF,
]

move_map = {0: "1", 1: "2", 2: "3", 3: "4"}


def solve_maze():
    queue = deque([(0, "", 0)])
    visited = set()

    while queue:
        state, path, v7 = queue.popleft()

        if state == 8:
            return path, v7

        if (state, len(path)) in visited:
            continue
        visited.add((state, len(path)))

        for move in range(4):
            next_state = transitions[4 * state + move]
            if next_state != 0xFF:
                queue.append(
                    (next_state, path + move_map[move], v7 + next_state)
                )

    return None, None


if __name__ == "__main__":
    solution, flag_arg = solve_maze()
    if solution:
        print(f"input4u: {solution}")
```

```bash
•  python3 input_finder.py
input4u: 21234123
```

- Then just run the challenge file with the correct input and get da flag

```bash
•  ./main 21234123
You stand at the entrance and walk the path you chose.
The chamber falls silent. The chest turns out to be a mimic but just before trying to eat you it says:
labyrinth{m1m1c_3nj0ys_d3ath_tr4ps}
```

> flag
```
labyrinth{m1m1c_3nj0ys_d3ath_tr4ps}
```

