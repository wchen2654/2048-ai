import random
import time
import copy
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4
TILE_SIZE = 100
MARGIN = 10
WIDTH = GRID_SIZE * (TILE_SIZE + MARGIN) + MARGIN
HEIGHT = WIDTH

# Globals
# The score is the sum of all the tiles
score = 0
# The number of moves made
moves = 0
# The number of times the board has been updated
updates = 0


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
TILE_COLORS = {
    2: (238, 228, 218),  # Light yellow
    4: (237, 224, 200),  # Light tan
    8: (242, 177, 121),  # Light orange
    16: (245, 149, 99),  # Orange
    32: (246, 124, 95),  # Salmon
    64: (246, 94, 59),   # Light coral
    128: (237, 207, 114),  # Light khaki
    256: (237, 204, 97),   # Yellow
    512: (237, 200, 80),   # Light yellow
    1024: (237, 197, 63),  # Dark yellow
    2048: (237, 194, 46),  # Darker yellow
}

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

def print_stats():
    print("Score:", score, "Moves:", moves, "Updates:", updates, "Empty:", empty_tiles())

# Function to draw the grid
def draw_grid(board, score):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(
                screen,
                TILE_COLORS.get(board[row][col], WHITE),
                [
                    MARGIN + col * (TILE_SIZE + MARGIN),
                    MARGIN + row * (TILE_SIZE + MARGIN),
                    TILE_SIZE,
                    TILE_SIZE,
                ],
            )
            value = board[row][col]
            if value != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(
                    center=(
                        col * (TILE_SIZE + MARGIN) + TILE_SIZE / 2,
                        row * (TILE_SIZE + MARGIN) + TILE_SIZE / 2,
                    )
                )
                screen.blit(text, text_rect)

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, HEIGHT - 40))

# Function to update the display
def update_display(board, score):
    screen.fill(GRAY)
    draw_grid(board, score)
    pygame.display.flip()

# Function to initialize the game board with two random tiles
def initialize_board():
    global board, score, moves, updates
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    score = 0
    moves = 0
    updates = 0
    add_new_tile(board)
    add_new_tile(board)
    return board

# Function to add a new tile (either 2 or 4) to a random empty spot on the board
def add_new_tile(board):
    empty_spots = [
        (row, col)
        for row in range(GRID_SIZE)
        for col in range(GRID_SIZE)
        if board[row][col] == 0
    ]
    if empty_spots:
        row, col = random.choice(empty_spots)
        board[row][col] = random.choice([2, 4])

# Function to merge adjacent tiles with the same value
def merge_tiles(row):
    new_row = [0] * GRID_SIZE
    index = 0
    score = 0
    moved = False
    for value in row:
        if value != 0:
            if new_row[index] == 0:
                new_row[index] = value
                moved = True
            elif new_row[index] == value:
                new_row[index] *= 2
                score += new_row[index]
                index += 1
                moved = True
            else:
                index += 1
                new_row[index] = value
                if index != 0:
                    moved = True
    return new_row, score, moved

def is_valid_move(original_board, new_board):
  return original_board != new_board

# Function to move tiles to the left
def move_left(board, score, test):
    original_board = [row[:] for row in board]  # Create a copy of the original board
    moved = False
    for row in range(GRID_SIZE):
        merged_row, row_score, row_moved = merge_tiles(board[row])
        if row_moved:
            moved = True
        board[row] = merged_row
        score += row_score
    if not test and moved and is_valid_move(original_board, board):
        add_new_tile(board)
    if test:
        return 0
    else:
        return score

# Function to move tiles to the right
def move_right(board, score, test):
    original_board = [row[:] for row in board]
    moved = False
    for row in range(GRID_SIZE):
        merged_row, row_score, row_moved = merge_tiles(board[row][::-1])
        if row_moved:
            moved = True
        board[row] = merged_row[::-1]
        score += row_score
    if not test and moved and is_valid_move(original_board, board):
        add_new_tile(board)
    if test:
        return 0
    else:
        return score

# Function to move tiles up
def move_up(board, score, test):
    original_board = [row[:] for row in board]
    moved = False
    for col in range(GRID_SIZE):
        column = [board[row][col] for row in range(GRID_SIZE)]
        merged_column, col_score, col_moved = merge_tiles(column)
        if col_moved:
            moved = True
        for row in range(GRID_SIZE):
            board[row][col] = merged_column[row]
        score += col_score
    if not test and moved and is_valid_move(original_board, board):
        add_new_tile(board)
    if test:
        return 0
    else:
        return score

