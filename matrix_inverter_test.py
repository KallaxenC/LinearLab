from math import lcm
from fractions import Fraction
a=2
b=3
c=4
d=1
e=2
f=3
g=3
h=4
i=5
u1=1
u2=0
u3=0
u4=0
u5=1
u6=0
u7=0
u8=0
u9=1

matrix = [
    [a, b, c, u1, u2, u3],
    [d, e, f, u4, u5, u6],
    [g, h, i, u7, u8, u9]
]
matrix_vals = [
    [2,3,4],
    [1,2,3],
    [3,4,5]
]
#column 1 operation
rows = 3
columns = rows*2

def lcd(*numbers):
    fractions = [Fraction(num).limit_denominator() for num in numbers]
    denominators = [frac.denominator for frac in fractions]
    multiplier = lcm(*denominators)
    return multiplier

def zero_value(pivot, p_loc, element, e_loc):
    if element != 0:
        scalarLCM = lcd(pivot, element)
        print(scalarLCM)
        scalarPivot = scalarLCM // pivot
        scalarElement = scalarLCM // element
        scalar = pivot // element
        element_index = 0
        while element_index < len(matrix)*2:
            matrix[e_loc][element_index] = (matrix[p_loc][element_index] * scalarPivot) - (matrix[e_loc][element_index] * scalarElement)
            element_index += 1

    #dfagsrg


#print(find_in_matrix(matrix, 1))
print(matrix)
zero_value(matrix[0][0], 0, matrix[1][0], 1)
print("\n", matrix[0],"\n", matrix[1],"\n", matrix[2])
zero_value(matrix[0][0], 0, matrix[2][0], 2)
print("\n", matrix[0],"\n", matrix[1],"\n", matrix[2])

zero_value(matrix[1][1], 1, matrix[0][1], 0)
print("\n", matrix[0],"\n", matrix[1],"\n", matrix[2])
zero_value(matrix[1][1], 1, matrix[2][1], 2)
print("\n", matrix[0],"\n", matrix[1],"\n", matrix[2])

zero_value(matrix[2][2], 2, matrix[0][2], 0)
print("\n", matrix[0],"\n", matrix[1],"\n", matrix[2])
zero_value(matrix[2][2], 2, matrix[1][2], 1)
print("\n", matrix[0],"\n", matrix[1],"\n", matrix[2])
#print(len(matrix))
