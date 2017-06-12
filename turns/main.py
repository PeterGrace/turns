"""The primary module for this skeleton application."""
import click
from .player import Player
import logging



@click.command()
@click.option('--debug', is_flag=True)
def main(debug):

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    p = Player("Pete")
    p.set_turns(10)
    while p.turns > 0:
        choice = input("(D)iscover, (M)arket")
        if choice == "D":
            p.g.lands+=10
        elif choice == "M":
            p.g.sell_food()
        p.process_turn()


if __name__ == '__main__':
    main()
