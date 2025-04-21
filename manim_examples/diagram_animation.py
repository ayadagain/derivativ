from manim import Scene, Axes, BarChart, MathTex, ValueTracker, Create, FadeIn, FadeOut, ReplacementTransform, Tex, VGroup, UP, DOWN, LEFT, RIGHT, Write, YELLOW, GREEN, BLUE
import numpy as np
import math

class BinomialToPoissonConvergence(Scene):
    def construct(self):
        # --- Configuration ---
        lambda_val = 4
        n_values = [5, 10, 20, 50, 100]  # Values of n to display
        x_range_max = 15  # Max value on x-axis (adjust based on lambda)
        y_range_max = 0.3  # Max value on y-axis (adjust based on probabilities)
        animation_run_time = 1.5
        
        # --- Helper Functions for PMFs ---
        def binomial_pmf(n, p, k):
            if k < 0 or k > n:
                return 0
            if p == 0 and k == 0:
                return 1  # Convention for p=0 case
            if p == 0 and k > 0:
                return 0
            if p == 1 and k == n:
                return 1  # Convention for p=1 case
            if p == 1 and k < n:
                return 0
            if n * p > 0 and (p < 0 or p > 1):  # Check for invalid p
                return 0  # Or raise error
            try:
                binom_coeff = math.comb(n, k)
                prob = binom_coeff * (p**k) * ((1-p)**(n-k))
                return prob
            except ValueError:  # Handle potential math domain errors
                return 0

        def poisson_pmf(lam, k):
            if k < 0:
                return 0
            try:
                return (lam**k * math.exp(-lam)) / math.factorial(k)
            except (ValueError, OverflowError):  # Handle potential math domain errors
                return 0  # Or very small number

        # --- Axis Setup ---
        axes = Axes(
            x_range=[0, x_range_max + 1, 1],  # Increased range by 1 to show full x-axis
            y_range=[0, y_range_max, 0.05],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 2}},
            x_axis_config={"numbers_to_include": np.arange(0, x_range_max + 1, 3)},
            y_axis_config={"include_numbers": True, "numbers_to_include": np.arange(0, y_range_max, 0.05)},
            tips=False,
        ).to_edge(DOWN, buff=1)
        
        x_label = axes.get_x_axis_label("k", edge=DOWN, direction=DOWN)
        y_label = axes.get_y_axis_label("P(X=k)", edge=LEFT, direction=LEFT)
        # Shift the y-label further left to avoid overlap with axis numbers
        y_label.shift(LEFT * 0.7)  # Increased shift for better visibility
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
        static_labels.arrange(RIGHT, buff=1.0)  # Increased buffer for better spacing
        static_labels.next_to(title, DOWN, buff=0.6)

        # Initial display of static labels
        self.play(Write(static_labels))
        self.wait(0.5)

        # Precompute all distributions
        k_values = list(range(x_range_max + 1))
        all_binomial_probs = []
        for n in n_values:
            p = lambda_val / n
            binomial_probs = [binomial_pmf(n, p, k) for k in k_values]
            # Ensure probabilities don't exceed axis limits visually
            binomial_probs_clipped = [min(prob, y_range_max * 0.98) for prob in binomial_probs]
            all_binomial_probs.append(binomial_probs_clipped)
            
        # Precompute Poisson distribution
        poisson_probs = [poisson_pmf(lambda_val, k) for k in k_values]
        poisson_probs_clipped = [min(prob, y_range_max * 0.98) for prob in poisson_probs]

        # --- Create a custom bar color gradient function ---
        def get_bar_colors(n_index):
            # Create a gradient from blue to purple as n increases
            base_color = BLUE
            target_color = "#9370DB"  # Medium purple
            ratio = float(n_index) / float(len(n_values))
            
            # Convert hex color to RGB values
            target_r = float(int(target_color[1:3], 16)) / 255.0
            target_g = float(int(target_color[3:5], 16)) / 255.0
            target_b = float(int(target_color[5:7], 16)) / 255.0
            
            # Interpolate between base color and target color
            r = float(base_color[0]) * (1.0 - ratio) + target_r * ratio
            g = float(base_color[1]) * (1.0 - ratio) + target_g * ratio
            b = float(base_color[2]) * (1.0 - ratio) + target_b * ratio
            
            # Return as a list of RGB values
            return [[r, g, b]]  # Note the double brackets to create a list of lists

        # Initialize variables to None before the loop
        current_chart = None
        current_n_val_tex = None
        current_p_val_tex = None

        # --- Animation Loop ---
        for i, n in enumerate(n_values):
            p = lambda_val / n
            
            # Create bar chart with custom settings
            new_chart = BarChart(
                values=all_binomial_probs[i],
                y_range=[0, y_range_max, 0.05],
                x_length=axes.x_length,
                y_length=axes.y_length,
                bar_width=0.5,  # Adjusted for better visibility
                bar_fill_opacity=0.8,  # Increased opacity
                bar_colors=[get_bar_colors(i)],  # Custom color based on n index
                x_axis_config={"include_numbers": False},  # Hide x-axis numbers since we're using the main axes
                y_axis_config={"include_numbers": False},  # Hide y-axis numbers since we're using the main axes
            )
            
            # Align the chart with the axes origin
            origin_point = axes.c2p(0, 0)
            new_chart.move_to(origin_point, aligned_edge=LEFT+DOWN)
            # Fine-tune alignment
            new_chart.shift(RIGHT * 0.25)  # Adjust horizontal position
            
            # Create n and p value text Mobjects
            new_n_val_tex = MathTex(str(n), font_size=36).next_to(n_label_static, RIGHT, buff=0.1)
            new_p_val_tex = MathTex(f"{p:.3f}", font_size=36).next_to(p_label_static, RIGHT, buff=0.1)

            # Align dynamic values vertically with their static labels
            new_n_val_tex.align_to(n_label_static, DOWN)
            new_p_val_tex.align_to(p_label_static, DOWN)

            if current_chart is None:  # First iteration
                # Create and fade in the first chart and its n/p values
                self.play(
                    FadeIn(new_chart),
                    Write(new_n_val_tex),
                    Write(new_p_val_tex),
                    run_time=animation_run_time
                )
            else:  # Subsequent iterations
                # Transform previous chart and n/p values into new ones
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
        poisson_chart = BarChart(
            values=poisson_probs_clipped,
            y_range=[0, y_range_max, 0.05],
            x_length=axes.x_length,
            y_length=axes.y_length,
            bar_width=0.5,  # Consistent with other charts
            bar_fill_opacity=0.8,
            bar_colors=[YELLOW],
            x_axis_config={"include_numbers": False},  # Hide x-axis numbers since we're using the main axes
            y_axis_config={"include_numbers": False},  # Hide y-axis numbers since we're using the main axes
        )
        
        # Align the Poisson chart with the axes
        origin_point = axes.c2p(0, 0)
        poisson_chart.move_to(origin_point, aligned_edge=LEFT+DOWN)
        poisson_chart.shift(RIGHT * 0.25)  # Match the binomial chart adjustment

        # Create and position the Poisson distribution label
        poisson_dist_label = MathTex(rf"\text{{Poisson}}(\lambda={lambda_val})", font_size=36)
        poisson_dist_label.next_to(static_labels, DOWN, buff=0.4)

        # Final animation to show the Poisson distribution
        self.play(
            ReplacementTransform(current_chart, poisson_chart),
            FadeOut(VGroup(n_label_static, current_n_val_tex, p_label_static, current_p_val_tex)),
            FadeIn(poisson_dist_label),
            run_time=animation_run_time * 1.5  # Slightly longer for emphasis
        )

        # Add a conclusion text
        conclusion_text = Tex("As $n \\to \\infty$ and $p \\to 0$ with $np = \\lambda$ constant,\\\\",
                            "the Binomial distribution converges to Poisson",
                            font_size=32)
        conclusion_text.next_to(poisson_dist_label, DOWN, buff=0.5)
        self.play(Write(conclusion_text), run_time=2)

        self.wait(3)