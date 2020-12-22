#!/usr/bin/python
import argparse
from verbosity import Verbosity
from puzzle9x9 import Puzzle9x9


def toNumber(char):
    if char == '.':
        return 0
    return int(char)


parser = argparse.ArgumentParser(description='Solve a sudoku 9x9 puzzle.')
parser.add_argument('file', help='sudoku-file', nargs=1)
parser.add_argument('--hints', action="store_true")
parser.add_argument('-v', "--verbose", type=int, help="verbosity 1-4")

args = parser.parse_args()
filename = args.file
verbosity = args.verbose
hints = args.hints
# print(f"hints: {hints}, verbosity: {verbosity}, filename: {filename}")
Verbosity.level = verbosity or 0
Verbosity.hints = hints
# print('verbosity level', Verbosity.level)

f = open(filename[0], "r")
text = f.read()
f.close()
# print(text)
values = [toNumber(char) for char in text if 46 <= ord(char) <= 57]
# print(values)
if len(values) != 81:
    raise Exception(f"Invalid sudoku: expected 81 digits, not {len(values)}")

# try:
sudoku = Puzzle9x9(values)
# sudoku.print()
sudoku.solve()
# except Exception as error:
# print('exception', error)
sudoku.print()