# Function to move tiles down
def move_down(board, score, test):
    original_board = [row[:] for row in board]
    moved = False
    for col in range(GRID_SIZE):
        column = [board[row][col] for row in range(GRID_SIZE)]
        reversed_column = column[::-1]
        merged_column, col_score, col_moved = merge_tiles(reversed_column)
        if col_moved:
            moved = True
        reversed_column = merged_column[::-1]
        for row in range(GRID_SIZE):
            board[row][col] = reversed_column[row]
        score += col_score
    if not test and moved and is_valid_move(original_board, board):
        add_new_tile(board)
    if test:
        return 0
    else:
        return score


# This function will execute the move in the specified direction
def execute_move(direction, board, test = False):
    global score, moves, updates
    if direction == 'up':
        score = move_up(board, score, test)
    elif direction == 'down':
        score = move_down(board, score, test)
    elif direction == 'left':
        score = move_left(board, score, test)
    elif direction == 'right':
        score = move_right(board, score, test)

# Find the best move using the Expectimax algorithm
def find_best_move(board):
    best_direction = None
    best_score = float('-inf')
    for direction in ['up', 'down', 'left', 'right']:
        new_board = copy.deepcopy(board)
        execute_move(direction, new_board, True)  # Pass new_board to execute_move
        if new_board != board:
            move_score = expectimax(new_board, 3, False)
            if move_score > best_score:
                best_score = move_score
                best_direction = direction
    return best_direction

def expectimax(board, depth, maximizing_player):
    if depth == 0:
        return heuristic(board)

    if maximizing_player:
        max_eval = float('-inf')
        for direction in ['up', 'down', 'left', 'right']:
            new_board = copy.deepcopy(board)
            execute_move(direction, new_board, True)  # Pass new_board to execute_move
            if new_board != board:
                eval = expectimax(new_board, depth - 1, False)
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        empty_tiles_coord = empty_tiles_coordinates(board)  # Pass the board to empty_tiles_coordinates
        if len(empty_tiles_coord) == 0:
            return 0

        total_eval = 0
        for i, j in empty_tiles_coord:
            new_board_2 = copy.deepcopy(board)
            new_board_4 = copy.deepcopy(board)

            new_board_2[i][j] = 2
            eval_2 = expectimax(new_board_2, depth - 1, True)
            total_eval += 0.9 * eval_2

            new_board_4[i][j] = 4
            eval_4 = expectimax(new_board_4, depth - 1, True)
            total_eval += 0.1 * eval_4

        return total_eval / len(empty_tiles_coord)

# Define a simple heuristic
def heuristic(board):
    empty_tiles_count = empty_tiles()
    max_tile_value = max(max(row) for row in board)
    smoothness = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                for direction in [(0, 1), (1, 0)]:
                    di, dj = direction
                    new_i, new_j = i + di, j + dj
                    if 0 <= new_i < 4 and 0 <= new_j < 4 and board[new_i][new_j] != 0:
                        smoothness -= abs(board[i][j] - board[new_i][new_j])
    return empty_tiles_count * 100 + max_tile_value * 100 + smoothness

# This function will return the number of empty tiles
def empty_tiles():
    empty = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty += 1
    return empty

# This function will check if the game is over
def game_over():
    if empty_tiles() == 0:
        for i in range(4):
            for j in range(4):
                if j < 3 and (board[i][j] == board[i][j + 1]):
                    return False
                if i < 3 and (board[i][j] == board[i + 1][j]):
                    return False
        return True
    else:
        return False

# This function will return the coordinates of the empty tiles
def empty_tiles_coordinates(board):
    empty_coordinates = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty_coordinates.append((i, j))
    return empty_coordinates



# Initialize the game board and score
board = initialize_board()
score = 0

# Set up the game loop
while not game_over():
    print_stats()
    time.sleep(0.01)  # Add a delay to see the moves

    ai_direction = find_best_move(copy.deepcopy(board))  # Pass a copy of board
    if ai_direction:
        print(f"AI chooses {ai_direction} move")
        execute_move(ai_direction, board)  # Pass the original board to execute_move
        moves += 1
        updates += 1
    else:
        print("No valid move found for the AI!")
        break
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    update_display(board, score)