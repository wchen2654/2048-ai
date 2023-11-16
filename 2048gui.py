import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4
TILE_SIZE = 100
MARGIN = 10
WIDTH = GRID_SIZE * (TILE_SIZE + MARGIN) + MARGIN
HEIGHT = WIDTH

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
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
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
      
def is_valid_move(original_board, new_board):
  return original_board != new_board
  
# Function to move tiles to the left
def move_left(board, score):
  original_board = [row[:] for row in board]  # Create a copy of the original board
  moved = False
  for row in range(GRID_SIZE):
    merged_row, row_score, row_moved = merge_tiles(board[row])
    if row_moved:
        moved = True
    board[row] = merged_row
    score += row_score
  if moved and is_valid_move(original_board, board):
    add_new_tile(board)
  return score

# Function to move tiles to the right
def move_right(board, score):
  original_board = [row[:] for row in board]
  moved = False
  for row in range(GRID_SIZE):
    merged_row, row_score, row_moved = merge_tiles(board[row][::-1])
    if row_moved:
        moved = True
    board[row] = merged_row[::-1]
    score += row_score
  if moved and is_valid_move(original_board, board):
    add_new_tile(board)
  return score

# Function to move tiles up
def move_up(board, score):
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
  if moved and is_valid_move(original_board, board):
    add_new_tile(board)
  return score

# Function to move tiles down
def move_down(board, score):
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
  if moved and is_valid_move(original_board, board):
    add_new_tile(board)
  return score

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

# Initialize the game board and score
board = initialize_board()
score = 0

# Set up the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                score = move_left(board, score)
            elif event.key == pygame.K_RIGHT:
                score = move_right(board, score)
            elif event.key == pygame.K_UP:
                score = move_up(board, score)
            elif event.key == pygame.K_DOWN:
                score = move_down(board, score)

    update_display(board, score)
