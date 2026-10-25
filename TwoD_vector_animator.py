from manim import *
from matrix_multiplier import applyMatrixtoVector
from Gauss_Jordan_Inverter import InverseMatrix


class CameraAwareLinearTransformationScene(LinearTransformationScene):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("camera_class", MovingCamera)
        super().__init__(*args, **kwargs)

    def get_moving_mobjects(self, *animations):
        moving_mobjects = super().get_moving_mobjects(*animations)
        camera_frames = self.camera.get_mobjects_indicating_movement()
        if any(animation.mobject in camera_frames for animation in animations):
            return [*self.mobjects, *self.foreground_mobjects]
        return moving_mobjects


class TwoDVectorTransformationWithCoordinates(CameraAwareLinearTransformationScene):
    def __init__(self, show_inverse, matrix, vectors, **kwargs):
        max_val = 3
        for vec in vectors:
            max_val = max(max_val, abs(vec[0]), abs(vec[1]))
            transformed_vec = applyMatrixtoVector(matrix, vec)
            max_val = max(max_val, abs(transformed_vec[0]), abs(transformed_vec[1]))
            grid_bound = int(round((max_val + 2), None))
            print(grid_bound)
        plane_config = {
            "x_range": [-grid_bound*1.5, grid_bound*1.5, 1],
            "y_range": [-grid_bound, grid_bound, 1],
            "background_line_style": {
                #"stroke_color": GRAY_E,
                #"stroke_width": 1,
                "stroke_opacity": 1,
            },
            "axis_config": {"stroke_color": GRAY_D, "stroke_width": 2},
        }

        super().__init__(
            include_background_plane=True,
            show_basis_vectors=True,
            show_coordinates=True,
            background_plane_kwargs=plane_config,
            foreground_plane_kwargs=plane_config,
            **kwargs,
        )   

        self.matrix = matrix
        self.vectors = vectors
        self.show_inverse = show_inverse
        self.max_val = max_val
        self.initial_max_val = max(
            [3, *(abs(component) for vec in vectors for component in vec)]
        )
        
    def construct(self):
        tracked_moving_mobjects = self.moving_mobjects.copy()
        initial_frame_height = (self.initial_max_val + 1.5) * 2
        required_height = max(initial_frame_height, (self.max_val + 1.5) * 2)
        self.camera.frame.set_height(initial_frame_height)
        frame_scale = required_height / initial_frame_height

        vector_colors = [PURPLE, ORANGE, DARK_BLUE, RED]
        ghost_group = VGroup()
        active_group = VGroup()
        label_group_ghost = VGroup()
        label_group_active = VGroup()

        movement_animations = []
        inverse_points = []
        inverse_matrix = 0
        if self.show_inverse == 1:
            inverse_matrix = InverseMatrix([
                [float(value) for value in row] for row in self.matrix
            ])

        for i, vec in enumerate(self.vectors):
            color = vector_colors[i % len(vector_colors)]
            point_3d = [vec[0],vec[1],0]
            ghost_dot = Dot(point=point_3d, radius=0.08, color=color).set_opacity(0.25)
            ghost_group.add(ghost_dot)

            #orig_text = f"({vec[0]}, {vec[1]}, {vec[2]})"
            orig_text = f"({vec[0]}, {vec[1]})"
            ghost_label = MathTex(orig_text, font_size=16*round(frame_scale/1.8,None), color=WHITE).set_opacity(0.9)
            ghost_label.next_to(ghost_dot, UP, buff=0.1)
            label_group_ghost.add(ghost_label)

            active_dot = Dot(point=point_3d, radius=0.12, color=color)
            active_group.add(active_dot)

            transformed_vec = applyMatrixtoVector(self.matrix, vec)
            trans_point_3d = [transformed_vec[0],transformed_vec[1],0]

            #trans_text = f"({round(transformed_vec[0], 1)}, {round(transformed_vec[1], 1)}, {round(transformed_vec[2], 1)})"
            trans_text = f"({round(transformed_vec[0], 1)}, {round(transformed_vec[1], 1)})"
            active_label = MathTex(trans_text, font_size=20*round(frame_scale,None), color=WHITE)
            active_label.next_to(trans_point_3d, UP, buff=0.1)
            label_group_active.add(active_label)

            movement_animations.append(active_dot.animate.move_to(trans_point_3d))

            if inverse_matrix != 0:
                inverse_vec = applyMatrixtoVector(inverse_matrix, transformed_vec)
                inverse_points.append([inverse_vec[0], inverse_vec[1], 0])
            
        self.add(ghost_group, active_group)
        self.wait(1)

        '''
        self.move_camera(
            phi=60 * DEGREES,
            theta=30 * DEGREES,
            run_time=4,
            rate_func=linear,
            added_anims=[
                ApplyMatrix(self.matrix, active_group, rate_func=linear)
            ]
        )
        '''
        self.play(FadeIn(label_group_ghost), run_time=1)
        self.wait(0.5)
        self.moving_mobjects = tracked_moving_mobjects
        self.apply_matrix(
            self.matrix,
            added_anims=[
                *movement_animations,
                *(
                    [self.camera.frame.animate.set_height(required_height)]
                    if frame_scale > 1
                    else []
                ),
            ],
            run_time=4,
            rate_func=linear,
        )

        self.play(FadeIn(label_group_active), run_time=1)
        self.wait(2)
        if inverse_matrix != 0:
            self.play(FadeOut(label_group_active), run_time=1)
            inverse_movement_animations = [
                dot.animate.move_to(point)
                for dot, point in zip(active_group, inverse_points)
            ]
            self.moving_mobjects = tracked_moving_mobjects
            self.apply_matrix(
                inverse_matrix,
                added_anims=[
                    *inverse_movement_animations,
                    *(
                        [self.camera.frame.animate.set_height(initial_frame_height)]
                        if frame_scale > 1
                        else []
                    ),
                ],
                run_time=4,
                rate_func=linear,
            )
            self.wait(2)



