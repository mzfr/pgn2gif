import os
import click
import cairosvg
import imageio

from chess import svg


def make_a_gif(game, duration, size, name, output_dir, color):
    """Changes PGN to gif format

        :game: chess game Object
        :duration: speed of the pieces moving in a gif
        :size: size(dimension) of the gif created
        :name: name of the gif file
        :output_dir: path to the output directory
        :color: color of the chess board
    """
    board = game.board()

    images = [_position_to_image(board, size, color)]

    for move in game.main_line():
        board.push(move)
        image = _position_to_image(board, size, color)

        if image is False:
            return False

        images.append(image)

    images.append(images[len(images) - 1])
    gif_name = os.path.join(output_dir, name)
    imageio.mimsave(gif_name, images, duration=duration)
    click.secho("created : %s" % os.path.basename(gif_name), fg='green')


def _position_to_image(board, size, color):
    """ Produce an image for every move

        :board: object for the board moves
        :size: size of the board
        :color: color of the chess board
    """
    css = {'green': 'css/green.css', 'blue': 'css/blue.css'}
    css_content = None
    if color != 'brown':
        css_content = open(css[color]).read()
    svg_file = svg.board(board, size=size, style=css_content)
    bytes = cairosvg.svg2png(bytestring=svg_file, border=False)
    return imageio.imread(bytes, format="PNG")
