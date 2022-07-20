#!/usr/bin/python
# -*- coding: utf-8 -*-

# The next bit is needed for the AI, it will refer to the tables. These values can be changed to choice.

import random

pieceScores = {"R": 5.63, "N": 4.16, "B": 4.14, "Q": 9.5, "K": 0, "P": 0.9}

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

kingScores = [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 5, 0, 0, 5, 0, 5, 0]]

whitePawnScores = [[9, 9, 9, 9, 9, 9, 9, 9],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [9, 9, 9, 9, 9, 9, 9, 9]]

piecePositionScores = {"R": rookScores,
                       "N": knightScores,
                       "B": bishopScores,
                       "Q": queenScores,
                       "K": kingScores,
                       "wP": whitePawnScores,
                       "bP": blackPawnScores}

CHECKMATE = 10000
STALEMATE = 0
DEPTH = 4


# End of tables

# Start of move finder. It will draw the board from ChessMain to be able to determine its calculations.

def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


# def findBestMove(gs, valid_moves):
#   turnMultiplier = 1 if gs.whiteToMove else -1
#   opponentMinMaxScore = CHECKMATE
#   bestPlayerMove = None
#   random.shuffle(valid_moves)
#   for playerMove in valid_moves:
#       gs.makeMove(playerMove)
#       opponentsMoves = gs.getValidMoves
#       if gs.staleMate:
#           opponentMaxScore = STALEMATE
#       elif gs.checkMate:
#           opponentMaxScore = -CHECKMATE
#       else:
#           opponentMaxScore = -CHECKMATE
#           for opponentsMove in opponentsMoves:
#               gs.makeMove(opponentsMove)
#               gs.getValidMoves()
#               if gs.checkMate:
#                   score = CHECKMATE
#               elif gs.staleMate:
#                   score = STALEMATE
#               else:
#                   score = -turnMultiplier*scoreMaterial(gs.board)
#               if score > opponentMaxScore:
#                   opponentMaxScore = score
#               gs.undoMove()
#       if opponentMaxScore < opponentMinMaxScore:
#           opponentMinMaxScore = opponentMaxScore
#           bestPlayerMove = playerMove
#       gs.undoMove()
#   return bestPlayerMove

def findBestMove(gs, ValidMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    random.shuffle(ValidMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, ValidMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    returnQueue.put(nextMove)


# def findMoveMinMax(gs, valid_moves, depth, whiteToMove):
#   global nextMove
#   if depth == 0:
#       return scoreMaterial(gs.board)

#   if whiteToMove:
#       maxScore = -CHECKMATE
#       for move in valid_moves:
#           gs.makeMove(move)
#           nextMoves = gs.getValidMoves()
#           score = findMoveMinMax(gs, nextMoves, depth-1, False)
#           if score > maxScore:
#               maxScore = score
#               if depth == DEPTH:
#                   nextMove = move
#           gs.undoMove()
#       return maxScore

#   else:
#       minScore = CHECKMATE
#       for move in valid_moves:
#           gs.makeMove(move)
#           nextMoves = gs.getValidMoves()
#           score = findMoveMinMax(gs, nextMoves, depth-1, False)
#           if score < minScore:
#               minScore = score
#               if depth == DEPTH:
#                   nextMove = move
#           gs.undoMove()
#       return minScore


# def findMoveNegaMax(gs, valid_moves, depth, turnMultiplier):
#    global nextMove
#   if depth == 0:
#        return turnMultiplier*scoreBoard(gs)

#    maxScore = -CHECKMATE
#    for move in valid_moves:
#        gs.makeMove(move)
#        nextMoves = gs.getValidMoves()
#        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
#        if score > maxScore:
#            maxScore = score
#            if depth == DEPTH:
#                nextMove = move
#       gs.undoMove()
#    return maxScore


def findMoveNegaMaxAlphaBeta(gs, ValidMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in ValidMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


# End of move finder

# Here the scoreboard will be drawn to determine what decisions to make. See values in run-box.

def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                piecePositionScore = 0
                if square[1] == 'P':
                    if square[1] == 'P':
                        piecePositionScore = \
                            piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = \
                            piecePositionScores[square[1]][row][col]

                if square[0] == 'w':
                    score += pieceScores[square[1]] \
                             + piecePositionScore * .15
                elif square[0] == 'b':
                    score -= pieceScores[square[1]] \
                             + piecePositionScore * .15

    return score


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScores[square[1]]
            elif square[0] == "b":
                score -= pieceScores[square[1]]

    return score

# End of scoreboard
