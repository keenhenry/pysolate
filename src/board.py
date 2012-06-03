#!/usr/bin/python

"""Module board
A data structure to represent a Board object in game Isolation.

@author: Henry Huang (keenhenry1109@gmail.com)
@date: 10/20/2010
@file: board.py

"""

def singleton(cls):
    "singleton function object used to decorate class Board."
    instances = {}
    def getInstance():
        if cls not in instances:
            instances[cls] = cls()
    	return instances[cls]
    return getInstance

@singleton
class Board(object):
    '''Class Board
  
    This is a decorated class, decorated by singleton function object. That said, 
    class Game can only be instantiated once, and hence remain singleton instance 
    at all times. Internally, Board uses a dictionary to represent a board.
    '''

    def __init__(self, size=8, sym_p1='x', sym_p2='o'):
	'''
	@board: initial board
	@size: the board (a square/grid) length
	@sym_p1: player 1 symbol
	@sym_p2: player 2 symbol
	'''

	self.size = size-1
	self.sym_p1 = sym_p1
	self.sym_p2 = sym_p2
	self.board = [[None for j in xrange(size)] for i in xrange(size)]
	self.board[self.size][self.size] = self.board[0][0] = (None, None)
	self.pos_x = (0, 0)
	self.pos_o = (self.size, self.size)
    
    def __str__(self):
	"Return human-readable string of Board object"

	s = '\n  '
	
	# header string
	for i in xrange(self.size+1):
	    s += str(i) + ' '
	s += '\n'

	# the rest of the board
	for i in xrange(self.size+1):
	    for j in xrange(self.size+1):
		if j == 0: s += str(i) + ' '
		if self.board[i][j]: 
		    if self.pos_x==(i,j):   s += self.sym_p1 + ' '
		    elif self.pos_o==(i,j): s += self.sym_p2 + ' '
		    else:		    s += '* '
		else:		     	 s += '- '
	    s += '\n'
	return s
    
    def set_move(self, move, whose_turn): 
	'''Make the move on board for player whose_turn.

	--- Function Arguments ---
	@move: the move (a tuple) a player wants to make
	@whose_turn: either 'p1' or 'p2'
	'''

	if whose_turn == 'p1':
	    self.board[move[0]][move[1]] = self.pos_x   # memorize last pawn position!
	    self.pos_x = move 		    	        # update position of pawn
	else:
	    self.board[move[0]][move[1]] = self.pos_o   # memorize last pawn position!
	    self.pos_o = move
    
    def delete_move(self, move, whose_turn): 
	'''Unmake the move on board for player whose_turn.

	--- Function Arguments ---
	@move: the move (a tuple) a player wants to unmake
	@whose_turn: either 'p1' or 'p2'
	'''
	
	if whose_turn == 'p1':
	    self.pos_x = self.board[move[0]][move[1]]   # update pawn position to previous one
	    self.board[move[0]][move[1]] = None   	# delete move
	else:
	    self.pos_o = self.board[move[0]][move[1]]   # update pawn position to previous one
	    self.board[move[0]][move[1]] = None   	# delete move

    def get_position(self, who):
	"Get the current position of the player (who) on board."
	return self.pos_x if who == 'p1' else self.pos_o

    def get_board(self):
	"Get the dictionary 'board'"
	return self.board

    def clear_board(self):
	"Clear board array for reuse."
	del self.board[:]
	self.pos_x = (0, 0)
	self.pos_o = (self.size, self.size)
	self.board = [[None for j in xrange(self.size+1)] for i in xrange(self.size+1)]
	self.board[self.size][self.size] = self.board[0][0] = (None, None)
