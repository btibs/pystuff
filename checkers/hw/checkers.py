# Sketch outline for a checkers program
# Fill in any sections currently with "pass"
# Do NOT modify existing function signatures or data structures
# You may create new private functions as necessary (hint: it may be helpful to add an "isValidPosition" function)

import sys

# String representations for each 'color' team
COLORS = {0: ('o', 'O'), 1: ('x', 'X')}

'''Class to hold the checkers game'''
class Board:
    '''Set up a new game.'''
    def __init__(self):
        # create the grid
        # note for grid[x][y] 'x' is vertical (rows) and 'y' is horizontal (columns), origin at top left
        self.grid = []
        for i in range(8):
            self.grid.append([None]*8)
        
        # place starting pieces
        pass
    
    '''Return a string representation of the Board.
    
    Example (starting setup):
    -------------------
    | o   o   o   o   |
    |   o   o   o   o |
    | o   o   o   o   |
    |   .   .   .   . |
    | .   .   .   .   |
    |   x   x   x   x |
    | x   x   x   x   |
    |   x   x   x   x |
    ------------------- 
    '''
    def __str__(self):
        # use the __str__ method of the pieces; valid playing spaces otherwise unoccupied should be marked with '.'
        pass
        
    '''Return a boolean indicating if the game is over'''
    def gameOver(self):
        pass
    
    '''Execute a move from coord1=(x1,y1) to coord2=(x2,y2) if valid and return a boolean indicating if the piece was moved.'''
    def executeMove(self, coord1, coord2):
        # first draft: simple diagonal moves
        # second draft: simple single jumps
        # bonus round: multiple jumps (although this may be better handled elsewhere in the program! think about it..)
        pass
        

'''Class for a checker piece. Do not modify.'''
class Checker:
    '''Initialize a checker piece'''
    def __init__(self, color):
        self.king = False
        self.color = color
    
    '''Return a string representation of the piece.'''
    def __str__(self):
        return COLORS[self.color][self.king]


'''Play the game on the command-line.'''
# No modifications should be necessary, but feel free to edit if you want.
if __name__ == "__main__":
    print("Welcome to Checkers!")
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
        
        # Okay, we have a valid piece selected, now figure out where to move it
        moved = False
        while not moved:
            move = input("Where to move the piece at (%s, %s)? " % (x,y))
            try:
                (x2,y2) = [int(n) for n in move.split(",")]
                if board.executeMove((x,y),(x2,y2)):
                    print("Moved!")
                    moved = True
                else:
                    print("Invalid move!")
            except ValueError as e:
                print("Invalid location!")
        
        print(board)
        turn = (turn+1)%2
    
    print("Game over!")
