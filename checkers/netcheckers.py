# checkers server

import sys
import socket
from threading import Thread
import argparse

from checkers import Board
from checkersgui import drawBoard
import pygame

import pickle # same as pickle but faster

BUFSIZE = 2048 # what is the actual minimum?
sock = None

# pygame variables
size = width, height = 496,496
dx,dy = width/8, height/8
black = 0,0,0
white = 255,255,255
green = 0, 255, 0
dkgreen = 0, 55, 0

COLORS = {0:((255,0,0), (155,0,0)), 1:((0,0,255), (0,0,155))}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="Run as a checkers server", action="store_true")
    parser.add_argument("-c", "--client", help="Run as a checkers client", action="store_true")
    parser.add_argument("-a", "--address", type=str, help="Set the IP address to connect", default="localhost")
    parser.add_argument("-p", "--port", type=int, help="Set the port number to connect", default=8080)
    args = parser.parse_args()
    
    if not args.server and not args.client:
        print("You must choose to run as either a client or server!")
        sys.exit(0)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock = None
    
    # set up pygame
    pygame.init()
    screen = pygame.display.set_mode(size)
    selected = None
    team = False
    
    # initialize board
    board = Board()
    
    myteam = not args.server
    
    # set up sockety things
    if args.server:
        print("Running as server @ %s:%s" % (args.address, args.port))
        sock.bind((args.address, args.port))
        
        # get connections
        sock.listen(1)
        (clientsock, addr) = sock.accept()
        print("got a connection")
        clientsock.send(pickle.dumps(board.grid))
    
    elif args.client:
        print("Running as client @ %s:%s" % (args.address, args.port))
        sock.connect((args.address, args.port))
        
        # initialize Board
        board = Board()
        board.grid = pickle.loads(sock.recv(BUFSIZE))
    
    # display the initial board
    drawBoard(screen, team, board, selected)
    pygame.display.flip()
    
    # pygame main loop
    while True:
        if myteam == team: # it's your turn!
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
                    
                    # send the board
                    if args.server:
                        clientsock.send(pickle.dumps((team, board.grid)))
                    elif args.client:
                        sock.send(pickle.dumps((team, board.grid)))

        else: # not your turn
            print("waiting for other turn")
            if args.server:
                try:
                    data = clientsock.recv(BUFSIZE)
                    if not data:
                        print("no data, bye")
                        sys.exit(0)
                    team, board.grid = pickle.loads(data)
                except:
                    print ("UH OHHH")
                    print(sys.exc_info())
                    sys.exit(0)
            elif args.client:
                team, board.grid = pickle.loads(sock.recv(BUFSIZE))
            # get the board
        
        drawBoard(screen, team, board, selected)
        pygame.display.flip()
    
    #################
    '''
    if args.server: # if they also had -c, well, that's their problem
        print("Running as server @ %s:%s" % (args.address, args.port))
        sock.bind((args.address, args.port))
        
        # get connections
        sock.listen(1)
        (clientsock, addr) = sock.accept()
        print "got a connection"
        
        # initialize board
        board = Board()
        print board
        clientsock.send(pickle.dumps(board.grid))
        
        # listen for data
        while True:
            try:
                data = clientsock.recv(BUFSIZE)
                if not data:
                    print "no data, bye"
                    break
                board.grid = pickle.loads(data)
                print board
                clientsock.send(pickle.dumps(board.grid))
            except Exception,e:
                print "UH OHHH",e
                break
        clientsock.close()
    
    elif args.client:
        print("Running as client @ %s:%s" % (args.address, args.port))
        sock.connect((args.address, args.port))
        
        # initialize Board
        board = Board()
        board.grid = pickle.loads(sock.recv(BUFSIZE))
        print board
        
        while True:
            data = raw_input("> ")
            if not data:
                break
            sock.send(pickle.dumps(board.grid))
            board.grid = pickle.loads(sock.recv(BUFSIZE))
            print board
    '''
    
    sock.close()
    