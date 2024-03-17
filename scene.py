# from manim import *

# class CoordinatePlaneExample(Scene):
#     def construct(self):
#         plane = NumberPlane(
#             x_range=(-5, 5, 1),
#             y_range=(-3, 3, 1),
#             axis_config={"color": BLUE},
#             # x_axis_config={"numbers_to_include": range(-5, 6)},
#             # y_axis_config={"numbers_to_include": range(-3, 4)},
#             background_line_style={"stroke_opacity": 0.5}
#         )

#         self.play(Create(plane))
#         self.wait(1)

# from manim import *

# class NumberPlaneScaled(Scene):
#     def construct(self):
#         number_plane = NumberPlane(
#             x_range=(-4, 11, 1),
#             y_range=(-3, 3, 1),
#             x_length=5,
#             y_length=2,
#         )
        
#         self.play(Create(number_plane))
from manim import *

class PointAnimation(Scene):
    def construct(self):
        # Coordinates of the points
        point1_coords = [0, 0, 0]
        point2_coords = [100, 200, 0]

        # Create points
        point1 = Dot(color=BLUE).move_to(point1_coords)
        point2 = Dot(color=BLUE).move_to(point2_coords)

        # Create line
        line = Line(point1.get_center(), point2.get_center(), color=BLUE)

        # Animation
        self.play(Create(point1), Create(point2))
        self.play(Create(line))

        self.wait(1)