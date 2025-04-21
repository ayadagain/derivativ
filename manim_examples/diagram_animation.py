from manim import Scene, Axes, Write

class BasicDiagram(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],  # x-axis from 0 to 10 with step 1
            y_range=[0, 5, 1],   # y-axis from 0 to 5 with step 1
            x_length=8,          # Visual length of x-axis
            y_length=4,          # Visual length of y-axis
            axis_config={"include_numbers": True}, # Add number labels
        )

        # Animate the creation of the axes
        self.play(Write(axes))
        self.wait(2) 