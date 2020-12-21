from group import Group
from cell import Cell


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
            print("Starting backtrack algoritm")
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

    @ staticmethod
    def backtrack(level):
        print('Not implemented')
