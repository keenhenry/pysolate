#!/usr/bin/python

class Terminal(object):
    '''Class Terminal

    This class implements command line user interface for Game Isolation.
    '''

    def __init__(self, board):
	self.board = board   # board is a Board object passed in.

    def __is_correct_format(self, move):
    	'''Check if move entered by user is in correct string format.

    	@move: the move input by user(s) to be checked.
	@return: True if valid, otherwise False.
    	'''

    	# check type
    	if not isinstance(move, tuple): False
    	# check length
    	if len(move) != 2: return False
    	# check entry validity
    	if not (isinstance(move[0], int) and isinstance(move[1], int)): 
		return False
    	return True

    def prompt_user_input(self):
	'''Prompt user for pawn's next move position.

	@return: return a valid-formatted move (a tuple) from user.
	'''

	move = None
	while True:
	    move = input('Enter your move here: ')
	    if self.__is_correct_format(move): break
	    else: print "Invalid move format: (x, y)"
	return move
    
    def is_surrender_move(self, move):
	'''A helper function to check if the move returned by human player 
	is a surrender move, namely (-1, -1).

	--- Function Arguments ---
	@move: the move to be checked.
	@return: True or False
	'''

	return True if move==(-1,-1) else False

    def print_start_game(self):
	print
	print "***********************************************************"
	print "*                 GAME ISOLATION STARTS                   *"
	print "***********************************************************"
	print

    def who_goes_first(self):
	answer = raw_input('You go first (Y/N)? ').lower()
	return False if answer=='yes' or answer== 'y' else True

    def print_board(self):
	"Print out game board's string representation on terminal."
	print self.board

    def print_winner(self, winner):
	"Print the winner of the game."

	answer = 'COMPUTER' if winner=='p1' else 'YOU'
	print "The winner is", answer, "!\n"

    def play_again(self):
	'''Ask if user wants to play game again at the end of the game.

	@return: True or False.
	'''

	answer = raw_input('\nPlay again (Y/N)? ').lower()
	return True if answer=='yes' or answer== 'y' else False

    def print_end_game(self):
	print "\n===================== GRAZIE! CIAO! =======================\n"
