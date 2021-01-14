from group import Group
from cell import Cell
from verbosity import Verbosity
import sys


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
                    for g in self.groups:
                        g.validate()

            if Cell.progress == prev_progress:
                for g1 in self.groups:
                    for g2 in self.groups:
                        if g1 is not g2:
                            self.process_intersection(g1, g2)

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
                for g in self.groups:
                    print(g.debug())
                # sys.exit(0)
                print("Starting backtrack algoritm (level {})".format(
                    len(stack)))
            self.backtrack(stack)
            Verbosity.verbose(1, f"leaving level {len(stack)}")

    def process_intersection(self, g1, g2):
        # Find common cells of two groups and if those cells should
        # contain certain values that can not be in other cells of
        # group 2, exclude this option from other cells in group 1

        # not sure yet why this is nescessary....
        g1.solve()
        g2.solve()

        common_cells = []
        for c1 in g1.cells:
            for c2 in g2.cells:
                if c1 is c2:
                    common_cells.append(c2)

        # don't look further if there is only one cell or less
        if len([c for c in common_cells if c.value == 0]) <= 1:
            return

        common_options = set()
        other_options_g2 = set()
        common_cell_id = {c.id for c in common_cells}
        for c2 in g2.cells:
            if c2.value == 0:
                for o in c2.options:
                    if c2.id in common_cell_id:
                        common_options.add(o)
                    else:
                        other_options_g2.add(o)

        diff = common_options.difference(other_options_g2)
        if len(diff) == 0:
            return

        if Verbosity.level >= 3:
            Verbosity.print()
            print(1, 'intersection', g1.__str__(), g2.__str__(),
                  '\ndiff', diff,
                  '\ncommon cells', common_cells,
                  '\ncommon_options', common_options,
                  '\nother options_g2', other_options_g2)

        if Verbosity.level >= 2:
            print('comparing', g1.__str__(), 'and', g2.__str__())
            cellstr = ",".join([c.__str__() for c in common_cells])
            print(cellstr, 'must have value', diff,
                  'dropping this option from other cells of', g1.__str__())

        for o in diff:
            for c1 in g1.cells:
                if not c1.value and c1.id not in common_cell_id:
                    c1.drop_option(o)
        g1.solve()

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
