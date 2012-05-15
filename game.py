#!/usr/bin/python

"""Module game
Game engine for Game Isolation. It is also an agent bridging AI module and UI module.

@author: Henry Huang (keenhenry1109@gmail.com)
@date: 10/25/2010
@file: game.py

"""

from board import Board
from algo import *
from ui_cmdline import Terminal

class Game(object):
    '''Class Game

    This class implements the game engine for game Isolation.
    '''

    def __init__(self):
	self.board = Board()
	self.cur_turn = 'p1'
	self.gameover = False
	self.winner = 'n/a'
	self.pc_first = True		# game engine goes first
	self.algo = alpha_beta_root     # assigning function pointer
	self.ui = Terminal(self.board)	# game UI is command line terminal!
	self.nom = 2 			# number of moves done on board
  
    def __get_direction(self, pos, move):
	'''Find the direction of move relative to pos.

	Return 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W' or 'NW'.
	'''

	if move[1]==pos[1] and move[0]<pos[0]: return 'N'
	if move[1]==pos[1] and move[0]>pos[0]: return 'S'
	if move[0]==pos[0] and move[1]<pos[1]: return 'W'
	if move[0]==pos[0] and move[1]>pos[1]: return 'E'
	if move[1]>pos[1] and (move[1]-pos[1])==(move[0]-pos[0]): return 'SE'
	if move[1]<pos[1] and (move[1]-pos[1])==(move[0]-pos[0]): return 'NW'
	if move[1]>pos[1] and (move[1]-pos[1])==(pos[0]-move[0]): return 'NE'
	if move[1]<pos[1] and (move[1]-pos[1])==(pos[0]-move[0]): return 'SW'

	# move is not in any of the 8 directions:
	return None

    def __is_blocked(self, drt, pos, move):
	'''Check if move is blocked by visited positions on board. 
	
	--- Function Arguments ---
	@drt: direction the move is in.
	@pos: the original position the pawn was at.
	@move: the move the pawn at pos try to make.
	@return: True if blocked, otherwise False.
	'''

	board = self.board.get_board()
	if drt == 'N':
	    for i in xrange(1, pos[0]-move[0]):
	    	if board[pos[0]-i][pos[1]]: return True
	elif drt == 'S':
	    for i in xrange(1, move[0]-pos[0]):
	    	if board[pos[0]+i][pos[1]]: return True
	elif drt == 'E':
	    for i in xrange(1, move[1]-pos[1]):
	    	if board[pos[0]][pos[1]+i]: return True
	elif drt == 'W':
	    for i in xrange(1, pos[1]-move[1]):
	    	if board[pos[0]][pos[1]-i]: return True
	elif drt == 'NE':
	    for i in xrange(1, move[1]-pos[1]):
	    	if board[pos[0]-i][pos[1]+i]: return True
	elif drt == 'NW':
	    for i in xrange(1, pos[1]-move[1]):
	    	if board[pos[0]-i][pos[1]-i]: return True
	elif drt == 'SE':
	    for i in xrange(1, move[1]-pos[1]):
	    	if board[pos[0]+i][pos[1]+i]: return True
	else:	# SW
	    for i in xrange(1, pos[1]-move[1]):
	    	if board[pos[0]+i][pos[1]-i]: return True
	return False

    def __set_gameover(self):
	"A helper function to set gameover and winner flag."
	
	self.gameover = True
    	self.winner = 'p1' if self.cur_turn=='p2' else'p2'

    def __set_search_depth(self):
	"A helper function to set search depth for alpha-beta algorithm."
	
	if self.nom <= 15: return 6
	elif self.nom <= 25: return 8
	elif self.nom <= 35: return 10
	elif self.nom <= 45: return 12
	elif self.nom <= 55: return 14
	else: return 10 
    
    def is_valid_move(self, move):
	'''Check if move is valid.

	Assume the format of move is sanitized by UI interface.

	--- Function Arguments ---
	@move: the move player in the current turn makes.
	@return: False if not a valid move, otherwise True.
	'''
    	
	# check entry validity
    	if not move[0] in xrange(self.board.size+1): return False
    	if not move[1] in xrange(self.board.size+1): return False

	# check if move already exists on board!
	board = self.board.get_board()
	if board[move[0]][move[1]]: return False

	# check if move direction is correct
	pos = self.board.get_position(self.cur_turn)
	drt = self.__get_direction(pos, move)
	if not drt: return False

	# check if move is blocked by visited moves on the path
	if self.__is_blocked(drt, pos, move): return False
	return True

    def make_move(self, move):
	"Make the move for the player in the current turn. Assume move is sanitized and checked."

	self.board.set_move(move, self.cur_turn)
	self.cur_turn = 'p1' if self.cur_turn=='p2' else 'p1'
	self.nom += 1

    def ai_goes(self):
	"Game AI makes his move."

	# determine the depth for alpha-beta algorithm to search first
    	depth = self.__set_search_depth()

        # find best move that can be searched so far
	move = self.algo(self.cur_turn, self.board, depth, NEG_INFINITY, POS_INFINITY)

	# best move can be 'not found' when AI knows it loses 
	# in that case a 'None' type is returned!
	if move: self.make_move(move)
	else: self.__set_gameover()

    def human_goes(self):
	"Human player make his/her move."
        
	self.cur_turn = 'p2'
	while True:
            move = self.ui.prompt_user_input()
	    if self.ui.is_surrender_move(move): 
		self.__set_gameover()
		break
    	    elif self.is_valid_move(move): 
		self.make_move(move)
		break
	    else:
		print 'Illegitimate move!'

    def reset_game(self):
	"Reset all game states when game is over."
	
	self.board.clear_board() 
	self.cur_turn = 'p1'
	self.gameover = False
	self.winner = 'n/a'
	self.pc_first = True		# game engine goes first
	self.nom = 2 			# number of moves done on board
