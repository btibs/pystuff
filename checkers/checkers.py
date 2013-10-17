# SOLUTION

# Sketch outline for a checkers program
# Do NOT modify existing function calls
# You may create new private functions as necessary
# Fill in any sections currently marked with "pass"

import sys

# string representations for each color type
COLORS = {0: ('o', 'O'), 1: ('x', 'X')}

class Board:
    '''Initialize a blank Board.'''
    def __init__(self):
        # set up an 8x8 board
        self.grid = []
        for i in range(8):
            self.grid.append([None]*8)
        
        # place starting pieces
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.isValidPosition((i,j)):
                    if i < 3: # player 1
                        self.grid[i][j] = Checker(0)
                    elif i >= 5: # player 2
                        self.grid[i][j] = Checker(1)
    
    '''Return a string representation of the Board.'''
    def __str__(self):
        s = "-------------------\n"
        for i in range(len(self.grid)):
            s += "| "
            for j in range(len(self.grid[i])):
                if self.grid[i][j] is not None:
                    s += str(self.grid[i][j]) + " "
                elif self.isValidPosition((i,j)):
                    s += ". "
                else:
                    s += "  "
            s += "|\n"
        s += "-------------------"
        return s
    
    '''Return a boolean indicating if the game is over or not'''
    def gameOver(self):
        counts = {0:0, 1:0}
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] is not None:
                    counts[self.grid[i][j].color] = 1
        return sum(counts.values()) == 1
    
    '''Return a boolean indicating if moving the piece from (x1,y1) to (x2,y2) is a valid move, and if valid, execute the move.'''
    def executeMove(self, coord1, coord2):
        (x1,y1) = coord1
        (x2,y2) = coord2
        
        piece = self.grid[x1][y1]
        if piece is None:
            print("Nothing at initial position")
            return False
        
        if not self.isValidPosition(coord1) or not self.isValidPosition(coord2):
            print("Invalid position selected")
            return False
        
        # check if final position is occupied
        if self.grid[x2][y2] is not None:
            print("Final position is occupied")
            return False
        
        # okay, both spots are potential positions, now we have to check if the path works
        # FIRST DRAFT no multiple jumps ewww
        
        # first, check it's in a valid direction if it's not a king
        if (piece.color == 0 and not piece.king and x1 < x2) or (piece.color == 1 and not piece.king and x1 > x2) or piece.king:
            if abs(x1-x2)==1 and abs(y1-y2)==1:
                #(x1-1 == x2 and y1-1 == x2) or (x1+1 == x2 and y1-1 == y2) or (x1-1 == x2 and y1+1 == y2) or (x1+1 == x2 and y1+1 == y2):
                # simple diagonal move, no capture
                # move the piece
                print("simple diagonal, okay")
                self.grid[x2][y2] = self.grid[x1][y1]
                self.grid[x1][y1] = None
                if x2 == 0 or x2 == 7:
                    piece.king = True
                return True
            elif abs(x1-x2)==2 and abs(y1-y2)==2:
                #(x1-2 == x2 and y1-2 == x2) or (x1+2 == x2 and y1-2 == y2) or (x1-2 == x2 and y1+2 == y2) or (x1+2 == x2 and y1+2 == y2):
                # okay move if they are capturing a piece
                enemyx = (x1-x2)//2 + x2
                enemyy = (y1-y2)//2 + y2
                print ("you are trying to capture HUH???? better be a dude at (%s, %s)" % (enemyx, enemyy))
                enemypiece = self.grid[enemyx][enemyy] # I THINK THIS IS RIGHT?
                if enemypiece is not None: # sure we can jump over our own!! why not!!!
                    print("okay cool")
                    if enemypiece.color != piece.color: # bad guy SLURRRPPP
                        print("SLURRRPPPPP")
                        self.grid[enemyx][enemyy] = None
                    else:
                        print("just passing through don't mind me")
                        
                    # move the piece
                    self.grid[x2][y2] = self.grid[x1][y1]
                    self.grid[x1][y1] = None
                    if x2 == 0 or x2 == 7:
                        piece.king = True
                    return True
                else:
                    print("NOT TODAY PUNK")
                    return False
        
        print("not the right direction / not a king")
        return False
    
    '''util'''
    def isValidPosition(self, pos):
        (i,j) = pos
        if i < 0 or i >= 8 or j < 0 or j >= 8:
            return False
        return (j%2 == i%2)
        
class Checker:
    '''Initialize a checker piece'''
    def __init__(self, color):
        self.king = False
        self.color = color
    
    '''Return a string representation of the piece.'''
    def __str__(self):
        return COLORS[self.color][self.king]

'''Play the game (command-line)'''
if __name__ == "__main__":
    print("Welcome to Checkers")
    board = Board()
    print(board)
    
    turn = 0
    while not board.gameOver():
        print("\nPlayer %s's move!" % (turn+1))
        
        (x,y) = (None, None)
        while x is None or y is None:
            move = input("Type 'x,y' to select a piece to move, or 'q' to quit: ").lower()
            if move == 'q':
                print("\nGoodbye!")
                sys.exit(0)
            else:
                try:
                    (x,y) = [int(n) for n in move.split(",")]
                    # check if valid spot for this player
                    if board.grid[x][y] is None:
                        print("Empty square!")
                        (x,y) = (None, None)
                    elif board.grid[x][y].color != turn:
                        print("Wrong team!")
                        (x,y) = (None, None)
                except (ValueError, IndexError) as e:
                    print("Invalid location!")
                    (x,y) = (None, None)
        
        # okay, we have a valid piece selected, now figure out where to move it
        # TODO: cancel move
        moved = False
        while not moved:
            move = input("Where to move the piece at (%s, %s)? " % (x,y))
            try:
                (x2,y2) = [int(n) for n in move.split(",")]
                # empty spot - okay, now is it reachable from the first spot?
                if board.executeMove((x,y),(x2,y2)):
                    print("Moved!")
                    moved = True
                else:
                    print("Invalid move!")
            except (ValueError, IndexError) as e:
                print("Invalid location!")
        
        print(board)
        turn = (turn+1)%2
    
    print("Game over!")
