import sys


class Verbosity:
    hints = False
    level = 0
    print = None

    @staticmethod
    def expect_answer(msg, expected_answer, cell=None):
        if Verbosity.hints:
            Verbosity.print(cell)
            print(msg)
            answer = ''
            for line in sys.stdin:
                answer = line.rstrip()
                if answer == expected_answer:
                    break
                else:
                    print(f"Maybe you should try {expected_answer}")

    @staticmethod
    def verbose(level, msg):
        if Verbosity.level >= level:
            print(msg)
