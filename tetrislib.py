#!/usr/bin/env python
import os
import sys
from subprocess import Popen, PIPE

# The board is represented as an array of arrays, with 10 rows and 10 columns.
boardsize = { 'x': 10, 'y': 10 }
board = []

# You can use these to define some shapes, or feel free to use your own shape data model.
SQUARE = \
  [[1, 1],
   [1, 1]]

L = \
  [[1, 1, 1],
   [0, 0, 1]]

L_90 = \
  [[0, 1],
   [0, 1],
   [1, 1]]

L_180 = \
  [[1, 0, 0],
   [1, 1, 1]]

L_270 = \
  [[1, 1],
   [1, 0],
   [1, 0]]

REVERSE_L = \
  [[0, 0, 1],
   [1, 1, 1]]

REVERSE_L_90 = \
  [[1, 0],
   [1, 0],
   [1, 1]]

REVERSE_L_180 = \
  [[1, 1, 1],
   [1, 0, 0]]

REVERSE_L_270 = \
  [[1, 1],
   [0, 1],
   [0, 1]]

T = \
  [[0, 1, 0],
   [1, 1, 1],
   [0, 0, 0]]

T_90 = \
  [[1, 0],
   [1, 1],
   [1, 0]]

T_180 = \
  [[1, 1, 1],
   [0, 1, 0]]

T_270 = \
  [[0, 1],
   [1, 1],
   [0, 1]]

Z = \
  [[1, 1, 0],
   [0, 1, 1]]

Z_90 = \
  [[0, 1],
   [1, 1],
   [1, 0]]

REVERSE_Z = \
  [[0, 1, 1],
   [1, 1, 0]]

REVERSE_Z_90 = \
  [[1, 0],
   [1, 1],
   [0, 1]]

VERTICAL = \
  [[1, 1, 1, 1]]

VERTICAL_90 = \
  [[1],
   [1],
   [1],
   [1]]

PIECE_TYPES = ['SQUARE', 'L', 'REVERSE_L', 'T', 'Z', 'REVERSE_Z', 'VERTICAL']

SQUARE_PIECES = [SQUARE]
L_PIECES = [L, L_90, L_180, L_270]
REVERSE_L_PIECES = [REVERSE_L, REVERSE_L_90, REVERSE_L_180, REVERSE_L_270]
T_PIECES = [T, T_90, T_180, T_270]
Z_PIECES = [Z, Z_90]
REVERSE_Z_PIECES = [REVERSE_Z, REVERSE_Z_90]
VERTICAL_PIECES = [VERTICAL, VERTICAL_90]

# Setup the board.
for i in range(0, boardsize['y']):
  board.append([0 for i in range(0, boardsize['x'])])

# Draws the contents of the board with a border around it.
def drawboard():
  boardborder = ''.join(['*' for i in range(0, boardsize['x'] + 2)])
  print boardborder
  for y in range(0, boardsize['y']):

    line = '|'
    for x in range(0, boardsize['x']):
      line += ('#' if board[y][x] == 1 else ' ')
    line += '|'
    print line
  print boardborder

# Waits for a single character of input and returns the string 'left', 'down', 'right', 'up', 'space' or None.
def getinput():
  original_terminal_state = None

  try:
    original_terminal_state = Popen('stty -g', stdout=PIPE, shell=True).communicate()[0]
    # Put the terminal in raw mode so we can capture one keypress at a time instead of waiting for enter.
    os.system('stty raw -echo')
    input = sys.stdin.read(1)

    # The arrow keys are read from stdin as an escaped sequence of 3 bytes.
    escape_sequence = '\x1b'
    ctrl_c = '\003'
    if input == escape_sequence:
      # The next two bytes will indicate which arrow keyw as pressed.
      character = sys.stdin.read(2)
      arrow_character_codes = dict(D='left', B='down', C='right', A='up')
      return arrow_character_codes.get(character[1], None)
    elif input == ' ':
      return 'space'
    elif input == ctrl_c:
      sys.exit()
  finally:
    os.system('stty ' + original_terminal_state)
  
  return None
