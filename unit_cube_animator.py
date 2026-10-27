from manim import *
from matrix_multiplier import applyMatrixtoVector
from Gauss_Jordan_Inverter import InverseMatrix

class CubeVertexTransformation(ThreeDScene):
    def __init__(self, matrix, show_inverse=False, show_coordinates=False, **kwargs):
        super().__init__(**kwargs)

        self.matrix = matrix
        self.show_inverse = show_inverse
        self.show_coordinates = show_coordinates

    def construct(self):
        
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        
        
        bg_axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"stroke_color": GRAY_E, "stroke_width": 2}
        )

        
        cube = Cube(
            side_length=1, 
            fill_opacity=0.4, 
            fill_color=BLUE_D, 
            stroke_color=BLUE_A, 
            stroke_width=2
        )

       
        hologram_cube = cube.copy()
        hologram_cube.set_color(GRAY_C)
        hologram_cube.set_fill(opacity=0.1)
        hologram_cube.set_stroke(color=GRAY_A, width=1, opacity=0.2)

        s = 0.5 # Half of the side length
        #We need to manually define the vertices of the cube unfortunately since there's not an easy way to get them from the cube object in Manim...
        cube_vertices = [
            [-s, -s, -s],  # Bottom-back-left
            [ s, -s, -s],  # Bottom-back-right
            [ s,  s, -s],  # Bottom-front-right
            [-s,  s, -s],  # Bottom-front-left
            [-s, -s,  s],  # Top-back-left
            [ s, -s,  s],  # Top-back-right
            [ s,  s,  s],  # Top-front-right
            [-s,  s,  s]   # Top-front-left
        ]

        vertex_colors = [RED, GREEN, GOLD, PURPLE, ORANGE, TEAL, PINK, MAROON]
        
       #Track each of the vertices of the cube
        tracking_dots = VGroup()
        original_labels = VGroup()
        transformed_labels = VGroup()
        transformed_vertices = [
            applyMatrixtoVector(self.matrix, coord) for coord in cube_vertices
        ]

        for index, coord in enumerate(cube_vertices):
            dot = Dot3D(
                point=coord, 
                radius=0.12, 
                color=vertex_colors[index]
            )
            tracking_dots.add(dot)

            if self.show_coordinates:
                original_label = MathTex(
                    f"({coord[0]}, {coord[1]}, {coord[2]})",
                    font_size=16,
                    color=WHITE,
                )
                original_label.next_to(coord, UP, buff=0.1)
                original_labels.add(original_label)

                transformed_coord = transformed_vertices[index]
                transformed_label = MathTex(
                    f"({round(transformed_coord[0], 1)}, "
                    f"{round(transformed_coord[1], 1)}, "
                    f"{round(transformed_coord[2], 1)})",
                    font_size=20,
                    color=WHITE,
                )
                transformed_label.next_to(transformed_coord, UP, buff=0.1)
                transformed_labels.add(transformed_label)


        self.add(bg_axes, hologram_cube, cube, tracking_dots)
        self.wait(1)

        matrix = self.matrix
        inverse_matrix = None
        if self.show_inverse:
            inverse_matrix = InverseMatrix([
                [float(value) for value in row] for row in matrix
            ])

        self.move_camera(
            phi=60 * DEGREES, 
            theta=30 * DEGREES, 
            run_time=4, 
            rate_func=linear,
            added_anims=[
                cube.animate(rate_func=linear).apply_matrix(matrix),
                tracking_dots.animate(rate_func=linear).apply_matrix(matrix)
            ]
        )

        if self.show_coordinates:
            self.add_fixed_orientation_mobjects(
                *original_labels,
                *transformed_labels,
            )
            self.play(FadeIn(original_labels, transformed_labels), run_time=1)

        if inverse_matrix != 0 and inverse_matrix is not None:
            self.wait(2)
            if self.show_coordinates:
                self.play(FadeOut(transformed_labels), run_time=1)
            self.play(
                cube.animate(rate_func=linear).apply_matrix(inverse_matrix),
                tracking_dots.animate(rate_func=linear).apply_matrix(inverse_matrix),
                run_time=4,
            )
        
        self.wait(2)
