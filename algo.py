#!/usr/bin/python

"""Module alpha_beta
Alpha-Beta pruning algorithm implementation file.

@author: Henry Huang (keenhenry1109@gmail.com)
@date: 11/01/2010
@file: alpha_beta.py

"""

#=====================================================================#
# 	                  Symbolic Constants 			      #
#=====================================================================#
NEG_INFINITY = -10000
POS_INFINITY = 10000

#=====================================================================#
# 	                  Private Functions                	      #
#=====================================================================#

def _is_symmetric(board):
    '''Check if board position is symmetric to 'x=y' axis.
    
    @board: a 2D array storing pawn positions
    @return: True or False
    '''
    
    for i in xrange(len(board)-1):   # from 0 to 6
        for j in xrange(i+1, len(board)): # from 1 to 7
    	    if board[i][j] != board[j][i]: return False
    return True

def _filter_move(who, move, board, move_table):
    '''Allow only moves that do not make board symmetric to 'x=y' axis 
       to be appended to move_table.

    --- Function Arguments ---
    @move: move (a tuple) to be filtered
    @board: current board state; a 2D array
    @move_table: a pool where filtered moves go into (a list)
    '''
   
    if (move[1], move[0]) in move_table:
	if not _is_symmetric(board): move_table.append(move)
    else:
	move_table.append(move)

def _eval_pos(pos):
    '''Evaluate a position solely based on its position.
    Score can be any element of the set: {-4, -3, -2, -1, 0}.
    The most negative score means the worst position.

    --- Function Arguments ---
    @pos: a position to be evaluated
    @return: a score for that position
    '''
    score = 0
    if pos[0]==0 or pos[0]==7: score -= 2
    if pos[0]==1 or pos[0]==6: score -= 1
    if pos[1]==0 or pos[1]==7: score -= 2
    if pos[1]==1 or pos[1]==6: score -= 1
    
    # return the negative of original score for sorting in descending manner
    return -score

def _get_next_moves(who, pos, board, low, high):
    '''Return all the next possible moves for player at position 'pos'.
    This is a game-specific rountine.

    --- Function Arguments ---
    @who: whose ply is it on current board
    @pos: position of the latest move
    @board: an array storing pawn positions
    @low: lowest index bound for board, an int
    @high: highest index bound for board, an int
    @return: a list of all possible next moves 
    '''
  
    move_table = []

    # possible moves in north
    for i in xrange(1, pos[0]-low+1):
	if not board[pos[0]-i][pos[1]]: # if that position is not taken/visited
	    _filter_move(who, (pos[0]-i, pos[1]), board, move_table)
	else:
	    break
    
    # possible moves in north-east
    for i in xrange(1, min(pos[0]-low, high-pos[1])+1):
	if not board[pos[0]-i][pos[1]+i]: # if that position is not taken/visited
	    _filter_move(who, (pos[0]-i, pos[1]+i), board, move_table)
	else:
	    break
    
    # possible moves in east
    for i in xrange(1, high-pos[1]+1):
	if not board[pos[0]][pos[1]+i]: # if that position is not taken/visited
	    _filter_move(who, (pos[0], pos[1]+i), board, move_table)
	else:
	    break
    
    # possible moves in south-east
    for i in xrange(1, high-max(pos[0],pos[1])+1):
	if not board[pos[0]+i][pos[1]+i]: # if that position is not taken/visited
	    _filter_move(who, (pos[0]+i, pos[1]+i), board, move_table)
	else:
	    break
    
    # possible moves in south
    for i in xrange(1, high-pos[0]+1):
	if not board[pos[0]+i][pos[1]]: # if that position is not taken/visited
	    _filter_move(who, (pos[0]+i, pos[1]), board, move_table)
	else:
	    break
    
    # possible moves in south-west
    for i in xrange(1, min(high-pos[0], pos[1]-low)+1):
	if not board[pos[0]+i][pos[1]-i]: 
	    _filter_move(who, (pos[0]+i, pos[1]-i), board, move_table)
	else:
	    break
    
    # possible moves in west
    for i in xrange(1, pos[1]-low+1):
	if not board[pos[0]][pos[1]-i]: 
	    _filter_move(who, (pos[0], pos[1]-i), board, move_table)
	else:
	    break
    
    # possible moves in north-west
    for i in xrange(1, min(pos[0],pos[1])-low+1):
	if not board[pos[0]-i][pos[1]-i]: 
	    _filter_move(who, (pos[0]-i, pos[1]-i), board, move_table)
	else:
	    break
   
    # ------ sorting before returning ------
    # use a very simple sort comparison routine
    # to do a very basic sorting - based on intuition
    return sorted(move_table, key=_eval_pos)

