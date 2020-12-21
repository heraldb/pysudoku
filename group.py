from verbosity import Verbosity
from island import Island


class Group:
    nr = 0
    search_islands = False
    verbosity = 0
    hints = False

    def __init__(self, type, cells):
        Group.nr += 1
        self.id = Group.nr
        self.type = type
        self.cells = cells

    def __repr__(self):
        return f"{self.__str__()}: {','.join([str(v) for v in self.values()])}"

    def __str__(self):
        return f"{self.type}-{self.id}"

    def debug(self):
        cellinfo = "\n".join([c.__repr__() for c in self.cells])
        return f"{self.__str__()}: {cellinfo}"

    def id(self):
        return self.id

    def values(self):
        return [c.value for c in self.cells if c.value]

    def remaining_cells(self):
        return [c for c in self.cells if c.value == 0]

    def remaining_values(self):
        options = {v for v in range(1, 10)}
        values = self.values()
        return list(options.difference(values))

    def is_ready(self):
        ready = len(self.remaining_cells()) == 0
        if (ready and len(self.values()) != 9):
            valuestr = ','.join([str(v) for v in self.values()])
            raise Exception(f"double values in {self.__str__()} ({valuestr})")
        return ready

    def verbose(self, level, msg):
        if (level <= Group.verbosity):
            print(msg)

    def solve(self):
        Verbosity.verbose(2, f"solving {self.__str__()}")
        Verbosity.verbose(2, self.debug())
        rcells = self.remaining_cells()
        if (len(rcells) == 0):
            return

        for cell in rcells:
            for value in self.values():
                cell.drop_option(value)

        rcells = self.remaining_cells()

        if (len(rcells) == 0):
            return

        if (Group.search_islands):
            islands = Group._get_island(rcells)
            Verbosity.verbose(2,
                              f"found {len(islands)} islands in {self.__str__()}")
            for island in islands:
                cellstr = ', '.join([c.__str__() for c in island.cells])
                valstr = ', '.join([str(o) for o in island.options])
                me = self.__str__()
                Verbosity.verbose(
                    1, f"island in {me}: cells {cellstr} have values {valstr}")

                il_ids = {c.id for c in island.cells}
                for c in rcells:
                    if c.id not in il_ids:
                        for o in island.options:
                            c.drop_option(o)

        self.find_single_option_cells()

    def find_single_option_cells(self):
        # find remaining values with one candidate
        for v in self.remaining_values():
            n = 0
            candidate = None
            for cell in self.remaining_cells():
                if (cell.can(v)):
                    n += 1
                    candidate = cell
            if n > 1:
                continue
            if n == 1:
                me = self.__str__()
                cstr = candidate.__str__()
                Verbosity.verbose(
                    1, f"{me}: cell {cstr} is only option for value {v}")
                Verbosity.expect_answer(
                    f"In {self.__str__()}, which cell can have value {v}:",
                    candidate.__str__()
                )
                candidate.set(v)

    def print(self, cell):
        n = 0
        print('|', end='')
        for c in self.cells:
            if (cell and cell.id == c.id):
                print(' ? ', end='')
            else:
                c.print()
            n += 1
            if n % 3 == 0:
                print('|', end='')

    @staticmethod
    def _get_island(cells):
        n = 0
        islands = []
        for cell in cells:
            n += 1
            for max in range(n, len(cells)):
                il = [c for c in cells[n:max]]
                il.append(cell)
                options = set()
                for c in il:
                    for o in c.options:
                        options.add(o)
                if len(il) == len(options):
                    islands.append(Island(il, options))
        return islands
    # @staticmethod
    # def _get_island(cells, il_cells, il_options):
    #     print(f"1 {il_cells} 2 {il_options}")
    #     if len(il_cells) > 0 and len(il_cells) == len(il_options):
    #         return (cells, il_cells, il_options)
    #     if len(cells) == 1:
    #         return (list(), list(), set())
    #     n = 0
    #     for cell in cells:
    #         n += 1
    #         other_cells = cells[n:]
    #         new_il_cells = [c for c in il_cells]
    #         new_il_cells.append(cell)
    #         new_options = il_options.copy()
    #         for o in cell.options:
    #             new_options.add(o)
    #         return Group._get_island(other_cells, new_il_cells, new_options)
