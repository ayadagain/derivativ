from manim import Scene, MathTex, ORIGIN, Write

class BasicEquation(Scene):
    def construct(self):
        # Define the LaTeX string for the binomial probability formula
        formula_tex = r"P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}"

        # Create a MathTex object from the LaTeX string
        formula = MathTex(formula_tex, font_size=72)

        # Set camera width to fit the formula before displaying it
        self.camera.frame_width = formula.width * 1.2

        # Animate the formula appearing and moving to the center
        self.play(Write(formula))
        self.play(formula.animate.move_to(ORIGIN))
        self.wait(2) # Hold the formula on screen for 2 seconds 