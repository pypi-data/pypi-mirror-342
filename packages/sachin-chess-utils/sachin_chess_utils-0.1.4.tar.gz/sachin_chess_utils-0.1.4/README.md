# sachin-chess-utils

General propose Chess related utility functions.
Some examples below.

### 1. Convert chess move to human readable sentence:

```
from sachin_chess_utils import describe_move

print(describe_move('Nxe4#'))
```

Output:
`"knight captures e4 check and mate"`

- This is useful for the text to speech model. Machine can "say" the moves.
- Function might look simple at first glance but there are **some corner cases which are handled here** (That's why I thought to make it open source).

### 2. Many more such functions are work in progress 🚀

....
