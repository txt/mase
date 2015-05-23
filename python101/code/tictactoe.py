"""
An example client that talks to olinapp3.

Code related to Think Python: An Introduction to Software Design

Copyright 2011 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import random
import sys

from app3client import App3Client


def make_client(args, password='ThePassword'):
    """Make an app3 client that talks to an olinapp3 server."""
    if 'local' in args:
        client = App3Client('localhost:8080', password)
    else:
        client = App3Client('olinapp3.appspot.com', password)

    return client


def test_client(client, game_id):
    """Run the client through some tests."""
    print client.list('tictactoe')

    print client.post('tictactoe', game_id,
                      dict(board='XO.O.O.XX', move='X'))

    print client.exists('tictactoe', game_id)

    print client.get('tictactoe', game_id)

    print client.list('tictactoe')

    print client.delete('tictactoe', game_id)

    print client.list('tictactoe')


def setup_game(client, game_id):
    """Create a tictactoe game."""
    return client.post('tictactoe', game_id,
                       dict(board='XO.O.O.XX', move='X'))


def delete_game(client, game_id):
    """Delete a tictactoe game."""
    return client.delete('tictactoe', game_id)


def move_and_win(client, game_id):
    """Download game state.  Check whether it is X's move.
    If so, modify game state and upload it.  Return the game state
    as a dictionary.
    """
    # FILL IN THE BODY OF THIS FUNCTION.
    # YOU WILL NEED TO CHANGE THE PASSWORD IN make_client.


def main(script, *args):
    client = make_client(args)
    game_id = 'game%d' % random.randint(0, 1000000)
    test_client(client, game_id)

    print setup_game(client, game_id)
    print move_and_win(client, game_id)
    print delete_game(client, game_id)


main(*sys.argv)
