import logging
from .game import Game

class Player:
    '''a person who plays'''
    def __init__(self, name):
        self.turns = 0
        self.name = name
        self.g = Game()
        logging.info("Welcome, {}".format(name))

    def set_turns(self, num):
        self.turns = num

    def process_turn(self):    
        self.g.run_turn()
        self.turns -= 1
