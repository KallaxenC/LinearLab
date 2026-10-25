from manim import *
from matrix_multiplier import applyMatrixtoVector
from Gauss_Jordan_Inverter import InverseMatrix

class ThreeDVectorTransformationWithCoordinates(ThreeDScene):
    def __init__(self, show_inverse, matrix, vectors, **kwargs):
        super().__init__(**kwargs)

        self.matrix = matrix
        self.vectors = vectors
        self.show_inverse = show_inverse
        
    def construct(self):
        
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        self.axisMax = 3
        transformed_vectors = [
            applyMatrixtoVector(self.matrix, vector) for vector in self.vectors
        ]
        for vector in (*self.vectors, *transformed_vectors):
            self.axisMax = max(self.axisMax, *(abs(coordinate) for coordinate in vector))

        inverse_matrix = 0
        if self.show_inverse == 1:
            inverse_matrix = InverseMatrix([
                [float(value) for value in row] for row in self.matrix
            ])
        
        bg_axes = ThreeDAxes(
            x_range=[-self.axisMax, self.axisMax, 1],
            y_range=[-self.axisMax, self.axisMax, 1],
            z_range=[-self.axisMax, self.axisMax, 1],
            axis_config={"stroke_color": GRAY_E, "stroke_width": 2}
        )

        x_label = Tex("X").next_to(bg_axes.x_axis.get_end(), RIGHT)
        y_label = Tex("Y").next_to(bg_axes.y_axis.get_end(), UP)
        z_label = Tex("Z").next_to(bg_axes.z_axis.get_end(), OUT)
        self.add(bg_axes)
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
        
        vector_colors = [PURPLE, ORANGE, DARK_BLUE, RED]
        ghost_group = VGroup()
        active_group = VGroup()
        original_label_group = VGroup()
        transformed_label_group = VGroup()

        for i, vec in enumerate(self.vectors):
            color = vector_colors[i % len(vector_colors)]
            ghost_dot = Dot3D(point=vec, radius=0.08, color=color).set_opacity(0.25)
            ghost_group.add(ghost_dot)

            orig_text = f"({vec[0]}, {vec[1]}, {vec[2]})"
            ghost_label = MathTex(orig_text, font_size=16, color=WHITE).set_opacity(0.7)
            ghost_label.next_to(ghost_dot, UP, buff=0.1)
            original_label_group.add(ghost_label)

            active_dot = Dot3D(point=vec, radius=0.12, color=color)
            active_group.add(active_dot)

            transformed_vec = transformed_vectors[i]

            trans_text = f"({round(transformed_vec[0], 1)}, {round(transformed_vec[1], 1)}, {round(transformed_vec[2], 1)})"
            active_label = MathTex(trans_text, font_size=24, color=WHITE)
            active_label.next_to(active_dot.copy().apply_matrix(self.matrix), UP, buff=0.1)
            transformed_label_group.add(active_label)

        self.add(ghost_group, active_group)
        self.wait(1)
        
        self.move_camera(
            phi=60 * DEGREES,
            theta=30 * DEGREES,
            run_time=4,
            rate_func=linear,
            added_anims=[
                ApplyMatrix(self.matrix, active_group, rate_func=linear)
            ]
        )

        self.add_fixed_orientation_mobjects(*original_label_group, *transformed_label_group)
        self.play(FadeIn(original_label_group, transformed_label_group), run_time=1)

        self.wait(2)
        if inverse_matrix != 0:
            self.play(FadeOut(transformed_label_group), run_time=1)
            self.play(
                ApplyMatrix(inverse_matrix, active_group, rate_func=linear),
                run_time=4,
            )
            self.wait(2)



class ThreeDVectorTransformation(ThreeDScene):
    def __init__(self, show_inverse, matrix, vectors, **kwargs):
        super().__init__(**kwargs)

        self.matrix = matrix
        self.vectors = vectors
        self.show_inverse = show_inverse
        
    def construct(self):
        
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        self.axisMax = 3
        transformed_vectors = [
            applyMatrixtoVector(self.matrix, vector) for vector in self.vectors
        ]
        for vector in (*self.vectors, *transformed_vectors):
            self.axisMax = max(self.axisMax, *(abs(coordinate) for coordinate in vector))

        inverse_matrix = 0
        if self.show_inverse == 1:
            inverse_matrix = InverseMatrix([
                [float(value) for value in row] for row in self.matrix
            ])
        
        bg_axes = ThreeDAxes(
            x_range=[-self.axisMax, self.axisMax, 1],
            y_range=[-self.axisMax, self.axisMax, 1],
            z_range=[-self.axisMax, self.axisMax, 1],
            axis_config={"stroke_color": GRAY_E, "stroke_width": 2}
        )

        x_label = Tex("X").next_to(bg_axes.x_axis.get_end(), RIGHT)
        y_label = Tex("Y").next_to(bg_axes.y_axis.get_end(), UP)
        z_label = Tex("Z").next_to(bg_axes.z_axis.get_end(), OUT)
        self.add(bg_axes)
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
        
        vector_colors = [PURPLE, ORANGE, DARK_BLUE, RED]
        ghost_group = VGroup()
        active_group = VGroup()
        
        for i, vec in enumerate(self.vectors):
            color = vector_colors[i % len(vector_colors)]
            ghost_dot = Dot3D(point=vec, radius=0.08, color=color).set_opacity(0.25)
            ghost_group.add(ghost_dot)
            active_dot = Dot3D(point=vec, radius=0.12, color=color)
            active_group.add(active_dot)
            
        self.add(ghost_group, active_group)
        self.wait(1)
        
        self.move_camera(
            phi=60 * DEGREES,
            theta=30 * DEGREES,
            run_time=4,
            rate_func=linear,
            added_anims=[
                ApplyMatrix(self.matrix, active_group, rate_func=linear)
            ]
        )
        if inverse_matrix != 0:
            self.wait(2)
            self.play(
                ApplyMatrix(inverse_matrix, active_group, rate_func=linear),
                run_time=4,
            )
        self.wait(2)