from manim import *
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


class UnitSquareTransformation(CameraAwareLinearTransformationScene):
    def __init__(self, show_inverse, matrix, **kwargs):
        self.matrix = matrix
        self.show_inverse = show_inverse
        transformed_corners = (
            (matrix[0][0], matrix[1][0]),
            (matrix[0][1], matrix[1][1]),
            (matrix[0][0] + matrix[0][1], matrix[1][0] + matrix[1][1]),
        )
        self.max_val = max(
            1,
            *(abs(coordinate) for corner in transformed_corners for coordinate in corner),
        )
        grid_bound = int(round((self.max_val + 2), None))
        plane_config = {
            "x_range": [-grid_bound*1.5, grid_bound*1.5, 1],
            "y_range": [-grid_bound, grid_bound, 1],
            "background_line_style": {
                #"stroke_color": 
                #"stroke_width": 1,
                "stroke_opacity": 1,
            },
            "axis_config": {"stroke_color": GRAY_D, "stroke_width": 2},
        
        }
        super().__init__(
            **kwargs,
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True,
            background_plane_kwargs=plane_config,
            foreground_plane_kwargs=plane_config
                )
    def construct(self):
        #Drawing the actual transformation stuff happens here
        initial_frame_height = self.camera.frame_height
        required_height = max(initial_frame_height, (self.max_val + 1.5) * 2)
        self.camera.frame.set_height(initial_frame_height)
        frame_scale = required_height / initial_frame_height

        if self.show_inverse == 1:
            inverse = InverseMatrix([row.copy() for row in self.matrix])
            print(inverse)
        else:
            inverse = 0
        unit_square = self.get_unit_square()
        self.add(unit_square)

        #text_det_A = always_redraw(lambda: Tex("Det(A)").set(width=0.7).move_to(unit_square.get_center()))

                
        self.add_transformable_mobject(unit_square)
        #self.add_background_mobject(text_det_A)
        self.apply_matrix(
            self.matrix,
            added_anims=[
                self.camera.frame.animate.set_height(required_height)
            ] if frame_scale > 1 else [],
        )
        if inverse != 0:
            self.wait(1)
            self.moving_mobjects = []
            self.apply_matrix(
                inverse,
                added_anims=[
                    self.camera.frame.animate.set_height(initial_frame_height)
                ] if frame_scale > 1 else [],
            )
        self.wait(2)
        