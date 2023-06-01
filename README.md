# Bank Transfers Problem

The project involves attempting to optimize the number of transfers between a group of individuals using an evolutionary algorithm. The project was carried out in the Operations Research laboratory with a simple GUI for handling the problem.

## Description of the project files:
#### specimen.py 
###### - representing a instance of Specimen Class the elementary part of population
```
class Specimen:
    def __init__(self, matrix: np.ndarray):
        self.number_of_rows = matrix.shape[0]
        self.number_of_cols = matrix.shape[1]
        self.rows = np.sum(matrix, axis=1)
        self.cols = np.sum(matrix, axis=0)
        self.matrix = matrix
```
#### population.py
###### - contains a Population class, a group of Specimen
```
class Population(specimen.Specimen):
    def __init__(self, size):
        self.specimens = []
        self.elite = []
        self.size = size
        self.best_quality = 0
        self.global_quality = []
```
#### functions.py 
###### - all used functions
```
- change_matrix() - function used to change matrix in elementary_mutation()
- valid_test() - test the properity of initial conditions 
- find_min() - needed in crossover
- ones() - used in crossover
- generate_initial_matrix() - function used to generate a random matrix for gui_PP
- reshape_initial_problem() - reshape matrix to square matrix for main algorithm
- delete_unexpected_rows_cols() - refactorr matrix to resulting matrix of initial shape
```
#### gui_PP.py
###### - Contains the application write in tkinter. evolutionary Algorithm () is the main function realizing the logic of the algorithm.
#### .txt file
###### Example of matrix to be exported to the application.
```
- test_matrix.txt - random matrix of size 12x12

0, 16, 7, 39, 47, 27, 22, 2, 90, 0, 46, 95
19, 0, 41, 0, 78, 8, 3, 19, 58, 10, 41, 26
61, 48, 0, 8, 53, 46, 43, 67, 28, 3, 0, 37
80, 35, 51, 0, 73, 94, 1, 0, 57, 75, 8, 13
95, 31, 1, 15, 0, 46, 94, 9, 50, 56, 0, 94
25, 36, 34, 78, 31, 0, 94, 6, 69, 0, 17, 7
11, 91, 23, 8, 25, 93, 0, 27, 34, 29, 0, 9
69, 8, 36, 23, 64, 1, 85, 0, 27, 61, 37, 0
20, 26, 15, 14, 3, 63, 6, 44, 0, 9, 32, 97
72, 38, 5, 18, 3, 10, 61, 63, 16, 0, 9, 16
84, 9, 48, 18, 6, 53, 7, 55, 67, 40, 0, 72
13, 24, 23, 8, 0, 5, 39, 0, 33, 81, 51, 0


- test_rectangle_matrix.txt - matrix of shape: 4x13

0, 2, 3, 4
1, 0, 3, 4
1, 2, 0, 4
1, 2, 3, 0
1, 2, 3, 4
1, 2, 3, 4
1, 2, 3, 4
1, 2, 3, 4
1, 2, 3, 4
1, 2, 3, 4
1, 2, 3, 4
1, 2, 3, 4
1, 2, 3, 4


- test_subproblem_matrix.txt - matrix of shape 12x12 with 3 problem shape 4x4.

0, 0, 0, 0, 0, 0, 0, 0, 3, 8, 54, 83
0, 0, 0, 0, 0, 0, 0, 0, 51, 3, 2, 33
0, 0, 0, 0, 0, 0, 0, 0, 21, 8, 1, 11
0, 0, 0, 0, 0, 0, 0, 0, 44, 3, 32, 7
0, 0, 0, 0, 0, 5, 22, 41, 0, 0, 0, 0
0, 0, 0, 0, 33, 0, 23, 2, 0, 0, 0, 0
0, 0, 0, 0, 12, 33, 0, 5, 0, 0, 0, 0
0, 0, 0, 0, 23, 5, 55, 0, 0, 0, 0, 0
23, 12, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0
5, 14, 55, 9, 0, 0, 0, 0, 0, 0, 0, 0
12, 4, 12, 1, 0, 0, 0, 0, 0, 0, 0, 0
33, 2, 2, 13, 0, 0, 0, 0, 0, 0, 0, 0
```
