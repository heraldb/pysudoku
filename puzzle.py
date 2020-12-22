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
        return [c for c in self.cells if c.value == 0]

    def solve(self, level=0):
        prev_progress = -1
        level += 1
        while Cell.progress > prev_progress:
            prev_progress = Cell.progress
            for group in self.groups:
                pre_solve = Cell.progress
                group.solve()
                if (Cell.progress > pre_solve):
                    for group in self.groups:
                        group.validate()

            if prev_progress == Cell.progress and not Group.search_islands:
                Group.search_islands = True
                prev_progress -= 1  # force extra iteration

        # if still not solved, fall back on backtrack trial and error
        if len(self.remaining_groups()) > 0:
            if Verbosity.level >= 1:
                print("gave up on logic, this is have far we got")
                self.print()
            self.backtrack(level)

    def backtrack(self, level):
        print(f"Starting backtrack algoritm (level {level})")
        cells = self.remaining_cells()
        cells.sort(key=lambda c: len(c.options))
        cell = cells.pop(0)  # take first cell

        Verbosity.verbose(1,
                          f"cell {cell.__str__()} has options {cell.options}")
        Verbosity.verbose(3,
                          "cell {} has {} options".
                          format(cell.__str__(), len(cell.options))
                          )
        for option in cell.options:
            Verbosity.verbose(1, f"trying {option} for cell {cell.__str__()}")
            remaining_cells = self.remaining_cells()
            for c in remaining_cells:
                c.save_state(level)
            cell.set(option)
            try:
                self.solve(level)
            except Exception as error:
                Verbosity.verbose(1,
                                  "option {} for {} did not work out ({})".
                                  format(option, cell.__str__(), error))
            else:
                if len(self.remaining_groups()) == 0:
                    Verbosity.print()
            finally:
                for c in remaining_cells:
                    c.revert_state(level)
