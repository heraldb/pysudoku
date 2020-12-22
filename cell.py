from verbosity import Verbosity


class Cell:
    nr = 0
    progress = 0

    def __init__(self, value):
        Cell.nr += 1
        self.id = Cell.nr
        self.value = value or 0
        self.options = {} if value else {v for v in range(1, 10)}
        self.state = None

    def __str__(self, strip=False):
        row = 1 + self.id // 9
        col = 1 + (self.id - 1) % 9
        if strip:
            return f"{col},{row}"
        return f"({col},{row})"

    def __repr__(self):
        return \
            f"<{self.__str__()}: value: {self.value}, options: {self.options}>"

    def id(self):
        return self.id

    def value(self):
        return self.value

    def options(self):
        return self.options

    def set(self, n):
        self.value = n
        Cell.progress += 1
        if not (n in self.options):
            raise Exception(
                f"value {n} not possible for cell {self.__str__()}")
        self.options = {}
        Verbosity.verbose(3, f"cell {self.__str__()} is set to value {n}")

    def can(self, n):
        return self.options and n in self.options

    def print(self):
        print(f" {self.value or '.'} ", end='')

    def drop_option(self, n):
        if (not self.value and n in self.options):
            Verbosity.verbose(3, f"cell {self.__str__()} can not be {n}")
            self.options.remove(n)
            Cell.progress += 1
            nr = len(self.options)
            if (nr == 0):
                raise Exception(
                    f"No remaining options for cell {self.__str__()}")
            if (nr == 1):
                self.set(list(self.options)[0])
                Verbosity.verbose(
                    2,
                    f"only option for cell {self.__str__()} is {self.value}")
                Verbosity.expect_answer(
                    f"Cell {self.__str__()} has only one option: ",
                    str(self.value),
                    self)

    # we need these for trackback
    def save_state(self, level):
        if not self.state:
            self.state = {}
        self.state[level] = {
            'options': self.options.copy(), 'value': self.value}

    def revert_state(self, level):
        self.options = self.state[level]['options']
        self.value = self.state[level]['value']
