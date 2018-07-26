from datetime import datetime

import click
import requests


def _make_file(name, content):
    filename = name + '.pgn'
    with open(filename, 'wb') as file:
        file.write(content)
    return filename


@click.command()
@click.argument('username', required=True)
def lichess(username: str):
    """ Get games played on lichess
    """

    url = "https://lichess.org/games/export/{name}".format(name=username)
    response = requests.get(url, allow_redirects=True)

    if response:
        _make_file(username, response.content)
    else:
        click.secho("Unable to download data. Please check the username")


@click.command()
@click.argument('username', required=True)
@click.option('--year', '-y', help='year for which the game data is required',
              default=datetime.now().month)
@click.option('--mon', '-m', help='month for which game data is required',
              default=datetime.now().year)
def chess_com(username: str, year: int, mon: int):
    """ Get games played on chess.com
    """

    url = "https://api.chess.com/pub/player/{name}/games/{yr}/{mm}/pgn".format(name=username, yr=year, mm=mon)
    response = requests.get(url, allow_redirects=True)

    if response:
        _make_file(username, response.content)
    else:
        click.secho("Unable to download data. Please check the username/month/year")
