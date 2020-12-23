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
Verbosity.level = args.verbose or 0
Verbosity.hints = args.hints
filename = args.file.pop()
f = open(filename, "r")
text = f.read()
f.close()

values = [toNumber(char) for char in text if 46 <= ord(char) <= 57]
if len(values) != 81:
    raise Exception(f"Invalid sudoku: expected 81 digits, not {len(values)}")

sudoku = Puzzle9x9(values)
if Verbosity.level >= 1:
    print("Initial sudoku")
    sudoku.print()
sudoku.solve()
if (len(sudoku.solutions) == 0):
    print("Could not solve the puzzle, are you sure about the input?")
elif len(sudoku.solutions) == 1:
    Puzzle9x9(sudoku.solutions[0]).print()
else:
    n = 0
    print("Multiple solutions!")
    for solution in sudoku.solutions:
        n += 1
        print(f"\nSolution {n}:")
        Puzzle9x9(solution).print()
