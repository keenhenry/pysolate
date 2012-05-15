#!/usr/bin/python

"""Module main
main.py is program entry point for Game Isolation.

@author: Henry Huang (keenhenry1109@gmail.com)
@date: 01/06/2010
@file: main.py
"""

from game import Game

def main():
  ''' Main program of isolation 
  '''
    
  # Initialize game isolation ...
  game = Game()

  while True:
    # start game
    game.ui.print_start_game()

    # ask user for going first
    game.pc_first = game.ui.who_goes_first()
    	
    # two possible execution flows:
    while not game.gameover:
      game.ui.print_board()
      if game.pc_first: game.ai_goes()
      else: game.human_goes()
      game.ui.print_board()
	   
      if game.gameover: break
      elif game.pc_first: game.human_goes()
      else: game.ai_goes()

    # print winner of the game
    game.ui.print_winner(game.winner)

    # reset game states
    game.reset_game()
    
    # to play again or not?
    if not game.ui.play_again(): break

  # game is over
  game.ui.print_end_game()

if __name__ == '__main__': main()
