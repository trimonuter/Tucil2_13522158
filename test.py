from manim import *

class RecursiveExample(Scene):
    def construct(self):
        # Create a text object to display the result of recursion
        # Call the recursive function
        self.recursive_function(5)

        # Display the result
        self.play(Create(Dot()))
        self.wait(1)

    def recursive_function(self, n):
        if n == 0:
            return
        else:
            self.wait(1)
            self.recursive_function(n - 1)