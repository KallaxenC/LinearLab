
def applyMatrixtoVector(matrix, vector):
    outputVector = []
    print(len(matrix))
    print(len(vector))
    for row in matrix:
        row_total = 0
        for i, element in enumerate(row):
            row_total = row_total + (element*vector[i])

        outputVector.append(row_total)
    return outputVector