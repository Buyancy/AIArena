from math import floor
import pygame
import numpy as np
import time
import sys
import threading
import copy
from pprint import pprint 

# If we are debugging/want verbose output. 
SMOKE = False
def smoke(val): 
    if SMOKE: 
        print(val)

# A way to gracefully exit the game. 
def exit_game(): 
    print("Game window closed.")
    exit(0)

pygame.init()

WIDTH = 800
HEIGHT = 800

window = pygame.display.set_mode((WIDTH, HEIGHT))

colors = np.ones(shape=(9,9,3)) * 255

# The gameboard. 
board = np.zeros(shape=(9,9))

# The winner. 
winner = None

# The players.
if len(sys.argv) == 3: 
    player_1 = __import__(sys.argv[1]).Player()
    player_2 = __import__(sys.argv[2]).Player()

    player_1.ID = 1
    player_2.ID = 2 

    players = [player_1, player_2]
else: 
    print(f"Please supply the two players. Args: {sys.argv}")
    exit(1) 

running = True
last_frame = time.time()

# A way for the players to get a list of legal moves. 
def get_legal_moves(state): 
    smoke("Getting legal moves.")

    player_id = state["id"]
    board = state["board"]
    x = state["next_x"]
    y = state["next_y"]
    moves = []
    if x == None and y == None: 
        for i in range(3):
            for j in range(3):
                for x in range(3):
                    for y in range(3): 
                        if board[x*3 + i, y*3 + j] == 0: 
                            moves.append((x*3 + i,y*3 + j))
    else:
        for i in range(3):
            for j in range(3): 
                if board[x*3 + i, y*3 + j] == 0: 
                    moves.append((x*3 + i, y*3 + j))

    smoke("Done getting legal moves.")
    return moves

# A function that will return the winner of a game board. Returns none if there is a tie. 
meta_board = np.zeros(shape=(3,3)) # Want to keep the winner as the first person to win. 
def check_winner(board, p1, p2):
    smoke("Checking winner.")
    # A sub-function to check for a 3x3 win. Takes a 3x3 numpy array. 
    def small_win(board):
        # Vertical and horizontal win check. 
        for i in range(3): 
            if np.array([board[i, j] == p1 for j in range(3)]).all() or np.array([board[:, i] == p1 for j in range(3)]).all():
                return p1
            if np.array([board[i, j] == p2 for j in range(3)]).all() or np.array([board[j, i] == p2 for j in range(3)]).all():
                return p2
        # Check the diagonal wins. 
        if np.array([board[i,i] == p1 for i in range(3)]).all() or np.array([board[i,2-i] == p1 for i in range(3)]).all():
            return p1
        if np.array([board[i,i] == p2 for i in range(3)]).all() or np.array([board[i,2-i] == p2 for i in range(3)]).all():
            return p2
        return 0

    for i in range(3): 
        for j in range(3):
            if meta_board[i,j] == 0: 
                small_board = board[i*3:i*3 + 3, j*3 : j*3+3]
                meta_board[i, j] = small_win(small_board)

    w = small_win(meta_board)

    smoke("Done checking winner.")
    return w

# A function that will draw the board. 
# Draw the background. 
def draw_board():
    smoke("Drawing board.")

    window.fill("black")

    w_unit = WIDTH / 10
    h_unit = HEIGHT / 10
    w_margin = WIDTH / 100
    h_margin = HEIGHT / 100

    # Draw the inter-board lines. 
    for i in range(3):
        pygame.draw.line(window, "red", ((i * (w_unit + w_margin) * 3) + w_margin/2, 0),((i * (w_unit + w_margin) * 3) + w_margin/2, HEIGHT), int(w_margin * 2))
        pygame.draw.line(window, "red", (0, (i * (h_unit + h_margin) * 3) + h_margin/2),(WIDTH, (i * (h_unit + h_margin) * 3) + h_margin/2), int(w_margin * 2))
    pygame.draw.line(window, "red", (WIDTH, 0),(WIDTH, HEIGHT), int(w_margin * 2))
    pygame.draw.line(window, "red", (0, HEIGHT),(WIDTH, HEIGHT), int(w_margin * 2))


    # Draw the player positions from the color array. 
    for i in range(3): 
        for j in range(3):
            for x in range(3): 
                for y in range(3): 
                    w_cord = (i * 3) + x
                    h_cord = (j * 3) + y
                    pygame.draw.rect(window, colors[i *3 + x, j * 3 + y], (h_cord * (h_unit + h_margin) + h_margin, w_cord * (w_unit + w_margin) + w_margin, h_unit + 1, w_unit + 1))

    # update the display. 
    pygame.display.flip()

    smoke("Done drawing board.")


