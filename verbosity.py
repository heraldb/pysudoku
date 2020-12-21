import sys


class Verbosity:
    hints = False
    level = 0

    @staticmethod
    def expect_answer(msg, expected_answer):
        if Verbosity.hints:
            print(msg)
            answer = ''
            while (answer != expected_answer):
                if (answer != ''):
                    print("Try again")
                answer = sys.stdin.rstrip()

    @staticmethod
    def verbose(level, msg):
        if Verbosity.level >= level:
            print(msg)
