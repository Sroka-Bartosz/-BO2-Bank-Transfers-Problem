# Bank Transfers Problem

## Description of the project files:
####specimen.py 
###### - representing a instance of Specimen Class the elementary part of population
```
class Specimen:
    def __init__(self, matrix: np.ndarray):
        self.size = matrix.shape[0]
        self.rows = np.sum(matrix, axis=1)
        self.cols = np.sum(matrix, axis=0)
        self.elite = False
        self.matrix = matrix
```
####population.py
###### - contains a Population class, a group of Specimen
```
class Population(specimen.Specimen):
    def __init__(self, size):
        self.specimens = []
        self.size = size
        self.best_quality = 0
```
####functions.py 
###### - all used functions
####EvolutionaryAlgorithm.py
###### - main of program
####test EA
###### - simple test of method and algorithm