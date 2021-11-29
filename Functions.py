import numpy as np


# Obliczenie wszystkich możliwych permutacji sumujących do granicy
def sums(length, total_sum):
    if length == 1:
        yield (total_sum,)
    else:
        for value in range(total_sum + 1):
            for permutation in sums(length - 1, total_sum - value):
                yield (value,) + permutation


# Usunięcie permutacji, które przekraczają sumę w kolumnach
def filter(permutation, columns, layer):
    pop_idx = []
    for idx_p in range(len(permutation)):
        if (np.array((permutation[idx_p])) > np.array(columns)).any() or permutation[idx_p][layer] != 0:
            pop_idx.append(idx_p)
    for idx in pop_idx[::-1]:
        permutation.pop(idx)
    return permutation
