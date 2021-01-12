from group import Group
from cell import Cell
from verbosity import Verbosity


class Puzzle:
    def __init__(self, cells=[], groups=[]):
        self.cells = cells
        self.groups = groups
        self.solutions = []

    def remaining_groups(self):
        return [g for g in self.groups if not g.is_ready()]

    def remaining_cells(self):
        return [c for c in self.cells if c.value == 0]

    def solve(self, stack=[]):
        prev_progress = -1
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
        if len(self.remaining_groups()) == 0:
            self.solutions.append([c.value for c in self.cells])
        else:
            if Verbosity.level >= 1:
                print("gave up on logic, this is how far we got")
                self.print()
                print("Starting backtrack algoritm (level {})".format(
                    len(stack)))
            self.backtrack(stack)
            Verbosity.verbose(1, f"leaving level {len(stack)}")

    def backtrack(self, stack):
        cells = self.remaining_cells()
        cells.sort(key=lambda c: len(c.options))
        cell = cells.pop(0)  # take first cell
        Verbosity.verbose(1,
                          f"cell {cell.__str__()} has options {cell.options}")
        n = 0
        for option in cell.options:
            remaining_cells = self.remaining_cells()
            for c in remaining_cells:
                c.save_state(len(stack))
            n += 1
            stack.append(n)
            Verbosity.verbose(1,
                              "\n--- <{}>. trying {} for cell {}"
                              .format('-'.join(str(s) for s in stack),
                                      option, cell.__str__()))
            cell.set(option)
            try:
                self.solve(stack)
            except Exception as error:
                Verbosity.verbose(1,
                                  "option {} for {} did not work out ({})".
                                  format(option, cell.__str__(), error))
            else:
                if len(self.remaining_groups()) == 0:
                    if Verbosity.level >= 1:
                        print('This option worked out!')
                        Verbosity.print()
            finally:
                stack.pop()
                for c in remaining_cells:
                    c.revert_state(len(stack))
