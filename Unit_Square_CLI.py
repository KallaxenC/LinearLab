from unit_square_animator import UnitSquareTransformation
from manim import config


print("Enter the a, b, c, and d values of the 2x2 matrix you want to transform the unit square by below when prompted:")
a = float(input("Enter the value of a: "))
b = float(input("Enter the value of b: "))
c = float(input("Enter the value of c: "))
d = float(input("Enter the value of d: "))
inv = input("Apply Inverse matrix after? y/n: ")
if inv.lower() == "y":
    show_inverse = 1
else:
    show_inverse = 0

matrix = [[a, b],
          [c, d]]

scene = UnitSquareTransformation(show_inverse=show_inverse, matrix=matrix)

print("Processing...")

output_name = "matrix_animation_001"

# Set up global Manim configurations programmatically before instantiation
config.preview = True                         # '-p' auto-preview flag
config.quality = "medium_quality"                # '-ql' speed optimization flag
config.output_file = "matrix_animation_001"   # '-o' file destination name

# Instantiate your imported scene object object-orientedly
scene = UnitSquareTransformation(show_inverse=show_inverse, matrix=matrix)
    
# Trigger the render pipeline natively
scene.render()