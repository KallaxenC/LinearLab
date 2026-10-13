from manim import *
import numpy as np

class LinearCubeTransformation(ThreeDScene):
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

        # 3. Create the Main Transforming Cube
        cube = Cube(
            side_length=2, 
            fill_opacity=0.5, 
            fill_color=BLUE_D, 
            stroke_color=BLUE_A, 
            stroke_width=2
        )

        # 4. Create the Hologram Cube
        hologram_cube = cube.copy()
        hologram_cube.set_color(GRAY_C)
        hologram_cube.set_fill(opacity=0.15)
        hologram_cube.set_stroke(color=GRAY_A, width=1, opacity=0.3)

        # Render the initial setup
        self.add(bg_axes, hologram_cube, cube)
        self.wait(1)

        # 5. Define the 3D Transformation Matrix
        matrix = np.array([
            [1.0, 0.5, 0.0],  
            [0.0, 1.0, 0.5],  
            [0.5, 0.0, 1.0]   
        ])

        # 6. Continuous, Linear Animation and Camera Movement
        # Setting rate_func=linear removes the acceleration and deceleration ease
        self.move_camera(
            phi=60 * DEGREES, 
            theta=30 * DEGREES, 
            run_time=4, 
            rate_func=linear,  # Makes the camera move at a constant speed
            added_anims=[
                cube.animate(rate_func=linear).apply_matrix(matrix)  # Makes the cube transform at a constant speed
            ]
        )
        
        self.wait(2)

output_name = "matrix_animation_001"

# Set up global Manim configurations programmatically before instantiation
config.preview = True                         # '-p' auto-preview flag
config.quality = "medium_quality"                # '-ql' speed optimization flag
config.output_file = "matrix_animation_001"   # '-o' file destination name

# Instantiate your imported scene object object-orientedly
scene = LinearCubeTransformation()
    
# Trigger the render pipeline natively
scene.render()