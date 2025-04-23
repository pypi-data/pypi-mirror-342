"""

Usage:
    drawlogo <input-file> [-O <path> | --output <path>] [--words-count <int>] [-r | --revcomp]
    drawlogo -h | --help

Arguments:
    <input-file>     Path to input pcm or ppm matrix
    <path>           Path to output svg file or directory
    <int>            Any positive integer


Options:
    -h, --help                      Show this.
    -O <path>, --output <path>      Output directory or file path. [default: ./]
    --words-count <int>             Words count for ppm matrix representation. [default: 100]
    -r, --revcomp                   If true draw revcomp motif
"""

from docopt import docopt
from schema import Schema, And, Const, Or, SchemaError, Use
from svgutils import transform
import numpy as np
from math import lgamma
import os
import pathlib


script_path = os.path.join(pathlib.Path(__file__).parent.absolute())


def get_letter_svg_by_name(name):
    return os.path.join(script_path, 'letters', '{}.svg'.format(name))

#
# get_revcomp = {
#     'A': 'T',
#     'T': 'A',
#     'C': 'G',
#     'G': 'C',
# }
#
# nucleotides = ['A', 'C', 'G', 'T']
#
# visible_cut_tr = 0.01
#
# unit_width = 300
# unit_height = 600


def get_KDIC(counts, N):
    return 1 / (N * np.log(0.25)) * (
                lgamma(N + 1) + sum([x * np.log(0.25) - lgamma(x + 1) for x in counts]))


def get_heights(lines, mode='freq', words=100):
    heights = []
    nucleotides = ['A', 'C', 'G', 'T']
    m = len(lines)
    for counts in lines:
        N = sum(counts)
        if mode == 'freq':
            KDIC = get_KDIC([x * words for x in counts], words)
            heights.append(sorted(list(zip(nucleotides, [(x / N) * KDIC for x in counts])),
                                  key=lambda x: x[1], reverse=True))
        elif mode == 'KDIC':
            KDIC = get_KDIC(counts, N)
            heights.append(sorted(list(zip(nucleotides, [(x / N) * KDIC for x in counts])),
                                  key=lambda x: x[1], reverse=True))

    return m, heights


def place_letter_on_svg(figure, letter_svg, unit_width, x, y, h):
    letter_object = transform.fromfile(letter_svg)
    letter_root = letter_object.getroot()
    # 13.229 and 26.458 are letter svg view box w and h
    letter_root.scale_xy(unit_width/13.229, h/26.458)
    letter_root.moveto(x, y)
    figure.append(letter_root)


def renorm(position):
    # TODO add as a parameter
    visible_cut_tr = 0.01
    letters, heights = zip(*position)
    total_height = sum(heights)
    new_total_height = 0
    new_heights = []
    for height in heights:
        if height < visible_cut_tr * total_height:
            new_heights.append(0)
        else:
            new_total_height += height
            new_heights.append(height)
    new_heights = [x * new_total_height / total_height for x in new_heights]
    return zip(letters, new_heights)


def draw_logo(file_path_or_matrix, out_path, unit_width, unit_height, revcomp=False, words=100, mode='KDIC'):
    if os.path.isfile(file_path_or_matrix):
        if file_path_or_matrix.endswith('.pcm'):
            mode = 'KDIC'
        elif file_path_or_matrix.endswith('.ppm'):
            mode = 'freq'
        else:
            raise ValueError(file_path_or_matrix, ' should ends with ".pcm" or ".ppm"')
        lines = []
        with open(file_path_or_matrix) as f:
            for line in f:
                if line.startswith('>'):
                    continue
                try:
                    lines.append(list(map(float, line.strip('\n').split('\t'))))
                except ValueError:
                    lines.append(list(map(float, line.strip('\n').split(' '))))
    else:
        lines = file_path_or_matrix
    m, heights = get_heights(lines, mode=mode, words=words)
    get_revcomp = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C',
    }
    if os.path.isdir(out_path):
        if os.path.isfile(file_path_or_matrix):
            out_path = os.path.join(out_path, '{}{}.svg'.format(
                                    os.path.splitext(os.path.basename(file_path_or_matrix))[0],
                                    '_revcomp' if revcomp else ''))
        else:
            out_path = os.path.join(out_path, 'matrix{}.svg'.format('_revcomp' if revcomp else ''))

    fig = transform.SVGFigure("{}".format(m * unit_width), "{}".format(unit_height))

    for pos, pack in enumerate(heights[::-1] if revcomp else heights):
        current_height = 0
        for letter, height in renorm(pack):
            # Draw letter with offset of pos*unit_width, current_height*unit_height and height of height*unit_height
            place_letter_on_svg(
                fig,
                get_letter_svg_by_name(get_revcomp[letter] if revcomp else letter),
                unit_width,
                pos * unit_width,
                (1-current_height - height) * unit_height,
                height * unit_height
            )
            current_height += height

    fig.save(out_path)


def dir_writable(x):
    return os.path.isdir(x) and os.access(x, os.W_OK)


def file_parent_writable(x):
    parent = os.path.dirname(x) or '.'
    return os.path.isdir(parent) and os.access(parent, os.W_OK)

def main():
    args = docopt(__doc__)
    schema = Schema({
        '<input-file>': And(
            Const(os.path.exists, error='Input file should exist'),
            Const(lambda x: os.access(x, os.R_OK), error='No read permissions')
        ),
        '--output': Or(
            Const(dir_writable, error='No write permissions'),
            Const(file_parent_writable, error='Parent not writable')
        ),
        '--words-count': Use(int, error='Number of words must be positive integer'),
        str: bool
    })
    try:
        args = schema.validate(args)
    except SchemaError as e:
        print(__doc__)
        exit('Error: {}'.format(e))

    matrix_path = args['<input-file>']
    out_path = args['--output']
    is_revcomp = args['--revcomp']
    n_words = args['--words-count']

    unit_width = 30
    unit_height = 60
    draw_logo(
        matrix_path,
        unit_width=unit_width,
        unit_height=unit_height,
        out_path=out_path,
        revcomp=is_revcomp,
        words=n_words
)
