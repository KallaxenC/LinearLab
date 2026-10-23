from manim import *
from Gauss_Jordan_Inverter import InverseMatrix

class UnitSquareTransformation(LinearTransformationScene):
    def __init__(self, show_inverse, matrix, **kwargs):
        LinearTransformationScene.__init__(
            self,
            **kwargs,
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True,
        )
        self.matrix = matrix
        self.show_inverse = show_inverse
        
    def construct(self):
        #Drawing the actual transformation stuff happens here
        if self.show_inverse == 1:
            inverse = InverseMatrix([row.copy() for row in self.matrix])
            print(inverse)
        unit_square = self.get_unit_square()
        self.add(unit_square)

        text_det_A = always_redraw(lambda: Tex("Det(A)").set(width=0.7).move_to(unit_square.get_center()))

                
        self.add_transformable_mobject(unit_square)
        self.add_background_mobject(text_det_A)
        self.apply_matrix(self.matrix)
        if inverse != 0:
            self.wait(1)
            self.moving_mobjects = []
            self.apply_matrix(inverse)
        self.wait(2)
        