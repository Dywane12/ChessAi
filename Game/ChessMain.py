import pygame as p
import ChessEngine, AIEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
colors = [p.Color('white'), p.Color('gray')]

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ',]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    animate = False #flag for when we should animate a move
    loadImages() #only do this once, before the while loop
    running = True
    sqSelected = () #no square is selected, keep track of the last click of the used (tuple: (row, col))
    playerClicks = [] #keep track of player clicks (two tuples [(6, 4), (4, 4)]
    gameOver = False
    playerOne = True #if a human is playing white, then this will be True. If an AI is playing, then False
    playerTwo = True #same as above, but for black
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            #mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x, y) location of mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col): #the user clicked the same square twice
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: #after 2nd click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () #reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #key handlers
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z: #undo then 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if event.key == p.K_r: #reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        #AI move finder
        if not gameOver and not humanTurn:
            '''Random Move'''
            # AIMove = AIEngine.findRandomMove(validMoves)

            '''Greedy algorithm (one move ahead)'''
            # AIMove = AIEngine.bestGreedyMove(gs, validMoves)
            # if AIMove is None:
            #     AIMove = AIEngine.findRandomMove(validMoves)

            '''MinMax algorithm no recursion (two moves ahead)'''
            # AIMove = AIEngine.minMaxNoRecursion(gs, validMoves)
            # if AIMove is None:
            #     AIMove = AIEngine.findRandomMove(validMoves)

            '''MinMax algorithm with recursion'''
            # AIMove = AIEngine.findBestMoveMinMax(gs, validMoves)
            # if AIMove is None:
            #     AIMove = AIEngine.findRandomMove(validMoves)

            '''Nega Max algorithm without Alpha Beta Pruning'''
            # AIMove = AIEngine.findBestMoveNegaMax(gs, validMoves)
            # if AIMove is None:
            #     AIMove = AIEngine.findRandomMove(validMoves)

            '''Nega Max algorithm with Alpha Beta Pruning'''
            AIMove = AIEngine.findBestMoveNegaMaxAlphaBeta(gs, validMoves)
            if AIMove is None:
                AIMove = AIEngine.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate!')
            else:
                drawText(screen, 'White wins by checkmate!')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate!')
        clock.tick(MAX_FPS)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
            #highlight selected square
            surface = p.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(100) #transparency value -> 0 fully transpared; 255 solid
            surface.fill(p.Color('blue'))
            screen.blit(surface, (col*SQ_SIZE, row*SQ_SIZE))
            #highlight moves from that square
            surface.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(surface, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) #draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #draw pieces on top of those squares


def drawBoard(screen):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animateMove(move, screen, board, clock):
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move on square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        row, col = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto the rectangle
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw the moving piece
        if move.pieceMoved != '--':
            screen.blit(IMAGES[move.pieceMoved], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(240)


def drawText(screen, text):
    font = p.font.SysFont("Roboto", 40, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == '__main__':
    main()