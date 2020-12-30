# Implementation and solver for tic-tac-two

### Game description:
- Two players take turns placing their pieces on a 3-by-3 grid (similar to regular tic-tac-toe)
- Player wins if they have 3 claimed squares in a line (horizontal, vertical, or diagonal)
- Player claims square when they are the first to get 2 of their own piece on the square
- Once per game, each player may move twice in a row.

### Current Solve:
```
Tic Tac Two analysis (symmetries not removed):
Remote  Win      Lose     Tie      Total
----------------------------------------
18      0        20       0        20     
17      568      0        1        569    
16      0        2482     75       2557   
15      7234     0        1428     8662   
14      0        21149    6827     27976  
13      38564    0        24433    62997  
12      0        90690    74186    164876 
11      143504   0        175737   319241 
10      0        301409   358704   660113 
9       470348   0        557742   1028090
8       0        755458   760417   1515875
7       1307413  0        775593   2083006
6       0        1590872  723568   2314440
5       3088869  0        484852   3573721
4       0        2919959  308808   3228767
3       4744654  0        139236   4883890
2       0        3175931  72784    3248715
1       10171698  0        7456     10179154
0       0        1005144  256      1005400
------------------------------------------
Total   19972852  9863114  4472103  34308069


```

### Updates:
10/19/20 (brian): Minor bugfixes to match Prof. Garcia's solution

10/12/20 (brian): Switched to tie-quickly solve, added symmetry and non-symmetry solves to README.

10/3/20 (janise): fixed formatting for output and added capture of current output. will verify correctness and try to optimize -- currently solves in 58 seconds on my computer

10/2/20 (brian): Uploaded own base code, with possible TT2 implementation. No guarantee it actually works, and definetly not efficient.

9/30/20 (janise): uploaded tic tac toe, solver, and Game abstract class to use as base code