class TwoDVectorTransformation(CameraAwareLinearTransformationScene):
    def __init__(self, show_inverse, matrix, vectors, **kwargs):
        max_val = 3
        for vec in vectors:
            max_val = max(max_val, abs(vec[0]), abs(vec[1]))
            transformed_vec = applyMatrixtoVector(matrix, vec)
            max_val = max(max_val, abs(transformed_vec[0]), abs(transformed_vec[1]))
            grid_bound = int(round((max_val + 2), None))
            print(grid_bound)
        plane_config = {
            "x_range": [-grid_bound*1.5, grid_bound*1.5, 1],
            "y_range": [-grid_bound, grid_bound, 1],
            "background_line_style": {
                "stroke_color": GRAY_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            "axis_config": {"stroke_color": GRAY_D, "stroke_width": 2},
        }
        super().__init__(
            include_background_plane=True,
            show_basis_vectors=True,
            show_coordinates=True,
            background_plane_kwargs=plane_config,
            foreground_plane_kwargs=plane_config,
            **kwargs,
        )

        self.matrix = matrix
        self.vectors = vectors
        self.show_inverse = show_inverse
        self.max_val = max_val
        self.initial_max_val = max(
            [3, *(abs(component) for vec in vectors for component in vec)]
        )
        
    def construct(self):
        tracked_moving_mobjects = self.moving_mobjects.copy()
        initial_frame_height = (self.initial_max_val + 1.5) * 2
        required_height = max(initial_frame_height, (self.max_val + 1.5) * 2)
        self.camera.frame.set_height(initial_frame_height)
        frame_scale = required_height / initial_frame_height
        
        vector_colors = [PURPLE, ORANGE, DARK_BLUE, RED]
        ghost_group = VGroup()
        active_group = VGroup()
        inverse_ghost_group = VGroup()
        movement_animations = []
        inverse_points = []
        inverse_matrix = 0
        if self.show_inverse == 1:
            inverse_matrix = InverseMatrix([
                [float(value) for value in row] for row in self.matrix
            ])
        
        for i, vec in enumerate(self.vectors):
            color = vector_colors[i % len(vector_colors)]
            point_3d = [vec[0],vec[1],0]
            ghost_dot = Dot(point=point_3d, radius=0.08, color=color).set_opacity(0.25)
            ghost_group.add(ghost_dot)
            active_dot = Dot(point=point_3d, radius=0.12, color=color)
            active_group.add(active_dot)

            transformed_vec = applyMatrixtoVector(self.matrix, vec)
            trans_point_3d = [transformed_vec[0],transformed_vec[1],0]
            movement_animations.append(active_dot.animate.move_to(trans_point_3d))
            
            if inverse_matrix != 0:
                inverse_vec = applyMatrixtoVector(inverse_matrix, transformed_vec)
                inverse_point_3d = [inverse_vec[0],inverse_vec[1],0]
                inverse_ghost_dot = Dot(point=inverse_point_3d, radius=0.08, color=color).set_opacity(0.25)
                inverse_ghost_group.add(inverse_ghost_dot)
                inverse_points.append(inverse_point_3d)

        self.add(ghost_group, active_group)
        self.wait(1)
        self.moving_mobjects = tracked_moving_mobjects
        self.apply_matrix(
            self.matrix,
            added_anims=[
                *movement_animations,
                *(
                    [self.camera.frame.animate.set_height(required_height)]
                    if frame_scale > 1
                    else []
                ),
            ],
            run_time=4,
            rate_func=linear,
        )
        if inverse_matrix != 0:
            self.add(inverse_ghost_group)
            self.wait(2)
            inverse_movement_animations = [
                dot.animate.move_to(point)
                for dot, point in zip(active_group, inverse_points)
            ]
            self.moving_mobjects = tracked_moving_mobjects
            self.apply_matrix(
                inverse_matrix,
                added_anims=[
                    *inverse_movement_animations,
                    *(
                        [self.camera.frame.animate.set_height(initial_frame_height)]
                        if frame_scale > 1
                        else []
                    ),
                ],
                run_time=4,
                rate_func=linear,
            )
        self.wait(2)