from manim import *
import numpy as np

class CubeVertexTransformation(ThreeDScene):
    def __init__(self, matrix, **kwargs):
        super().__init__(**kwargs)

        self.matrix = matrix

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
        for index, coord in enumerate(cube_vertices):
            dot = Dot3D(
                point=coord, 
                radius=0.12, 
                color=vertex_colors[index]
            )
            tracking_dots.add(dot)


        self.add(bg_axes, hologram_cube, cube, tracking_dots)
        self.wait(1)

        matrix = self.matrix

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
        
        self.wait(2)

'''
output_name = "matrix_animation_001"

# Set up global Manim configurations programmatically before instantiation
config.preview = True                         # '-p' auto-preview flag
config.quality = "medium_quality"                # '-ql' speed optimization flag
config.output_file = "matrix_animation_001"   # '-o' file destination name

# Instantiate your imported scene object object-orientedly
scene = CubeVertexTransformation()
    
# Trigger the render pipeline natively
scene.render()
'''