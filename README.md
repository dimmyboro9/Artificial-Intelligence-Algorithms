# Artificial-Intelligence-Algorithms
There is a repository containing my implementation of some of the algorithms of Artificial intelligence, which I did during my studies at FIT CTU.

## Projects
- [Sudoku using CSP](#Sudoku-using-CSP)
- [TSP using genetic algorithm](#TSP-using-genetic-algorithm)
- [Planning with PDDL](#Planning-with-PDDL)

## Sudoku using CSP
Let's consider the well-known `SUDOKU puzzle`, where I need to fill in the numbers 1 to 9 into a 9x9 grid in a way that satisfies various conditions regarding the uniqueness of digits. I won't detail the rules here, assuming they are known. My task is to solve the puzzle using artificial intelligence techniques, but in a way that is `as fast as possible` and guaranteed - meaning the solving algorithm `always finishes` and `provides the correct solution`. An interesting question is to implement multiple techniques and compare their performance.

This problem (Sudoku) will be solved using two approaches:

* The **CSP (Constraint Satisfaction Problem)** approach, meaning modeling Sudoku as a CSP and then performing a search on the CSP.
* Transformation into propositional satisfiability and then utilizing a known **SAT solver**.

You can find a detailed description of the project in the PDF document in the folder.

## TSP using genetic algorithm
The **Traveling Salesman Problem (TSP)** is a classic optimization problem in the field of operations research and computer science. A set of cities W is given, along with a matrix C representing the distances between pairs of cities in W. The task for the traveling salesman is to visit these cities and then return to the starting city with the minimum travel expenses, while visiting each city exactly once. 

Assume that the problem is formulated in Euclidean space, the distance matrix C between cities is symmetric, i.e., c(i,j) = c(j,i) (meaning the traveler can travel between cities in both directions), and the triangular inequality holds, c(i,k) < c(i,j) + c(j,k) for all i, j, k in W.

Using the apparatus of graph theory, the problem can be formulated as follows: let G = (V, A) be an undirected graph. V denotes the set of vertices in the graph, representing cities. A is the set of edges with non-negative weights, corresponding to the elements of the distance matrix C between cities. The task is to `find the shortest cycle` in the given graph that passes through all vertices exactly once (**Hamiltonian cycle**).

To solve this problem, I will utilize a **Genetic Algorithm**, a search heuristic inspired by the process of natural selection and evolution. Genetic algorithms are particularly effective in solving `optimization and search problems`. A genetic algorithm operates on a population of potential solutions, where each solution is represented as a set of parameters. The algorithm evolves the population over generations, applying `selection`, `crossover`, and `mutation` operators to improve the solutions' fitness. 

My tasks are:
* Implement a suitable encoding for the TSP (in the context of TSP, a common encoding is to represent a solution as a permutation of cities),
* Implement an appropriate method for algorithm initialization (to create an initial population of solutions),
* Implement the chosen selection method (to select pairs of individuals - parents),
* Implement a crossover operator (to define how parents exchange information to create new solutions),
* Implement a mutation operator (to introduce small random changes in individuals),
* Implement a repair operator (to ensure that solutions adhere to the problem constraints, this may involve fixing invalid permutations)
* Implement the visualization of the genetic algorithm's progress.

By addressing these tasks, I aim to create an effective and visually insightful genetic algorithm tailored to solve the Traveling Salesman Problem.

## Planning with PDDL
The next project addresses the task of `automated planning` using the **Planning Domain Definition Language (PDDL)** modeling language. This project concerns the topic of `warehouse logistics`.

I have a warehouse represented as a grid map, with various items stored at different locations in the warehouse. Additionally, I have a group of robots, with each robot assigned to transport one item. The task is to use the robots to transport the items to specified target locations. Typically, there are more items than robots, and the distribution of items in the warehouse is uniform. However, there are relatively few target locations for the items (typically, places where items are packaged).

I will describe this task in the PDDL language and generate a plan that leads to the solution of the problem with the fewest number of steps (`optimal plan`).

`Copyright (c) Dmytro Borovko 2023`
