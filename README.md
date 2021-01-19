# PySudoku

Solving sudoku puzzles (9x9)

## Usage:

```
$ ./sudoku.py -h
usage: sudoku.py [-h] [--hints] [--hyper] [-v VERBOSE] file

Solves a sudoku 9x9 puzzle.

positional arguments:
  file                  sudoku-file

optional arguments:
  -h, --help            show this help message and exit
  --hints               interactive mode
  --hyper               hyper sudoku (with 4 inner squares)
  -v VERBOSE, --verbose VERBOSE
                        verbosity 1-4
```

## Example

create a text file with the sudoko. Use "." for empty cells e.g.:

```
$ cat s20201128
2...4.793
47.2.3185
.....5426
5.8.2.3.1
...4185.2
1.2.3.9.8
3...8265.
..53..21.
92..5.837
```

Then, solve the puzzle:

```
$ python sudoku.py s20201128
  1  2  3   4  5  6   7  8  9
+-----------------------------+
| 2  5  6 | 8  4  1 | 7  9  3 | 1
| 4  7  9 | 2  6  3 | 1  8  5 | 2
| 8  3  1 | 7  9  5 | 4  2  6 | 3
+-----------------------------+
| 5  4  8 | 6  2  9 | 3  7  1 | 4
| 7  9  3 | 4  1  8 | 5  6  2 | 5
| 1  6  2 | 5  3  7 | 9  4  8 | 6
+-----------------------------+
| 3  1  7 | 9  8  2 | 6  5  4 | 7
| 6  8  5 | 3  7  4 | 2  1  9 | 8
| 9  2  4 | 1  5  6 | 8  3  7 | 9
+-----------------------------+
```

## Features

- uses logic to solve as much as possible. If there is one solution possible,
  it will find it.
- falls back to trial & error with backtracking if logic is insufficient. In this case multiple solutions are likely. All possible solutions will appear in the output.
- Many validation are done while the sudoku is being solved. If something appears
  to be invalid, you probably should take a look at the input (any typos?).
- If you are trying to solve a sudoku by hand and your are stuck, you can use the
  `--hints` option to help you solving the sudoku. **Note**: the hint mode might
  be a bit confusing in the case multiple solutions are possible.
- can also solve hyper sudokus (with four inner squares)

## Design

The sudoku is represented by cells (representing one digit), groups (containing cells with unqiue values in this group, typically, these are the rows collumns and 3x3 squares in the regular sudoku).

It should be relatively easy to add support for other types of sudokus.
The base classes Cell, Group and Puzzle are agnostic for sudoku layout.
To support other sudoku types than the popular 9x9 type, write a variant
of Puzzle9x9 and `sudoky.py` to deal with the other type.

## Logic

The sudoku has cells. A cell can have a value or, when the value is not known, it has options for a value. When we know nothing about the value,the options can be 1 to 9. When applying rules, the set of options will reduce. When there is only one option left, we know the value of that cell. So the game of solving is to apply rules until options of all cells are reduced to one, i.o.w. until we know the value of each cell.

We apply three rules for reducing options of the cells without a value:

1. We consider a group and we check the values in that group, and drop that option from the cells withou a value. We do that for all groups and repeat that until no options are dropped. Of course, as soon as a cell has only one option, we take that as value for that cell.
2. We consider a group and try to find a subgroup ("island") of N cells which have (together) only N possible options. Then we know for sure we can drop these options from the other cells of the group. (Because if one of the options would taken by another cell, the group of N cells would only have N-1 optional values, which would make a solution impossible).
3. This one is a bit more complex, since it involves two groups. We consider groups with an intersection of more than two (empty) cells. E.g. a row and a 3x3 square. In the case that the common cells have an option for a value that is impossible for any of the other cells of one of the groups, we know that this value should be in one of the common cells. So, we can drop this option for other the cells of the other group.

## To be done

- Improvements on hint-mode for multi-solution sudokus
- nicer print layout for hyper sudokus.
