# TetrisPy
Tetris implemented using pygame.

## How to play
1. Clone the repo
2. [Install pygames](https://www.pygame.org/wiki/GettingStarted)
3. Run main.py file (Tested on Python 3.10.4)

    >```python3 main.py```

## Keybinds
`Arrow-Left`: Move left  
`Arrow-Right`: Move right  
`Arrow-Up`: Rotate clockwise  
`Z`: Rotate counterclockwise  
`Arrow-Down`: Softdrop  
`Space`: Harddrop  
`C`: Hold piece

## Features
Implements most of the featrues associated with modern, guideline Tetris, including:
- Piece movement:
    - left and right movement
    - soft and hard drop
    - clockwise, counterclockwise and 180 degrees rotations
- Variable DAS, ARR
- Variable softdrop and normal gravity
- Debounce to prevent multiple inputs on single press
- Holding
- Piece queue
- Piece shadow
- 7-bag randomizer
- SRS kicktable for piece rotations
- T-spins

## Scoring
Different types of line clears are scored as follows:
|**Line clear**|**Points**|
|:-----|:-----|
|Single|1|
|Double|100|
|Triple|200|
|Quad (**Tetris**)|400|
|T-Spin Single (**TSS**)|200|
|T-Spin Double (**TSD**)|400|
|T-Sping Triple (**TST**)|600|

## Unimplemented Features
Features that I *might* come back around to implementing (eventually)
- Perfect clears
- Back-to-Back
- Comboes
- Infinite ARR (currently the fastest possible speed is a rate of 1 move per frame)
- Configurable keybinds

Features that I *won't* implement
- (Hurry up) Garbage
- Ramping up gravity
