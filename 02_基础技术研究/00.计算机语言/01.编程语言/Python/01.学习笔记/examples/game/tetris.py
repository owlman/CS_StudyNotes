#! /usr/bin/env python
'''
    Created on 2017-10-18

    @author: lingjie
    @name : tetris
'''

import sys
import random
import time
import pygame

from pygame.locals import *

# RGB
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
LIGHT_RED = (175, 20, 20)
GREEN = (0, 155, 0)
LIGHT_GREEN = (20, 175, 20)
BLUE = (0, 0, 155)
LIGHT_BLUE = (20, 20, 175)
YELLOW = (155, 155, 0)
LIGHT_YELLOW = (175, 175, 20)

# UI settings
FPS = 25
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOX_SIZE = 20
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLANK = '.'

X_MARGIN = int((WINDOW_WIDTH - BOARD_WIDTH * BOX_SIZE) / 2)
TOP_MARGIN = int(WINDOW_HEIGHT - (BOARD_HEIGHT * BOX_SIZE) - 5)

MOVE_SIDEWAYS_FREQ = 0.15
MOVE_DOWN_FREQ = 0.1

# color settings
BORDER_COLOR = BLUE
BG_COLOR = BLACK
TEXT_COLOR = WHITE
TEXT_SHADOW_COLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW)
LIGHT_COLORS = (LIGHT_BLUE, LIGHT_GREEN, LIGHT_RED, LIGHT_YELLOW)

# each color must have light color
assert len(COLORS) == len(LIGHT_COLORS)

TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False  # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while(True):  # game loop
        if(fallingPiece is None):
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()  # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return  # can't fit a new piece on the board, so game over

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game
                    DISPLAY_SURF.fill(BG_COLOR)
                    # pygame.mixer.music.stop()
                    showTextScreen('Paused')  # pause until a key press
                    # pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a):
                    if isValidPosition(board, fallingPiece, adjX=-1):
                        fallingPiece['x'] -= 1
                        movingLeft = True
                        movingRight = False
                        lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d):
                    if isValidPosition(board, fallingPiece, adjX=1):
                        fallingPiece['x'] += 1
                        movingRight = True
                        movingLeft = False
                        lastMoveSidewaysTime = time.time()

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == K_q):  # rotate the other direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']]) 
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']]) 

                # making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARD_HEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVE_SIDEWAYS_FREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVE_DOWN_FREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        DISPLAY_SURF.fill(BG_COLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece is not None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type != KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIG_FONT, TEXT_SHADOW_COLOR)
    titleRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    DISPLAY_SURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIG_FONT, TEXT_COLOR)
    titleRect.center = (int(WINDOW_WIDTH / 2) - 3, int(WINDOW_HEIGHT / 2) - 3)
    DISPLAY_SURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs("Press a key to play.",
                                              BASIC_FONT, TEXT_COLOR)
    pressKeyRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + 100)
    DISPLAY_SURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() is None:
        pygame.display.update()
        FPS_CLOCK.tick()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq


def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARD_WIDTH / 2) - int(TEMPLATE_WIDTH / 2),
                'y': -2,  # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS) - 1)}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARD_WIDTH):
        board.append([BLANK] * BOARD_HEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARD_WIDTH and y < BOARD_HEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True


def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARD_WIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the
    # board, move everything above them
    # down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARD_HEIGHT - 1  # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARD_WIDTH):
                    board[x][pullDownY] = board[x][pullDownY - 1]
            # Set very top line to blank.
            for x in range(BOARD_WIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1  # move on to check next row up
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (X_MARGIN + (boxx * BOX_SIZE)), (TOP_MARGIN + (boxy * BOX_SIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    """
     draw a single box (each tetromino piece has four boxes)
     at xy coordinates on the board. Or, if pixelx & pixely
     are specified, draw to the pixel coordinates stored in
     pixelx & pixely (this is used for the "Next" piece).
    """
    if color == BLANK:
        return

    if pixelx is None and pixely is None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)

    pygame.draw.rect(DISPLAY_SURF, COLORS[color],
                     (pixelx + 1, pixely + 1, BOX_SIZE - 1, BOX_SIZE - 1))
    pygame.draw.rect(DISPLAY_SURF, LIGHT_COLORS[color],
                     (pixelx + 1, pixely + 1, BOX_SIZE - 4, BOX_SIZE - 4))


def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAY_SURF, BORDER_COLOR,
                     (X_MARGIN - 3, TOP_MARGIN - 7,
                      (BOARD_WIDTH * BOX_SIZE) + 8,
                      (BOARD_HEIGHT * BOX_SIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAY_SURF, BG_COLOR,
                     (X_MARGIN, TOP_MARGIN,
                      BOX_SIZE * BOARD_WIDTH,
                      BOX_SIZE * BOARD_HEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, level):
    # draw the score text
    scoreSurf = BASIC_FONT.render('Score: %s' % score, True, TEXT_COLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOW_WIDTH - 150, 20)
    DISPLAY_SURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASIC_FONT.render('Level: %s' % level, True, TEXT_COLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOW_WIDTH - 150, 50)
    DISPLAY_SURF.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx is None and pixely is None:
        # if pixelx & pixely hasn't been specified,
        # use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None,
                        piece['color'],
                        pixelx + (x * BOX_SIZE),
                        pixely + (y * BOX_SIZE))


def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASIC_FONT.render('Next:', True, TEXT_COLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOW_WIDTH - 120, 80)
    DISPLAY_SURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOW_WIDTH - 120, pixely=100)


def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT, BIG_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    BIG_FONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')

    # the main loop
    while True:
        runGame()
        showTextScreen('Game Over')


if __name__ == '__main__':
    main()
