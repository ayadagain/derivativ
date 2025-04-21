import random
import numpy as np
from manim import (
    ThreeDScene, MathTex, Tex, Write, Transform, VGroup, FadeOut, UP, DOWN, LEFT, RIGHT,
    AnimationGroup, Create, Line, Dot, DashedLine, Square, BraceBetweenPoints,
    ORIGIN, YELLOW, GREEN, BLUE, WHITE, RED, DEGREES, OUT, IN,
    Polyhedron, Polygon, Line3D, Dot3D, Text # Changed Text3D back to Text
)
import math

# Helper function to create the VMN triangle diagram - REMOVED

# Removed create_vmn_triangle function

class WorkedExamplePyramid(ThreeDScene): # Changed Scene to ThreeDScene
    def construct(self):
        # Set camera orientation for 3D view
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, distance=8)

        # --- Problem Setup with Random Integers ---
        base_side = random.randint(4, 10); base_side += base_side % 2
        height = random.randint(5, 12)
        mn_length = base_side / 2.0 # Ensure float division
        vn_length_sq = height**2 + mn_length**2
        vn_length = math.sqrt(vn_length_sq)

        # --- Problem Text (Yellow Color) ---
        # Corrected backslash escaping for minipage and newlines using a single f-string
        problem_string = f"""\\begin{{minipage}}{{12cm}}
\\raggedright ABCD is the square base of a right pyramid with vertex V. \\
 The centre of the base is M.\\
 The sides of the square base are {base_side} cm and the vertical height is {height} cm.\\
 N is the midpoint of BC.\\
 i) Use the Pythagorean Theorem to find the distance VN.
\\end{{minipage}}"""

        problem_text = (Tex(problem_string) # No tex_environment needed as it's in the string
                       .scale(0.5) # Smaller scale for 3D scene
                       .to_corner(UP + LEFT, buff=0.5) # Position top-left
                       .set_color(YELLOW)
                       )
        self.add_fixed_in_frame_mobjects(problem_text)

        # --- Define Pyramid Geometry ---
        hs = base_side / 2.0 # half side
        vertex_coords = [
            [-hs, -hs, 0], # A: 0
            [ hs, -hs, 0], # B: 1
            [ hs,  hs, 0], # C: 2
            [-hs,  hs, 0], # D: 3
            [  0,   0, height]  # V: 4
        ]
        faces_list = [
            [0, 1, 4], # VAB
            [1, 2, 4], # VBC
            [2, 3, 4], # VCD
            [3, 0, 4], # VDA
            [0, 1, 2, 3]  # Base ABCD
        ]
        # Define points M and N
        M_coord = np.array([0, 0, 0])
        # Corrected N definition assuming B=(hs, -hs, 0), C=(hs, hs, 0)
        # Midpoint N should be ( (hs+hs)/2 , (-hs+hs)/2, (0+0)/2 ) = (hs, 0, 0)
        N_coord = np.array([hs, 0, 0])
        V_coord = np.array([0, 0, height])

        # --- Create Polyhedron (Pyramid) ---
        pyramid = Polyhedron(
            vertex_coords,
            faces_list,
            faces_config={"fill_opacity": 0.5, "fill_color": BLUE, "stroke_width": 1, "stroke_color": WHITE},
            graph_config={"edge_config": {"stroke_color": WHITE, "stroke_width": 2}, # Increased width slightly
                          "vertex_config": {"fill_color": WHITE, "radius": 0.05} # Made vertices small dots
                         }
        ).scale(0.5) # Scale the pyramid down

        # --- Create Helper Lines and Labels for VMN Triangle ---
        vm_line = Line3D(V_coord, M_coord, color=RED, thickness=0.02)
        mn_line = Line3D(M_coord, N_coord, color=RED, thickness=0.02)
        vn_line = Line3D(V_coord, N_coord, color=YELLOW, thickness=0.02)

        dot_M = Dot3D(M_coord, color=RED)
        dot_N = Dot3D(N_coord, color=RED)
        dot_V = Dot3D(V_coord, color=RED)

        # Use Text for labels in 3D space - Increased font size and adjusted positioning
        label_M = Text("M", font_size=24).next_to(dot_M, OUT * 0.5 + LEFT * 0.5) # Move slightly out from screen
        label_N = Text("N", font_size=24).next_to(dot_N, OUT * 0.5 + RIGHT * 0.5)
        label_V = Text("V", font_size=24).next_to(dot_V, UP * 0.8) # Move further UP

        # Group the helper elements - Removed scaling from the group
        vmn_helpers = VGroup(vm_line, mn_line, vn_line, dot_M, dot_N, dot_V, label_M, label_N, label_V) # .scale(0.5) REMOVED

        # --- Position the Pyramid and Helpers ---
        # Note: Pyramid is scaled 0.5, helpers are now unscaled but use original coords
        pyramid_group = VGroup(pyramid, vmn_helpers).move_to(ORIGIN + DOWN*0.5)

        # --- Display Problem Text and Diagram First ---
        self.play(Write(problem_text))
        self.play(Create(pyramid), Create(vmn_helpers)) # Create pyramid and helpers
        self.wait(2)

        # --- Define Steps Data (Simplified) ---
        steps_data = [
            (Tex, f"Height VM = {height}", 0.4, None), # Reduced scale for 3D
            (Tex, f"Base MN = {mn_length:.1f}", 0.4, None),
            (Tex, f"Triangle VMN is right-angled at M.", 0.4, None),
            (MathTex, f"VN^2 = VM^2 + MN^2", 0.4, None),
            (MathTex, f"VN^2 = ({height})^2 + ({mn_length:.1f})^2", 0.5, None), # Slightly larger scale for math
            (MathTex, f"VN^2 = {height**2} + {mn_length**2:.2f}", 0.5, None),
            (MathTex, f"VN^2 = {vn_length_sq:.2f}", 0.5, None),
            (MathTex, f"VN = \\sqrt{{ {vn_length_sq:.2f} }} \\approx {vn_length:.2f}", 0.5, None),
            (Tex, f"Slant height VN $\\approx$ {vn_length:.2f} cm", 0.5, GREEN)
        ]

        steps_mobs = VGroup() # Group to hold all displayed steps

        # --- Position and Animate Calculation Steps ---
        # Position steps relative to the screen corners for fixed-in-frame mobjects
        # anchor_point = self.camera.frame.get_corner(UP + RIGHT) + LEFT * 0.5 + DOWN * 1.5 # REMOVED

        for i, (MobClass, text, scale_val, color) in enumerate(steps_data):
            step_mob = MobClass(text).scale(scale_val)
            if color:
                step_mob.set_color(color)

            # Position the new step, fixed in frame
            if i == 0:
                # step_mob.move_to(anchor_point, aligned_edge=UP + RIGHT) # REMOVED
                step_mob.to_corner(UP + RIGHT, buff=0.5) # Position first step to corner
            else:
                step_mob.next_to(steps_mobs[-1], DOWN, buff=0.15, aligned_edge=RIGHT) # Tighter buffer
            
            self.add_fixed_in_frame_mobjects(step_mob)
            steps_mobs.add(step_mob)
            self.play(Write(step_mob), run_time=0.6) # Faster animation
            self.wait(0.6)

        # Add rotation for better 3D view
        self.move_camera(phi=75 * DEGREES, theta=135 * DEGREES, run_time=3)
        self.wait(3) # Final pause 