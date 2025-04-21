from manim import Scene, Axes, BarChart, MathTex, ValueTracker, Create, FadeIn, FadeOut, ReplacementTransform, Tex, VGroup, UP, DOWN, LEFT, RIGHT, Write, YELLOW
import numpy as np
import math

class BinomialToPoissonConvergence(Scene):
    def construct(self):
        # --- Configuration ---
        lambda_val = 4
        n_values = [5, 10, 20, 50, 100] # Values of n to display
        x_range_max = 15 # Max value on x-axis (adjust based on lambda)
        y_range_max = 0.3 # Max value on y-axis (adjust based on probabilities)
        animation_run_time = 1.5

        # --- Axis Setup ---
        axes = Axes(
            x_range=[0, x_range_max, 1],
            y_range=[0, y_range_max, 0.05],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 2}},
            x_axis_config={"numbers_to_include": np.arange(0, x_range_max + 1, 3)}, # Use Axes for x-labels
            tips=False,
        ).to_edge(DOWN, buff=1)
        x_label = axes.get_x_axis_label("k", edge=DOWN, direction=DOWN)
        y_label = axes.get_y_axis_label("P(X=k)", edge=LEFT, direction=LEFT)
        # Manually shift the y-label further left to avoid overlap with axis numbers
        y_label.shift(LEFT * 0.5)
        axes_labels = VGroup(x_label, y_label)

        self.play(Create(axes), Create(axes_labels))
        self.wait(0.5)

        # --- Title ---
        title = Tex("Binomial Convergence to Poisson", font_size=48).to_edge(UP)
        self.play(Write(title))

        # --- Text Labels for n, p, lambda ---
        lambda_label = MathTex(rf"\lambda = {lambda_val}", font_size=36)
        n_label_static = MathTex("n = ", font_size=36)
        p_label_static = MathTex(r"p = \lambda / n = ", font_size=36)

        # Group static labels and position them
        static_labels = VGroup(lambda_label, n_label_static, p_label_static)
        static_labels.arrange(RIGHT, buff=0.8).next_to(title, DOWN, buff=0.6)

        # Initial display of static labels
        self.play(Write(lambda_label), Write(n_label_static), Write(p_label_static))
        self.wait(0.5)

        # --- Functions for PMFs ---
        def binomial_pmf(n, p, k):
            if k < 0 or k > n:
                return 0
            if p == 0 and k == 0:
                 return 1 # Convention for p=0 case
            if p == 0 and k > 0:
                 return 0
            if p == 1 and k == n:
                 return 1 # Convention for p=1 case
            if p == 1 and k < n:
                 return 0
            if n * p > 0 and (p < 0 or p > 1): # Check for invalid p
                return 0 # Or raise error
            try:
                binom_coeff = math.comb(n, k)
                prob = binom_coeff * (p**k) * ((1-p)**(n-k))
                return prob
            except ValueError: # Handle potential math domain errors
                return 0

        def poisson_pmf(lam, k):
            if k < 0:
                return 0
            try:
                return (lam**k * math.exp(-lam)) / math.factorial(k)
            except (ValueError, OverflowError): # Handle potential math domain errors
                 return 0 # Or very small number

        # Initialize variables to None before the loop
        current_chart = None
        current_n_val_tex = None
        current_p_val_tex = None

        # --- Simplified Animation Loop ---
        for i, n in enumerate(n_values):
            p = lambda_val / n
            k_values = list(range(x_range_max + 1))
            binomial_probs = [binomial_pmf(n, p, k) for k in k_values]

            # Ensure probabilities don't exceed axis limits visually
            binomial_probs_clipped = [min(prob, y_range_max*0.98) for prob in binomial_probs]

            new_chart = BarChart(
                values=binomial_probs_clipped,
                y_range=[0, y_range_max, 0.05],
                x_length=axes.x_length,
                y_length=axes.y_length,
                bar_width=0.4,
                bar_fill_opacity=0.7,
            ).move_to(axes.coords_to_point(0, 0), aligned_edge=LEFT+DOWN)

            # Create n and p value text Mobjects
            new_n_val_tex = MathTex(str(n), font_size=36).next_to(n_label_static, RIGHT, buff=0.1)
            new_p_val_tex = MathTex(f"{p:.3f}", font_size=36).next_to(p_label_static, RIGHT, buff=0.1)

            # Align dynamic values vertically with their static labels
            new_n_val_tex.align_to(n_label_static, DOWN)
            new_p_val_tex.align_to(p_label_static, DOWN)

            if current_chart is None: # First iteration
                # Create and fade in the first chart and its n/p values
                self.play(
                    FadeIn(new_chart),
                    Write(new_n_val_tex),
                    Write(new_p_val_tex),
                    run_time=animation_run_time
                )
            else: # Subsequent iterations
                # Transform previous chart and n/p values into new ones.
                self.play(
                    ReplacementTransform(current_chart, new_chart),
                    ReplacementTransform(current_n_val_tex, new_n_val_tex),
                    ReplacementTransform(current_p_val_tex, new_p_val_tex),
                    run_time=animation_run_time
                )

            current_chart = new_chart
            current_n_val_tex = new_n_val_tex
            current_p_val_tex = new_p_val_tex
            self.wait(1)

        # --- Final Transformation to Poisson ---
        poisson_probs = [poisson_pmf(lambda_val, k) for k in k_values]
        poisson_probs_clipped = [min(prob, y_range_max*0.98) for prob in poisson_probs]

        poisson_chart = BarChart(
            values=poisson_probs_clipped,
            y_range=[0, y_range_max, 0.05],
            x_length=axes.x_length,
            y_length=axes.y_length,
            bar_width=0.4,
            bar_fill_opacity=0.7,
            bar_colors=[YELLOW],
        ).move_to(axes.coords_to_point(0, 0), aligned_edge=LEFT+DOWN)

        poisson_dist_label = MathTex(rf"\text{{Poisson}}(\lambda={lambda_val})", font_size=36)
        poisson_dist_label.next_to(static_labels, DOWN, buff=0.4)

        self.play(
            ReplacementTransform(current_chart, poisson_chart),
            FadeOut(n_label_static),
            FadeOut(current_n_val_tex),
            FadeOut(p_label_static),
            FadeOut(current_p_val_tex),
            FadeIn(poisson_dist_label),
            run_time=animation_run_time
        )

        self.wait(3) 