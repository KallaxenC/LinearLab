from manim import *
import numpy as np

class CubeVertexTransformation(ThreeDScene):
    def construct(self):
        # 1. Setup Camera Angle
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        
        # 2. Static Background Axes
        bg_axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"stroke_color": GRAY_E, "stroke_width": 2}
        )

        # 3. Create the Main Transforming Cube (Side length = 2)
        cube = Cube(
            side_length=2, 
            fill_opacity=0.4, 
            fill_color=BLUE_D, 
            stroke_color=BLUE_A, 
            stroke_width=2
        )

        # 4. Create the Hologram Cube
        hologram_cube = cube.copy()
        hologram_cube.set_color(GRAY_C)
        hologram_cube.set_fill(opacity=0.1)
        hologram_cube.set_stroke(color=GRAY_A, width=1, opacity=0.2)

        # 5. Define Coordinates for all 8 corners manually
        # Since side_length = 2 and it's centered, coordinates are variations of +/- 1
        cube_vertices = [
            [-1, -1, -1],  # Bottom-back-left
            [ 1, -1, -1],  # Bottom-back-right
            [ 1,  1, -1],  # Bottom-front-right
            [-1,  1, -1],  # Bottom-front-left
            [-1, -1,  1],  # Top-back-left
            [ 1, -1,  1],  # Top-back-right
            [ 1,  1,  1],  # Top-front-right
            [-1,  1,  1]   # Top-front-left
        ]

        # A list of distinct high-contrast colors for all 8 vertices
        vertex_colors = [RED, GREEN, GOLD, PURPLE, ORANGE, TEAL, PINK, MAROON]
        
        # Build 3D tracking dots at each corner coordinate
        tracking_dots = VGroup()
        for index, coord in enumerate(cube_vertices):
            dot = Dot3D(
                point=coord, 
                radius=0.12, 
                color=vertex_colors[index]
            )
            tracking_dots.add(dot)

        # Render the initial setup
        self.add(bg_axes, hologram_cube, cube, tracking_dots)
        self.wait(1)

        # 6. Define the 3D Transformation Matrix
        matrix = np.array([
            [-1.0, 0.0, 0.0],  
            [0.0, -1.0, 0.0],  
            [0.0, 0.0, -1.0]   
        ])

        # 7. Linearly Animate Everything Together
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

output_name = "matrix_animation_001"

# Set up global Manim configurations programmatically before instantiation
config.preview = True                         # '-p' auto-preview flag
config.quality = "medium_quality"                # '-ql' speed optimization flag
config.output_file = "matrix_animation_001"   # '-o' file destination name

# Instantiate your imported scene object object-orientedly
scene = CubeVertexTransformation()
    
# Trigger the render pipeline natively
scene.render()