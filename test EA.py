import EA


# TEST 1
def test1():
    S = EA.Specimen(3)
    rows_ = [2,
             6,
             3]
    columns_ = [2, 5, 4]
    S.initialize_matrix(columns_, rows_)


# TEST 2
def test2():
    S = EA.Specimen(6)
    columns_ = [6, 8, 9, 6, 3, 7]
    rows_ = [8, 3, 7, 9, 8, 4]
    S.initialize_matrix(columns_, rows_)
    S.display()
