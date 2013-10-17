# Sudoku solver
# Beth McNany

'''
Currently: solves up to "hard" puzzles
fails on "evil"

which means that it can solve with pure elimination just fine
but cannot solve when it ends up with pairs...
probably need an ai-like cascading check-what-happens-when you pick one in a pair
'''

from optparse import OptionParser
import sys
import time

'''Class for a cell in the sudoku puzzle'''
class Cell:
    '''Initialize cell'''
    def __init__(self, value, x, y):
        [self.x, self.y] = [x,y]
        if value and value != ' ' and int(value) in range(1, 10):
                self.assigned = True
                self.possible = [int(value)]
        else:
            #print "'%s' is not a valid value" % value
            self.assigned = False # Does the object have a specific value associated with it?
            self.possible = range(1, 10) # Possible numbers for the cell
            
    '''Print value'''
    def __str__(self):
        if self.assigned: return str(self.possible[0])
        else: return "_"

    '''Eliminate possible values'''
    def eliminateValue(self, value):
        try:
            self.possible.remove(int(value))
            if len(self.possible) == 1:
                self.assignValue(self.possible[0])
                #print "elimination assigned %s at (%s,%s)" % (self.possible, self.x, self.y)
                #self.printPuzzle()
                
        except ValueError:
            # value was not in possibilities to begin with
            pass
            
    '''Assign value to a cell'''
    def assignValue(self, value):
        # TODO: input validation
        if not self.assigned:
            self.possible = [value]
            self.assigned = True
        else:
            #print "ASSIGNING: already assigned!!!"
            pass
        
