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
    p.set_turns(100)
    while p.turns > 0:
        choice = input("[L:{land}][S:{serfs}][F:{food}][T:{turns}] (D)iscover, (M)arket: ".format(land=p.g.lands,serfs=p.g.serfs, food=p.g.food, turns=p.turns))
        if choice == "D":
            p.g.lands+=10
        elif choice == "M":
            p.g.sell_food()
        p.process_turn()


if __name__ == '__main__':
    main()
