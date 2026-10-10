from manim import *

class UnitSquareTransformation(LinearTransformationScene):
    def __init__(self, matrix, **kwargs):
        LinearTransformationScene.__init__(
            self,
            **kwargs,
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True,
        )
        self.matrix = matrix

    def construct(self):
        #Drawing the actual transformation stuff happens here
        unit_square = self.get_unit_square()
        self.add(unit_square)

        text_det_A = always_redraw(lambda: Tex("Det(A)").set(width=0.7).move_to(unit_square.get_center()))

                
        self.add_transformable_mobject(unit_square)
        self.add_background_mobject(text_det_A)
        self.apply_matrix(self.matrix)
                
        self.wait(2)