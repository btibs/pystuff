# checkers GUI

from checkers import Board

import sys
import pygame

size = width, height = 496,496
dx,dy = width/8, height/8
black = 0,0,0
white = 255,255,255
green = 0, 255, 0
dkgreen = 0, 55, 0

COLORS = {0:((255,0,0), (155,0,0)), 1:((0,0,255), (0,0,155))}

def drawBoard(screen, team, board, selected):
    # draw just the checkerboard
    screen.fill(white)
    i=0
    for x in range(0, width, dx):
        j=0
        for y in range(0, height, dy):
            if (i%2==j%2):
                screen.fill(black, (x, y, dx, dy))
            j += 1
        i += 1
    
    # draw the turn indicators
    xturn1 = width if team else 0
    xturn2 = 0 if team else width
    pygame.draw.circle(screen, green, (xturn1, height/2), dx/5)
    pygame.draw.circle(screen, dkgreen, (xturn2, height/2), dx/5)

    # now draw the checkers on the board
    x = 0
    for i in range(len(board.grid)):
        y = 0
        for j in range(len(board.grid[i])):
            if board.grid[i][j] is not None:
                piece = board.grid[i][j]
                pos = (x + dx/2, y + dy/2)
                color = COLORS[piece.color][(i,j) == selected]
                cw = dx/5 if piece.king else 0
                pygame.draw.circle(screen, color, pos, dx/3, cw)
            y += dy
        x += dx

def runGame():
    pygame.init()
    screen = pygame.display.set_mode(size)
    board = Board()

    selected = None
    team = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.dict['pos']
                
                # convert to i,j
                i,j = pos[0]//dx, pos[1]//dy
                
                # check if this matches an actual piece
                if board.grid[i][j] is not None and board.grid[i][j].color == team:
                    selected = (i,j)
                    
            elif event.type == pygame.MOUSEBUTTONUP and selected is not None:
                pos = event.dict['pos']
                
                # convert to i,j
                i,j = pos[0]//dx, pos[1]//dy
                if board.executeMove(selected, (i,j)):
                    team = not team
                selected = None
            
            drawBoard(screen, team, board, selected)
            pygame.display.flip()

if __name__ == "__main__":
    runGame()