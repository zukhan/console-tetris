#!/usr/bin/env python
from tetrislib import *
from threading import Thread
import time
import random

# keeps track of the coordinates for the current piece's 4 squares
pieceCoords = []

# start from the top (middle)
startPosition = (boardsize['x']/2 - 1, 0)
pieceX, pieceY = startPosition
rotationIndex = 0
score = 0

pieceArrLookup = {
  'SQUARE': SQUARE_PIECES,
  'L': L_PIECES,
  'REVERSE_L': REVERSE_L_PIECES,
  'T': T_PIECES,
  'Z': Z_PIECES,
  'REVERSE_Z': REVERSE_Z_PIECES,
  'VERTICAL': VERTICAL_PIECES
}


def setNextPiece():
  global curPiece, curPieceArr, rotationIndex
  pieceType = random.choice(PIECE_TYPES)
  curPieceArr = pieceArrLookup[pieceType]
  curPiece = curPieceArr[0]
  rotationIndex = 0


def inBounds(row, col):
  return col >= 0 and col < boardsize['y'] and row >= 0 and row < boardsize['x']


def rotatePiece():
  global curPiece, rotationIndex
  newRotationIndex = (rotationIndex + 1) % len(curPieceArr)
  newPiece = curPieceArr[newRotationIndex]

  if shouldAllowRotation(newPiece):
    curPiece = newPiece
    rotationIndex = newRotationIndex


def shouldAllowRotation(newPiece):
  for r in xrange(len(newPiece)):
    for c in xrange(len(newPiece[0])):
      if newPiece[r][c] == 1:
        row = r + pieceY
        col = c + pieceX

        # prevent rotation is there's a collision
        if not inBounds(row, col) or (board[row][col] == 1 and (row, col) not in pieceCoords):
          return False
  return True


def setPieceOnBoard():
  for r in xrange(len(curPiece)):
    for c in xrange(len(curPiece[0])):
      if curPiece[r][c] == 1:
        curRow = r + pieceY
        curCol = c + pieceX

        # exit the program if you've reached the top
        if board[curRow][curCol] == 1:
          raise SystemExit

        board[curRow][curCol] = 1
        pieceCoords.append((curRow,curCol))


#
# Removes the previous piece from the board when you move
#
def clearPrevPiece():
  global pieceCoords
  for pieceCoord in pieceCoords:
    r, c = pieceCoord
    board[r][c] = 0
  pieceCoords = []


def redraw():
  setPieceOnBoard()
  print "Score: " + str(score)
  print
  drawboard()


def processInput(key):
  global pieceX, pieceY
  if key == 'left' and canMoveHorizontally('left'):
    pieceX -= 1
  elif key == 'right' and canMoveHorizontally('right'):
    pieceX += 1
  elif key == 'down':
    if shouldAnchor():
      anchor()
    else:
      pieceY += 1
  elif key == 'up':
    rotatePiece()
  elif key == 'space':
    while not shouldAnchor():
      pieceY += 1
      clearPrevPiece()
      redraw()
    anchor()

  clearPrevPiece()
  clearScreen()
  redraw()


def canMoveHorizontally(direction):
  for pieceCoord in pieceCoords:
    row, col = pieceCoord

    isInbound = inBounds(row, col-1)
    partOfCurrPiece = (row, col-1) in pieceCoords
    nextSquareFilled = isInbound and board[row][col-1] == 1
    leftCollision = (not isInbound or nextSquareFilled) and not partOfCurrPiece

    isInbound = inBounds(row, col+1)
    partOfCurrPiece = (row, col+1) in pieceCoords
    nextSquareFilled = isInbound and board[row][col+1] == 1
    rightCollision = (not isInbound or nextSquareFilled) and not partOfCurrPiece

    if (direction == 'right' and rightCollision) \
        or (direction == 'left' and leftCollision):
      return False
  return True


#
# Achors the piece and starts a new piece on the board
#
def anchor():
  global pieceX, pieceY, pieceCoords

  clearFilledLines()
  setNextPiece()
  pieceCoords = []
  pieceX, pieceY = startPosition
  redraw()


#
# Determines whether we've reached the bottom (will be colliding below)
#
def shouldAnchor():
  for pieceCoord in pieceCoords:
    row, col = pieceCoord
    collisionBelow = not inBounds(row+1, col) or board[row+1][col] == 1
    partOfCurrPiece = (row+1, col) in pieceCoords

    if collisionBelow and not partOfCurrPiece:
      return True
  return False


def clearFilledLines():
  global score

  row = len(board)-1
  while row > 0:
    while all(val is 1 for val in board[row]):
      # move rows down
      for r in xrange(row, 0, -1):
        for c in xrange(len(board[0])):
          board[r][c] = board[r-1][c]

      # empty out the first row
      for c in xrange(len(board[0])):
        board[0][c] = 0

      score += 50
    row -= 1


def clearScreen():
  os.system('clear')


def listenForInput():
  while True:
    # getinput() returns one of 'left', 'up', 'right', 'down', 'space'.
    key = getinput()
    if not key:
      break

    t = Thread(target=processInput, args = (key,))
    t.start()


setNextPiece()

t = Thread(target=listenForInput, args = ())
t.start()

clearScreen()
redraw()
