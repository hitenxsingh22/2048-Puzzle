import random
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Initialize the board
def init_board():
    board = np.zeros((4, 4), dtype=int)
    add_random_tile(board)
    add_random_tile(board)
    return board

# Add a random tile (2 or 4) to the board
def add_random_tile(board):
    empty_tiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4

# Slide a row left (merge tiles if necessary)
def slide_left(row):
    new_row = [i for i in row if i != 0]
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [i for i in new_row if i != 0]
    return new_row + [0] * (4 - len(new_row))

# Movement functions
def move_left(board):
    new_board = np.zeros((4, 4), dtype=int)
    for i in range(4):
        new_board[i] = slide_left(board[i])
    return new_board

def move_right(board):
    new_board = np.zeros((4, 4), dtype=int)
    for i in range(4):
        new_board[i] = slide_left(board[i][::-1])[::-1]
    return new_board

def move_up(board):
    new_board = np.zeros((4, 4), dtype=int)
    for j in range(4):
        col = slide_left(board[:, j])
        for i in range(4):
            new_board[i][j] = col[i]
    return new_board

def move_down(board):
    new_board = np.zeros((4, 4), dtype=int)
    for j in range(4):
        col = slide_left(board[::-1, j])[::-1]
        for i in range(4):
            new_board[i][j] = col[i]
    return new_board

# Check if there are any possible moves
def can_move(board):
    if np.any(board == 0):
        return True
    for i in range(4):
        for j in range(4):
            if (i < 3 and board[i][j] == board[i + 1][j]) or (j < 3 and board[i][j] == board[i][j + 1]):
                return True
    return False

# Check if the player has won (reached 2048)
def game_won(board):
    return np.any(board == 2048)

# Update the GUI with the current board state
def update_gui(board, labels):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            labels[i][j].config(text=str(value) if value != 0 else '', bg=get_tile_color(value))

# Tile background color based on value
def get_tile_color(value):
    colors = {
        0: "#cdc1b4", 2: "#d9e3f0", 4: "#c4d4f0", 8: "#a0c1f0", 16: "#7da8e0",
        32: "#5b8ed0", 64: "#3f78b0", 128: "#56c79f", 256: "#42a982", 512: "#2e8b57",
        1024: "#6a67ce", 2048: "#5539c7", 4096: "#3b2c8a"
    }
    return colors.get(value, "#3c3a32")

# Display a message box for winning or losing
def check_game_state(board, labels, root, game_continued):
    if game_won(board) and not game_continued[0]:  # Check if player won and if they haven't been asked to continue
        game_continued[0] = True  # Set flag to True after asking once
        if messagebox.askyesno("Congratulations!", "You've reached 2048! Do you want to continue?"):
            return
        else:
            play_game_gui(root, labels)  # Start a new game if user chooses not to continue
    elif not can_move(board):  # Check if there are no more moves
        messagebox.showinfo("Game Over", "No more moves possible!")
        play_game_gui(root, labels)  # Start a new game if user loses

# Handle key press events for arrow keys
def key_event(event, board, labels, root, game_continued):
    direction = event.keysym
    new_board = board.copy()
    
    if direction == 'Up':
        new_board = move_up(board)
    elif direction == 'Left':
        new_board = move_left(board)
    elif direction == 'Down':
        new_board = move_down(board)
    elif direction == 'Right':
        new_board = move_right(board)
    else:
        return

    if not np.array_equal(board, new_board):  # Check if the board actually changes
        board[:] = new_board
        add_random_tile(board)
        update_gui(board, labels)
        check_game_state(board, labels, root, game_continued)

# Start the game with GUI
def play_game_gui(root=None, labels=None):
    if root is None:
        root = tk.Tk()
        root.title("2048 Game")

    board = init_board()
    game_continued = [False]  # Use a list to make the flag mutable inside functions

    # If labels grid does not exist, create it
    if labels is None:
        labels = [[tk.Label(root, text='', width=6, height=3, font=('Helvetica', 20), borderwidth=2, relief="solid")
                   for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                labels[i][j].grid(row=i, column=j)

    # Update the GUI for the first time
    update_gui(board, labels)

    # Bind arrow keys to movement
    root.bind('<Up>', lambda event: key_event(event, board, labels, root, game_continued))
    root.bind('<Left>', lambda event: key_event(event, board, labels, root, game_continued))
    root.bind('<Down>', lambda event: key_event(event, board, labels, root, game_continued))
    root.bind('<Right>', lambda event: key_event(event, board, labels, root, game_continued))

    root.mainloop()

# Play the game
play_game_gui()