'''Class to hold the sudoku-solving object'''
class SudokuSolver:
    '''Initialize'''
    def __init__(self, options):
        self.options = options
        self.options.iters = int(self.options.iters)
        self.solved = False
        if not self.options.file:
            print "No puzzle specified!"
            sys.exit()
        
        self.getPuzzle(self.options.file)
        
    '''Actually solve the puzzle'''
    def solve(self):
        tStart = time.time()
        solved = False
        for i in range(0, self.options.iters): # how many iterations to go
            if self.isSolved():
                solved = True
                break
            if self.options.verbose:    print "\n***   ITERATION %s   ***" % i
            self.checkBoxes()
            self.checkColumns()
            self.checkRows()
            #self.printPuzzle()
        tEnd = time.time()
        dt = (tEnd-tStart)*1000
        if self.isSolved():   solved = True
        return (solved, dt, i)
        
    '''Check if puzzle is solved'''
    def isSolved(self):
        # if all boxes are assigned
        for i in range(0, 9):
            for j in range(0, 9):
                if not self.puzzle[i][j].assigned: return False
        if self.options.verbose:    print "PUZZLE IS SOLVED WOO"
        return True
    
    '''Check boxes and eliminate possibilities'''
    def checkBoxes(self):
        needToRerun = True
        while (needToRerun):
            needToRerun = False # only run once unless you assign a new number in the box
            # arrays for each box
            boxes = []
            for i in range(0, 3):
                boxes.append([])
                for j in range(0, 3):
                    boxes[i].append([])
            
            for i in range(0, 9):
                for j in range(0, 9):
                    # get list of assigned numbers in each box
                    if self.puzzle[i][j].assigned:  boxes[i/3][j/3].append(self.puzzle[i][j].possible[0])
            
            # now eliminate possibilities based on assigned numbers
            for i in range(0, 9):
                for j in range(0, 9):
                    for n in boxes[i/3][j/3]:
                        # eliminate assigned from not assigned
                        if not self.puzzle[i][j].assigned:
                            self.puzzle[i][j].eliminateValue(n)
                            if self.puzzle[i][j].assigned:
                                if self.options.verbose:    print "assigned by boxes at %s, %s" % (i, j)
                                needToRerun = True
                                if self.options.verbose:    self.printPuzzle()
        # end while needToReRun
        
        # now assign numbers if only one spot where a number can go in a box
        # TODO - this doesn't currently work... ugh
        # only looping over once?
        
        #print "counting up!"
        
        # initialize
        boxes = []
        for b in range(0, 9):
            boxes.append([]) # array to hold j's
            for n in range(0, 9): # array to hold n's
                boxes[b].append([0, -1, -1]) # initialize
        
        # get list of assigned numbers for each box
        for i in range(0, 9):
            for j in range(0, 9):
                (ib, jb) = (i/3, j/3)
                boxnum = 3*ib + jb
                #print "checking %s,%s = box %s,%s = boxnum %x" % (i,j,ib,jb,boxnum)
                if not self.puzzle[i][j].assigned:
                    for n in self.puzzle[i][j].possible:
                        #print "%s possible at %s,%s for total of %s (box %s)" % (n,i,j,boxes[boxnum][n-1][0]+1,boxnum)
                        boxes[boxnum][n-1][0] += 1 # increase count
                        boxes[boxnum][n-1][1:] = [i,j]
                #print "finished checking"
        
        # print out info
        if self.options.verbose:
            print "\nBOXES: "
            for i in range(0,9):
                print "Box %s: " % i
                for n in range(0,9):
                    print "%s x %s, last one at %s,%s" %(n+1, boxes[i][n][0], boxes[i][n][1], boxes[i][n][2])
            
        # this should have gotten all the info for the boxes, now assign if possible
        for box in boxes:
            for n in range(0, 9):
                if box[n][0] == 1:
                    [x,y] = box[n][1:]
                    if self.options.verbose:    print "ASSIGNING "+str(n+1)+" at "+str(y)+","+str(x)+" for boxes"
                    self.puzzle[x][y].assignValue(n+1)
                    if self.options.verbose:    self.printPuzzle()
        
    '''Check columns and eliminate possibilities'''
    def checkColumns(self):
        needToRerun = True
        while (needToRerun):
            needToRerun = False # only run once unless you assign a new number in the column
            for j in range(0, 9):
                nums_in_row = []
                for i in range(0, 9):
                    # get list of assigned numbers in this column
                    if self.puzzle[i][j].assigned:
                        nums_in_row.append(self.puzzle[i][j].possible[0])
                for i in range(0, 9):
                    for n in nums_in_row:
                        # eliminate assigned from not assigned
                        if not self.puzzle[i][j].assigned:
                            self.puzzle[i][j].eliminateValue(n)
                            if self.puzzle[i][j].assigned:
                                if self.options.verbose:    print "assigned by columns at %s, %s" % (i, j)
                                # update the nums assigned
                                nums_in_row.append(self.puzzle[i][j].possible[0])
                                needToRerun = True
                                if self.options.verbose:    self.printPuzzle()
        
        # now assign numbers if only one spot where a number can go
        # loop and count up numbers, record last index
        for j in range(0, 9):
            numarray = []   # array to hold the numbers in the column
            for i in range(0,9): numarray.append([0,-1,-1]) # initialize
            
            for i in range(0, 9):
                if not self.puzzle[i][j].assigned: # we already did those
                    for n in self.puzzle[i][j].possible:
                        numarray[n-1][0] += 1    # add to count
                        numarray[n-1][1:] = [i,j]    # record last index
        
            # ok, collected all the info, assign if possible
            for k in range(0,9):
                if numarray[k][0] == 1:
                    [x,y] = numarray[k][1:]
                    if self.options.verbose:    print "ASSIGNING "+str(k+1)+" at " + str(x) + ","+str(y) + " for columns"
                    self.puzzle[x][y].assignValue(k+1)
                    #self.puzzle[x][y].possible = [k+1]
                    #self.puzzle[x][y].assigned = True
                    if self.options.verbose:    self.printPuzzle()
                    
    '''Check rows and eliminate possibilities'''
    def checkRows(self):
        needToRerun = True
        while (needToRerun):
            needToRerun = False # only run once unless you assign a new number in the row
            for i in range(0, 9):
                nums_in_row = []
                for j in range(0, 9):
                    # get list of assigned numbers in this row
                    if self.puzzle[i][j].assigned:  nums_in_row.append(self.puzzle[i][j].possible[0])
                for j in range(0, 9):
                    for n in nums_in_row:
                        # eliminate assigned from not assigned
                        if not self.puzzle[i][j].assigned:
                            self.puzzle[i][j].eliminateValue(n)
                            if self.puzzle[i][j].assigned:
                                if self.options.verbose:    print "assigned by rows at %s, %s" % (j, i)
                                # update the nums assigned
                                nums_in_row.append(self.puzzle[i][j].possible[0])
                                # this needs re-run then
                                needToRerun = True
                                if self.options.verbose:    self.printPuzzle()

        # now assign numbers if only one spot where a number can go        
        # loop and count up numbers, record last index
        for i in range(0, 9):
            numarray = []   # array to hold numbers for row
            for k in range(0,9): numarray.append([0,-1,-1]) # initialize
            
            for j in range(0, 9):
                if not self.puzzle[i][j].assigned: # we already did those
                    for n in self.puzzle[i][j].possible:
                        numarray[n-1][0] += 1    # add to count
                        numarray[n-1][1:] = [i,j]    # record last index
        
            # ok, collected all the info, assign if possible
            #print numarray
            for k in range(0,9):
                if numarray[k][0] == 1:
                    [x,y] = numarray[k][1:]
                    if self.options.verbose:    print "ASSIGNING "+str(k+1)+" at " + str(x) + ","+str(y) + " for rows"
                    self.puzzle[x][y].assignValue(k+1)
                    #self.puzzle[x][y].possible = [k+1]
                    #self.puzzle[x][y].assigned = True
                    if self.options.verbose:    self.printPuzzle()
                        
    '''Load sudoku from file'''
    def getPuzzle(self, filename):
        if self.options.verbose:    print "Opening %s..." % filename
        try:
            pfile = file(filename, "r")
        except IOError:
            print "Error opening %s, exiting now" % filename
            sys.exit()
        
        #load puzzle
        self.puzzle = []
        j = 0;
        for line in pfile:
            temp = line.split(",")[:-1]
            if len(temp) != 9:
                print "Error loading puzzle: invalid number of columns"
                print line
                sys.exit()
            for i in range(0, 9):
                temp[i] = Cell(temp[i], i, j)
            self.puzzle.append(temp)
            j += 1
        if len(self.puzzle) != 9:
            print "Error loading puzzle: invalid number of rows"
            sys.exit()
    
    '''Print the puzzle in a pretty fashion'''
    def printPuzzle(self):
        print "\nPuzzle:"
        for i in range(0, 9):
            row = ""
            if i%3 == 0: row = " -----  -----  -----\n"
            row += "|"
            for j in range(0, 9):
                row += str(self.puzzle[i][j])
                if (j+1)%3 == 0:
                    row += "|"
                    if j != 8: row += "|"
                else: row += " "
            print row
        print " -----  -----  -----\n"
        
