# AIArena
 
This is a project that allows the competition of two AI algorithms to play super-tic-tak=toe. 

## Usage 

The game is run by executing the command ```python arena.py file1 file2``` where ```file1.py``` and ```file2.py``` are files that each have a player class in them. A player class should have the same form as the example random player defined below. 

```python
import random
import numpy as np

class Player: 
    def __init__(self):  
        self.ID = 6969 # This can be anything, it will get over written but its important for you to know it is here. (CAN NOT BE ZERO.)
        self.COLOR = np.random.rand(3) * 255

    # Give your AI a name. 
    def __str__(self): 
        return "Random player"

    def get_move(self, state, get_legal_moves): 
        moves = get_legal_moves(state)
        if len(moves) > 0: 
            move = random.choice(moves)
        else:
            move = None
        return move
```
The ```get_move``` function takes two arguments. 
* ```state``` is the state of the game. It is a dict with the following values. 
    * ```"board"```         : a 9x9 numpy array representing the board with player IDs or 0s representing who is in which spot (0 is nobody.) This is a COPY of the actuial game board so you can feel free to mutate it however you want. 
    * ```"next_x"```        : the x cordinate of the quareant you must move into. (None = Any)
    * ```"next_y"```        : the y cordinate of the quareant you must move into. (None = Any)
    * ```"opponent_x"```    : the x cordinate of the quareant your opponent must move into. (None = Any)
    * ```"opponent_x"```    : the y cordinate of the quareant your opponent must move into. (None = Any)
    * ```"id"```            : the id of the current player. 
    * ```"opponent"```      : the id of your opponent.
* ```get_legal_moves``` is a function that you can call. It takes a game state as the argument (see above) and returns a list of valid moves. (Beware, this list may be empty if there are no legal moves. In this case, the AI should return None and pass the turn otherwise it will break the rules and lose.)
* ```self.COLOR``` is the color that the AI's peices will be rendered as. 

## Rules
* Dont try to meta game by changing the ID of your AI or interrupt the opponent AI (unless we decide that should be fair game.)
* Your AI has exactly 5 seconds to return a move or it forfits the game. 
* The move must be a tuple of the form ```(x,y)``` where ```x``` and ```y``` are integers between 0 and 9 (exclusive.) 
* Your program MUST be single threaded.
* Please be gentile, I only have 8G of RAM.
* Thats pretty much it. 


## Python Libraries Installed in Environment
* PyGame
* Numpy
* Pandas
* SciPy
* SkLearn
* PyTorch
* TensorFlow
* Keras

Requests are welcome.