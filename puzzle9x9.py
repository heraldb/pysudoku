#!/usr/bin/python
#import sys
import argparse
from verbosity import Verbosity
from cell import Cell
from group import Group
from puzzle import Puzzle


class Puzzle9x9(Puzzle):
    def __init__(self, values):
        cells = [Cell(v) for v in values]
        rows = [Group('row', cells[v * 9:(v * 9) + 9]) for v in range(9)]
        Group.nr = 0
        columns = []
        for c in range(9):
            columns.append(
                Group('column', [cells[c + v * 9] for v in range(9)]))

        Group.nr = 0
        squares = []
        for n in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
            squares.append(Group('square',
                                 cells[n:n + 3] +
                                 cells[n + 9:n + 12] +
                                 cells[n + 18:n + 21]
                                 ))
        for r in rows:
            print(r.__repr__())
        for c in columns:
            print(c.__repr__())
        for s in squares:
            print(s.__repr__())
        self.cells = cells
        self.groups = rows + columns + squares
        self.rows = rows


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
print(f"hints: {hints}, verbosity: {verbosity}, filename: {filename}")
Verbosity.level = verbosity or 0
Verbosity.hints = hints
print('verbosity level', Verbosity.level)

f = open(filename[0], "r")
text = f.read()
f.close()
print(text)
values = [toNumber(char) for char in text if 46 <= ord(char) <= 57]
print(values)
if len(values) != 81:
    raise Exception(f"Invalid sudoku: expected 81 digits, not {len(values)}")

# try:
sudoku = Puzzle9x9(values)
sudoku.print()
sudoku.solve()
# except Exception as error:
# print('exception', error)
sudoku.print()
