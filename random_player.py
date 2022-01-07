import random
import numpy as np

class Player: 
    """
    Called when the player is created. Set everything up here. 
    """
    def __init__(self):  
        self.ID = 6969 # This can be anything, it will get over written but its important for you to know it is here. (CAN NOT BE ZERO.)
        self.COLOR = np.random.rand(3) * 255

    # Give your AI a name. 
    def __str__(self): 
        return "Random player"

    """
    The function used by the game to get a move from your AI. 
    State: The state of the game board this is a dictionary with different values for different keys. 
        "board"         : a 9x9 numpy array representing the board with player IDs or 0s representing who is in which spot (0 is nobody.)
        "next_x"        : the x cordinate of the quareant you must move into. (None = Any)
        "next_y"        : the y cordinate of the quareant you must move into. (None = Any)
        "opponent_x"    : the x cordinate of the quareant your opponent must move into. (None = Any)
        "opponent_x"    : the y cordinate of the quareant your opponent must move into. (None = Any)
        "id"            : the id of the current player. 
        "opponent"      : the id of your opponent.
    get_legal_moves: A function that you can call to get a list of legal moves for a given state. 
        you should run get_legal_moves(state) to get a list of moves.

    A move is represented as a tuple of the (x, y) cordinate you want to put a peice in. 
    """
    def get_move(self, state, get_legal_moves): 
        moves = get_legal_moves(state)
        if len(moves) > 0: 
            move = random.choice(moves)
        else:
            move = None
        return move
