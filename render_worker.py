import json
import sys

from manim import config
from unit_square_animator import UnitSquareTransformation
from unit_cube_animator import CubeVertexTransformation
from TwoD_vector_animator import (
    TwoDVectorTransformation,
    TwoDVectorTransformationWithCoordinates,
)
from ThreeD_vector_animator import (
    ThreeDVectorTransformation,
    ThreeDVectorTransformationWithCoordinates,
)


request = json.loads(sys.argv[1])

config.preview = False
config.quality = request["quality"]
config.output_file = request["output_file"]

kind = request["kind"]
matrix = request["matrix"]
show_inverse = request["show_inverse"]
show_coordinates = request["show_coordinates"]
vectors = request["vectors"]

if kind == "unit_square":
    scene = UnitSquareTransformation(show_inverse, matrix=matrix)
elif kind == "unit_cube":
    scene = CubeVertexTransformation(
        matrix,
        show_inverse=show_inverse,
        show_coordinates=show_coordinates,
    )
elif kind == "2d_vector":
    scene_class = (
        TwoDVectorTransformationWithCoordinates
        if show_coordinates
        else TwoDVectorTransformation
    )
    scene = scene_class(show_inverse, matrix, vectors)
elif kind == "3d_vector":
    scene_class = (
        ThreeDVectorTransformationWithCoordinates
        if show_coordinates
        else ThreeDVectorTransformation
    )
    scene = scene_class(show_inverse, matrix, vectors)
else:
    raise ValueError(f"Unknown scene kind: {kind}")

scene.render()
