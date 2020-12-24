# PySudoku

Solving sudoku puzzles (9x9)

## Usage:

```
$ ./sudoku.py -h`
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

* uses logic to solve as much as possible.
* falls back to trial & error with backtracking if logic is insufficient. In this case multiple solutions are possible. All possible solutions will appear in the output.
* If you are trying to solve a sudoku by hand and your are stuck, you can use the 
`--hints` option to help you solving the sudoku. **Note**: the hint mode will only work as expected when the sudoku can be solved with logic.
* can also solve hyper sudokus (with four inner squares)

## Design

It should be relatively easy to add support for other types of sudoku's.
The base classes Cell, Group and Puzzle are agnostic for sudoku layout.
To support other sudoku types than the popular 9x9 type, write a variant
of Puzzle9x9 and `sudoky.py` to deal with the other type.

## To be done
* Fix hint mode for cases where trial & error with backtracking is used.
* nicer print layout for hyper sudokus.
