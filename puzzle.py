from group import Group
from cell import Cell
from verbosity import Verbosity


class Puzzle:
    def __init__(self, cells=[], groups=[], rows=[]):
        self.cells = cells
        self.groups = groups
        self.rows = rows

    def remaining_groups(self):
        return [g for g in self.groups if not g.is_ready()]

    def remaining_cells(self):
        return [c for c in self.cells if not c.value]

    def solve(self, level=0):
        prev_progress = -1
        level += 1
        while Cell.progress > prev_progress:
            prev_progress = Cell.progress
            for group in self.groups:
                group.solve()

            if prev_progress == Cell.progress and not Group.search_islands:
                Group.search_islands = True
                prev_progress -= 1  # force extra iteration

        # if still not solved, fall back on backtrack trial and error
        if len(self.remaining_groups()) > 0:
            self.backtrack(level)

    def print(self, cell=None):
        for i in range(1, 10):
            if i == 4 or i == 7:
                print(' ', end='')
            print(f"  {i}", end='')
        print()
        print(f"+{'-' * 29}+")
        n = 0
        for row in self.rows:
            n += 1
            row.print(cell)
            print('', n)
            if n % 3 == 0:
                print(f"+{'-' *29}+")

    def backtrack(self, level):
        print(f"Starting backtrack algoritm (level {level})")
        cells = self.remaining_cells()
        cells.sort(key=lambda c: len(c.options))
        for cell in cells:
            Verbosity.verbose(3,
                              "cell {} has {} options".
                              format(cell.__str__(), len(cell.options))
                              )
            for option in cell.options:
                Verbosity.verbose(1, f"try {option} for cell {cell.__str__()}")
                remaining_cells = self.remaining_cells()
                for c in remaining_cells:
                    c.save_state(level)
                cell.set(option)
                for group in self.groups:
                    group.cleanup_options()
                try:
                    self.solve(level)
                except Exception:
                    Verbosity.verbose(1,
                                      "option {} for {} did not work out".
                                      format(option, cell.__str__()))
                    for c in remaining_cells:
                        c.revert_state(level)
                else:
                    return
