from manim import *
from matrix_multiplier import applyMatrixtoVector

class ThreeDVectorTransformationWithCoordinates(ThreeDScene):
    def __init__(self, matrix, vectors, **kwargs):
        super().__init__(**kwargs)

        self.matrix = matrix
        self.vectors = vectors
        
    def construct(self):
        
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        self.axisMax = 3
        for vector in self.vectors:
            if abs(vector[0]) > self.axisMax:
                self.axisMax = abs(vector[0])
            if abs(vector[1]) > self.axisMax:
                self.axisMax = abs(vector[1])
            if abs(vector[2]) > self.axisMax:
                self.axisMax = abs(vector[2])
        
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
        label_group = VGroup()

        for i, vec in enumerate(self.vectors):
            color = vector_colors[i % len(vector_colors)]
            ghost_dot = Dot3D(point=vec, radius=0.08, color=color).set_opacity(0.25)
            ghost_group.add(ghost_dot)

            orig_text = f"({vec[0]}, {vec[1]}, {vec[2]})"
            ghost_label = MathTex(orig_text, font_size=16, color=WHITE).set_opacity(0.7)
            ghost_label.next_to(ghost_dot, UP, buff=0.1)
            label_group.add(ghost_label)

            active_dot = Dot3D(point=vec, radius=0.12, color=color)
            active_group.add(active_dot)

            transformed_vec = applyMatrixtoVector(self.matrix, vec)

            trans_text = f"({round(transformed_vec[0], 1)}, {round(transformed_vec[1], 1)}, {round(transformed_vec[2], 1)})"
            active_label = MathTex(trans_text, font_size=24, color=WHITE)
            active_label.next_to(active_dot.copy().apply_matrix(self.matrix), UP, buff=0.1)
            label_group.add(active_label)

            
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

        self.add_fixed_orientation_mobjects(*label_group)
        self.play(FadeIn(label_group), run_time=1)

        self.wait(2)



class ThreeDVectorTransformation(ThreeDScene):
    def __init__(self, matrix, vectors, **kwargs):
        super().__init__(**kwargs)

        self.matrix = matrix
        self.vectors = vectors
        
    def construct(self):
        
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        self.axisMax = 3
        for vector in self.vectors:
            if vector[0] > self.axisMax:
                self.axisMax = vector[0]
            if vector[1] > self.axisMax:
                self.axisMax = vector[1]
            if vector[2] > self.axisMax:
                self.axisMax = vector[2]
        
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
        self.wait(2)