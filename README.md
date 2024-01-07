# Artificial-Intelligence-Algorithms
There is a repository containing my implementation of some of the algorithms of Artificial intelligence, which I did during my studies at FIT CTU.

## Projects
- [Sudoku using CSP](#Sudoku-using-CSP)

## Sudoku using CSP
Let's consider the well-known `SUDOKU puzzle`, where I need to fill in the numbers 1 to 9 into a 9x9 grid in a way that satisfies various conditions regarding the uniqueness of digits. I won't detail the rules here, assuming they are known. My task is to solve the puzzle using artificial intelligence techniques, but in a way that is `as fast as possible` and guaranteed - meaning the solving algorithm `always finishes` and `provides the correct solution`. An interesting question is to implement multiple techniques and compare their performance.

This problem (Sudoku) will be solved using two approaches:

* The **CSP (Constraint Satisfaction Problem)** approach, meaning modeling Sudoku as a CSP and then performing a search on the CSP.
* Transformation into propositional satisfiability and then utilizing a known **SAT solver**.

You can find a detailed description of the project in the PDF document in the folder.