def _get_score(pos, board, low, high):
    '''Return the number of possible moves a player can make at 
    a given position 'pos', plus the number of degrees of freedom. 
    This is a game-specific rountine.

    --- Function Arguments ---
    @pos: position of pawn on board
    @board: an array storing pawn positions
    @low: lowest index bound for board, an int
    @high: highest index bound for board, an int
    @return: a integer score of position 'pos' 
    '''
  
    mv_counts = 0

    # possible moves in north
    for i in xrange(1, pos[0]-low+1):
	if not board[pos[0]-i][pos[1]]: # if that position is not taken/visited
	    mv_counts += 1
	else:
	    break
    # possible moves in north-east
    for i in xrange(1, min(pos[0]-low, high-pos[1])+1):
	if not board[pos[0]-i][pos[1]+i]: # if that position is not taken/visited
	    mv_counts += 1
	else:
	    break
    # possible moves in east
    for i in xrange(1, high-pos[1]+1):
	if not board[pos[0]][pos[1]+i]: # if that position is not taken/visited
	    mv_counts += 1
	else:
	    break
    # possible moves in south-east
    for i in xrange(1, high-max(pos[0],pos[1])+1):
	if not board[pos[0]+i][pos[1]+i]: # if that position is not taken/visited
	    mv_counts += 1
	else:
	    break
    # possible moves in south
    for i in xrange(1, high-pos[0]+1):
	if not board[pos[0]+i][pos[1]]: # if that position is not taken/visited
	    mv_counts += 1
	else:
	    break
    # possible moves in south-west
    for i in xrange(1, min(high-pos[0], pos[1]-low)+1):
	if not board[pos[0]+i][pos[1]-i]: 
	    mv_counts += 1
	else:
	    break
    # possible moves in west
    for i in xrange(1, pos[1]-low+1):
	if not board[pos[0]][pos[1]-i]: 
	    mv_counts += 1
	else:
	    break
    # possible moves in north-west
    for i in xrange(1, min(pos[0],pos[1])-low+1):
	if not board[pos[0]-i][pos[1]-i]: 
	    mv_counts += 1
	else:
	    break
    return mv_counts

def _make_move(board, who, move):
    '''Make the tentative move on board for player 'who'.
    
    --- Function Arguments ---
    @board: a Board object reference
    @who: the player to make the move; either 'p1' or 'p2'
    @move: the move to be make
    '''
    
    board.set_move(move, who)
    
def _unmake_move(board, who, move):	
    '''Unmake the move on board for player 'who'.

    --- Function Arguments ---
    @board: a Board object reference
    @who: the player to make the move; either 'p1' or 'p2'
    @move: the move to be unmake
    '''
    
    board.delete_move(move, who)

#=====================================================================#
# 	                  Public Interface 			      #
#=====================================================================#

def hef(whose_ply, board):
    '''Heuristic Evaluation Function

    Evaluate a board position and return a score. This function returns
    a score relative to the side being evaluated. This is also a game-specific 
    function.

    --- Function Arguments ---
    @whose_ply: either 'p1' or 'p2'; current-ply player to make the move
    @board: Board object reference; board state of current ply
    @return: an integer score relative to the side being evaluated
    '''
    
    opponent = 'p1' if whose_ply=='p2' else 'p2'

    # (number of possible moves of node/ply player)
    # _____________________________________________
    #
    #   (number of possible moves of opponents)
    pos_node = board.get_position(whose_ply)
    pos_oppt = board.get_position(opponent)
    num = _get_score(pos_node, board.get_board(), 0, 7)
    den = _get_score(pos_oppt, board.get_board(), 0, 7)

    # numerator examined first; this is important for algorithm correctness
    if num == 0: return NEG_INFINITY
    if den == 0: return POS_INFINITY

    # otherwise return the ratio	
    return 100*(float(num) / den)

def alpha_beta(whose_ply, board, depth, alpha, beta):
    '''Negamax implementation of Alpha-Beta pruning algorithm.
    
    --- Function Arguments ---
    @whose_ply: either 'p1' or 'p2'; current-ply player to make the move
    @board: Board object reference; the initial board state to be searched
    @depth: the number of plys to search down the tree
    @alpha: the score of node player
    @beta: the score of opponent
    @return: an integer score
    '''

    # return a score computed by a quiescence search
    # need to check if terminal too!
    if depth == 0: return hef(whose_ply, board)

    # otherwise calculate alpha and beta score for next ply
    pos = board.get_position(whose_ply)
    next_ply_player = 'p1' if whose_ply=='p2' else 'p2'
    
    for move in _get_next_moves(whose_ply, pos, board.get_board(), 0, 7):
	_make_move(board, whose_ply, move)   # make move
	score = -alpha_beta(next_ply_player, board, depth-1, -beta, -alpha)
	_unmake_move(board, whose_ply, move) # unmake move
	if score >= beta: return beta 	 # beta-cutoff
	if score > alpha: alpha = score  # max's player's score
    return alpha

def alpha_beta_root(whose_ply, board, depth, alpha, beta):
    '''Alpha-Beta algorithm root function. It calls a recursive
    function 'alpha_beta(node, dept, alpha, beta)'
    
    --- Function Arguments ---
    @whose_ply: either 'p1' or 'p2'; current-ply player to make the move
    @board: Board object reference; the initial board state to be searched
    @depth: the number of plys to search down the tree
    @alpha: the score of node player
    @beta: the score of opponent
    @return: the best move so far 
    '''
    
    # calculate the best move for next ply
    best_move, pos = None, board.get_position(whose_ply)
    next_ply_player = 'p1' if whose_ply=='p2' else 'p2'
    
    for move in _get_next_moves(whose_ply, pos, board.get_board(), 0, 7):
	_make_move(board, whose_ply, move)   # make move
	score = -alpha_beta(next_ply_player, board, depth-1, -beta, -alpha)
	_unmake_move(board, whose_ply, move) # unmake move
	if score > alpha: alpha, best_move = score, move
    return best_move
