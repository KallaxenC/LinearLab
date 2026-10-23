from math import lcm

#Test data below by uncommenting this if you like
'''
a=1
b=2
c=3
d=0
e=1
f=4
g=5
h=6
i=0

matrix = [
    [a, b, c],
    [d, e, f],
    [g, h, i]
]
'''

def add_identity_matrix(matrix):
    rows = len(matrix)
    for i in range(rows):
        for x in range(rows):
            if i == x:
                matrix[i].append(1)
            else:
                matrix[i].append(0)

def calculateScalars(pivot, element):
    if element == 0:
        return 0,1
        #if the element is 0 then we dont even need to do anything which is nice. This has alert code 0,1
    if pivot == 0:
        return 1,0
        #IF the pivot is 0 then we must swap rows in the matrix which is kinda annoying. This has alert code 1,0
        
    if pivot.is_integer() and element.is_integer():
        scalar = lcm(int(pivot), int(element))
        scalarPivot = scalar // pivot
        scalarElement = scalar // element
        return scalarPivot, scalarElement
    else:
        scalarPivot = 1/pivot
        scalarElement = 1/element
        return scalarPivot, scalarElement

def zero_value(matrix, pivot, p_loc, element, e_loc):
    scalars = calculateScalars(pivot, element)
    if scalars[0] == 0:
        return 1
    if scalars[1] == 0:
        loc_value = -1
        for i in range (len(matrix)):
            if i != p_loc and matrix[i][p_loc] != 0:
                loc_value = i
        if loc_value == -1:
            return 0

        #Annoyingly we must swap pivot's row with another due to this pivot being 0.
            
        for i in range(len(matrix)*2):
            temp_p = matrix[p_loc][i]
            #loc_e_val means location element value
            temp_loc_e_val = matrix[loc_value][i]
            matrix[p_loc][i] = temp_loc_e_val
            matrix[loc_value][i] = temp_p
        #Update the pivot and element values (element only if needed) after we've done faff with them
        pivot = matrix[p_loc][p_loc]
        if loc_value == e_loc:
            element = matrix[e_loc][p_loc]
        
        scalars = calculateScalars(pivot, element)
    
    scalarPivot = scalars[0]
    scalarElement = scalars[1]
    element_index = 0
    while element_index < len(matrix)*2:
        matrix[e_loc][element_index] = (matrix[p_loc][element_index] * scalarPivot) - (matrix[e_loc][element_index] * scalarElement)
        element_index += 1

#Zero all the non pivot values on the LHS matrix (inefficient but it works rn)
def InverseMatrix(matrix):
    rows = len(matrix)
    add_identity_matrix(matrix)
    for i in range(rows):
        pivot_location = i
        for x in range(rows-1):
            position = pivot_location + x + 1
            if position > rows-1:
                continue
            non_singular = zero_value(matrix, matrix[pivot_location][pivot_location], pivot_location, matrix[position][pivot_location], position)
            if non_singular == 0:
                return 0

    det = matrix[0][0]
    for i in range(len(matrix)-1):
        det = det *matrix[i+1][i+1]
    if det == 0:
        return 0

    for i in range(rows):
        pivot_location = i
        for x in range(rows-1):
            position = pivot_location - x - 1
            if position < 0:
                continue
            non_singular = zero_value(matrix, matrix[pivot_location][pivot_location], pivot_location, matrix[position][pivot_location], position)
            if non_singular == 0:
                return 0

    #Operate on each non-1 pivot's row to turn the pivots into 1s. (again inefficient as it requires 2 for loops bruh)
    for i in range(rows):
        pivot_location = i
        if matrix[pivot_location][pivot_location] != 1:
            scalar = 1 / matrix[pivot_location][pivot_location] 
            for index, element in enumerate(matrix[pivot_location]):
                matrix[pivot_location][index] = element * scalar

    #Finally we clearly need to remove the identity matrix and leave just the inverse matrix
    inverse_matrix = []
    for row in matrix:
        inverse_row = []
        for index, element in enumerate(row):
            if index >= rows:
                inverse_row.append(element)
        inverse_matrix.append(inverse_row)
    return inverse_matrix

