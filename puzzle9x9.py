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
        # for r in rows:
        #     print(r.__repr__())
        # for c in columns:
        #     print(c.__repr__())
        # for s in squares:
        #     print(s.__repr__())
        self.cells = cells
        self.groups = rows + columns + squares
        self.rows = rows
        Verbosity.print = self.print