# The game loop.
player_turn = 0
player_last_move = [(None, None), (None, None)]
while running: 
    # Quit the game if we are done. 
    for event in pygame.event.get(): 
        # Quit if the window is closed. 
        if event.type == pygame.QUIT:
            exit_game()

    # Draw the super-tic-tack-toe board every 1/5 of a second. 
    if time.time() > last_frame + 1/5: 
        last_frame = time.time()
        draw_board()
    
    # Playing the game. 
    smoke("Assigning players.")
    current_player = players[player_turn]
    opponent = players[1-player_turn]

    # The state of the game board. 
    smoke("Building state.")
    last_x, last_y = player_last_move[player_turn]
    opponent_last_x, opponent_last_y = player_last_move[1-player_turn]
    state = {
        "board" : copy.deepcopy(board), 
        "next_x" : last_x, 
        "next_y" : last_y, 
        "oponent_x" : opponent_last_x, 
        "oponent_y" : opponent_last_y, 
        "id" : current_player.ID, 
        "opponent" : opponent.ID, 
    }
    smoke("Done building state.")

    # Get the move from the player. 
    smoke(f"Getting move for {current_player}.")
    start_time = time.time()
    move = current_player.get_move(state, get_legal_moves)
    if time.time() - start_time > 5.0: 
        print("Time limit exceded.")
        winner = opponent
        break
    smoke(f"Done getting move for {current_player}. Move: {move}.")
    

    # Verify that it is a valid move. 
    if move == None: # The player is passing the move and will be free to move anywhere next turn. 
        mx, my = None, None
    else:
        mx, my = move 
        if board[mx, my] != 0: # Not a valid move. 
            print(f"Invalid move, invalid location. ({mx}, {my})")
            winner = opponent
            running = False 
            break
        if last_x != None and last_y != None:
            if floor(mx / 3) != last_x or floor(my / 3) != last_y:
                print(f"Invalid move, wrong quadrant. ({mx}, {my})")
                winner = opponent
                running = False 
                break
    

        # Apply the move to the game board.
        board[mx, my] = current_player.ID

        # Update the colors. 
        colors[mx, my] = current_player.COLOR

    # Check for a winner. 
    winner_id = check_winner(board, current_player.ID, opponent.ID)
    if winner_id != 0: 
        running = False
        winner = player_1 if winner_id == player_1.ID else player_2
        break

    # Check for a draw. 
    if np.array([c != 0 for c in board.flat]).all():
        print("This game is a draw.")
        winner = None
        break

    # Update the last and next move. 
    if mx != None and my != None:
        player_last_move[player_turn] = (mx % 3, my % 3)
    else: 
        player_last_move[player_turn] = (None, None)

    # Change the player turn for the next move. 
    player_turn = 1 - player_turn 

# Wrap up the game by saving stats and printing the winner. 
print(f"The winner is: {winner}")
pprint(board)
pprint(meta_board)

# Keep the window upen while we view the end state of the board. 
running = True
draw_board()
while running:
    # Quit the game if we are done. 
    for event in pygame.event.get(): 
        # Quit if the window is closed. 
        if event.type == pygame.QUIT:
            exit_game()