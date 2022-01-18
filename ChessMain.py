#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as p
from multiprocessing import Process, Queue
from Chess import ChessEngine, SmartMoveFinder

BOARD_WIDTH = BOARD_HEIGHT = 900
MOVE_LOG_PANEL_WIDTH = 160
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 120
IMAGES = {}


# Audio part of the program

def StartSound():
    p.mixer.pre_init(frequency=96000, channels=2, buffer=1024)
    p.mixer.init()
    startSound = p.mixer.Sound("C:\\Users\\jools\\PycharmProjects\\Chess\\Chess\\Sounds\\start.mp3")
    if startSound.play(0) == True:
        startSound.play(0)
        print("May both players win")
    else:
        pass


def PieceMovedSound():
   p.mixer.pre_init(frequency=96000, channels=2, buffer=1024)
   p.mixer.init()
   pieceMovedSound = p.mixer.Sound("C:\\Users\\jools\\PycharmProjects\\Chess\\Chess\\Sounds\\pieceMoved.mp3")
   if pieceMovedSound.play(0) == True:
       pieceMovedSound.play(0)
       print("Seems like a good move! Or is it?")
   else:
       pass

#   def PieceCapturedSound():
#       p.mixer.pre_init(frequency=96000, channels=2, buffer=1024)
#       p.mixer.init()
#       pieceCapturedSound = p.mixer.Sound("C:\\Users\\jools\\PycharmProjects\\Chess\\Chess\\Sounds\\pieceCaptured.mp3")
#       if pieceCapturedSound.play(0) == True:
#           pieceCapturedSound.play(0)
#           print("It's just one piece, do not worry")
#       else:
#           pass


#   def InCheckSound():
#       p.mixer.pre_init(frequency=96000, channels=2, buffer=1024)
#       p.mixer.init()
#       inCheckSound = p.mixer.Sound("C:\\Users\\jools\\PycharmProjects\\Chess\\Chess\\Sounds\\inCheck.mp3")
#       if inCheckSound.play(0) == True:
#           inCheckSound.play(0)
#           print("That seems like a difficult situation")
#       else:
#           pass

def EndSound():
    p.mixer.pre_init(frequency=96000, channels=2, buffer=1024)
    p.mixer.init()
    endSound = p.mixer.Sound("C:\\Users\\jools\\PycharmProjects\\Chess\\Chess\\Sounds\\end.mp3")
    if endSound.play(0) == True:
        endSound.play(0)
        print("Thank you for playing")
    else:
        pass

# End of audio controls

# Loads in images under the name of the pieces

def loadImages():
    pieces = ["bB", "bK", "bN", "bP", "bQ", "bR", "wB", "wK", "wN", "wP", "wQ", "wR"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


#Start of controls

def main():
    global returnQueue
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 24, False, False)
    gs = ChessEngine.GameState()
    ValidMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    StartSound()
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True
    playerTwo = True
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col) or col >= 8:
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2 and humanTurn:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(ValidMoves)):
                            if move == ValidMoves[i]:
                                gs.makeMove(move)
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_u:
                    sqSelected = ()
                    playerClicks = []
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    ValidMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = ()
                    moveMade = False
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                print("Processing...")
                returnQueue = Queue()
                moveFinderProcess = Process(target=SmartMoveFinder.findBestMove, args=(gs, ValidMoves, returnQueue))
                moveFinderProcess.start()

            if not moveFinderProcess.is_alive():
                print("Done Processing")
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = SmartMoveFinder.findRandomMove(ValidMoves)
                gs.makeMove(AIMove)
                moveMade = True
                animate = True
                AIThinking = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
                PieceMovedSound()
            ValidMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            moveUndone = False

        drawGameState(screen, gs, ValidMoves, sqSelected, moveLogFont)

        if gs.checkMate or gs.staleMate:
            EndSound()
            gameOver = True
            drawEndGameText(screen,
                            "Engine wins by checkmate" if gs.staleMate else "Equal thinking, stalemate"
                            if gs.whiteToMove else "You win by checkmate")
        clock.tick(MAX_FPS)
        p.display.flip()

# End of controls

# GUI/UI controls

def drawGameState(screen, gs, ValidMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highLightSquares(screen, gs, ValidMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("purple")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highLightSquares(screen, gs, ValidMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(200)
            s.fill(p.Color("Grey"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color("Violet"))
            for move in ValidMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2+1) + "  " + str(moveLog[i]) + "  "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i + 1]) + "  "
        moveTexts.append(moveString)

    movesPerRow = 1
    padding = 5
    lineSpacing = 3
    textY = padding

    for i in range(0, len(moveTexts), movesPerRow):
        text = "--"
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]

        textObject = font.render(text, True, p.Color("White"))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 2
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "--":
            if move.enPassant:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == "b" else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        if move.pieceMoved != "--":
            screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        p.display.flip()
        clock.tick(60)


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 8, p.Color("Black"))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Gray"))
    screen.blit(textObject, textLocation.move(2, 2))

#End of UI/GUI controls

if __name__ == "__main__":
    main()