if __name__ == "__main__":
    optParser = OptionParser()
    optParser.add_option("-f", dest="file", help="Select a file (in csv format) containing puzzle", default="sudokutest.txt")
    optParser.add_option("-i", dest="iters", help="Set max iterations", default=100)
    optParser.add_option("-v", action="store_true", dest="verbose", help="Set verbose", default=False)
    optParser.add_option("-s", dest="solvetimes", help="How many times to solve the puzzle (for runtime analysis)", default=1)
    optParser.add_option("-m", dest="manyPuzzles", help="Do a bunch o' puzzles", action="store_true", default=False)
    (options, args) = optParser.parse_args()
    
    if not options.manyPuzzles:
        for i in range(0,int(options.solvetimes)):
            solver = SudokuSolver(options)
            solver.printPuzzle()
            solver.solve()
            solver.printPuzzle()
            print "Done\n"

    else: # solve lots of puzzles
        hardpuzzles = ["sudokutest1.txt", "sudokutest2.txt"]
        evilpuzzles = ["sudokutest.txt"]
        for i in range(0, 10):
            hardpuzzles.append("sudoku_hard_%s.csv"%i)
        for i in range(0, 10):
            evilpuzzles.append("sudoku_evil_%s.csv"%i)
        print "---HARD PUZZLES---"
        for p in hardpuzzles:
            options.file = p
            solver = SudokuSolver(options)
            stats = solver.solve() # solved, dt, iters
            print "Solved? %s\tTime: %sms\tIters: %s" % stats
        
        print "\n---EVIL PUZZLES---"
        for p in evilpuzzles:
            options.file = p
            solver = SudokuSolver(options)
            stats = solver.solve() # solved, dt, iters
            print "solved=%s\ttime=%s\titers=%s" % stats
