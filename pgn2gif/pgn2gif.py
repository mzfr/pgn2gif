#!/usr/bin/env python3

import os
import glob

import click
from chess import pgn

from . import download_data
from . import handle_gifs


def _handle_pgn(path: str):
    """Read all the games present within a pgn file

        :path: path of the pgn file
        :return: list of game objects
    """
    games = []

    if os.path.exists(path):

        with open(path) as file:
            while True:
                game = pgn.read_game(file)
                games.append(game)

                if game is None:
                    break
    return games


def _valid_pgn_files(pgn_files):
    """ Check for valid PGN files

        Validation is:
            1) Whether the file(s) exists or not.
            2) Whether the file(s) are empty or not
    """
    all_files = []

    if pgn_files:
        for file in pgn_files:
            if os.path.getsize(file) > 0:
                all_files.append(file)
            else:
                click.secho("Empty PGN file found !!", fg='red')
                return False

        return all_files

    else:
        click.secho("No pgn found in specified path", fg='red')


def _check_existing_files(path: str, name: str):
    """Check if the given file exists in a given path
        :path: Path to the file
        :name: Name of the file

        :return: boolean value
    """
    file = os.path.join(path, name)
    if os.path.exists(file):
        return True


def convert_pgn_to_gif(path, size, duration, output_dir, color, game_index, all_games):
    """Call other gif functions to change a PGN into a gif
        :path: path to the pgn file
        :size: size of the gif in dimensions
        :duration: speed of the pieces with which they move in Gif
        :output_dir: where Gifs need to be stored
        :color: color of the chess board in a gif
    """
    games = _handle_pgn(path)

    # When the option for all the games is given
    if all_games:

        for index, game in enumerate(games[:-1]):
            name = os.path.basename(path)[:-4] + '-' + str(index) + '.gif'

            if not _check_existing_files(output_dir, name):
                handle_gifs.make_a_gif(game, duration, size, name, output_dir, color)
            else:
                click.secho("gif name %s already exists " % name, fg='green')

    # When a particular index is given
    else:
        name = os.path.basename(path)[:-4] + '.gif'
        if game_index - 1 < (len(games) - 1):
            if not _check_existing_files(output_dir, name):
                handle_gifs.make_a_gif(games[game_index], duration, size, name, output_dir, color)
            else:
                click.secho("gif name %s already exists " % name, fg='green')
        else:
            click.secho("Game on the given index doesn't exists", fg="red")


@click.group(invoke_without_command=True)
@click.option('-p', '--path', help='path to the pgn file/folder', default=os.getcwd() + '/')
@click.option('-s', '--speed', help='speed with which pieces move in gif.', default=0.5)
@click.option('-o', '--out', help='name of the output folder', default=os.getcwd() + '/gifs/')
@click.option('-si', '--size', help='size of the gif', default=480)
@click.option('-c', '--color', help='color of chess board',
              type=click.Choice(['green', 'blue', 'brown']), default='brown')
@click.option('-g', '--game-index', help='index of the game for which gif is to be made', default=0)
@click.option('--all-games', help='make gif of all the games found in a PGN', is_flag=True, default=False)
@click.pass_context
def main(ctx, path, speed, out, size, color, game_index, all_games):
    """Create GIFs from PGNs
    """
    if ctx.invoked_subcommand is None:

        if not os.path.exists(out):
            os.makedirs(out)

        if os.path.isfile(path):
            convert_pgn_to_gif(path, size, speed, out, color, game_index, all_games)

        elif os.path.isdir(path):
            pgn_files = glob.glob(path + '*.pgn')

            valid_pgn_file = _valid_pgn_files(pgn_files)

            if valid_pgn_file:
                for file in valid_pgn_file:
                    convert_pgn_to_gif(file, size, speed, out, color, game_index, all_games)
            else:
                click.secho("Try using the download option for getting valid pgn files")


main.add_command(download_data.lichess)
main.add_command(download_data.chess_com)
if __name__ == "__main__":
    main()
