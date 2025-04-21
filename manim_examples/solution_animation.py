import random
# Removed numpy import
from manim import (
    # Scene, # Replaced by VoiceoverScene
    MathTex, Tex, Write, Transform, VGroup, FadeOut, UP, DOWN, LEFT, RIGHT,
    AnimationGroup, Create, Line, Dot, DashedLine, Square, BraceBetweenPoints,
    ORIGIN, YELLOW, GREEN
    # Removed 3D specifics like DEGREES, OUT, IN, BLUE, WHITE, RED
    # Removed Polyhedron, Polygon, Line3D, Dot3D, Text
)
# Added Voiceover imports
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

import math

# Helper function to create the VMN triangle diagram - RESTORED
def create_vmn_triangle(vm_len, mn_len, vn_len):
    # Define points relative to M at ORIGIN
    M = ORIGIN
    N = RIGHT * mn_len
    V = UP * vm_len

    # Create lines
    vm_line = Line(V, M, stroke_width=6)
    mn_line = Line(M, N, stroke_width=6)
    vn_line = DashedLine(V, N, stroke_width=6, color=YELLOW) # Slant height - changed color for visibility

    # Create dots and labels
    dot_M = Dot(M)
    dot_N = Dot(N)
    dot_V = Dot(V)
    label_M = MathTex("M").next_to(dot_M, DOWN*0.5 + LEFT*0.5)
    label_N = MathTex("N").next_to(dot_N, DOWN*0.5 + RIGHT*0.5)
    label_V = MathTex("V").next_to(dot_V, UP*0.5)

    # Right angle indicator
    right_angle = Square(side_length=0.4, color="white", stroke_width=3).move_to(M + RIGHT*0.2 + UP*0.2)

    # Dimension labels
    brace_vm = BraceBetweenPoints(V, M, direction=LEFT)
    label_vm = brace_vm.get_tex(f"{vm_len}").scale(0.8)
    brace_mn = BraceBetweenPoints(M, N, direction=DOWN)
    label_mn = brace_mn.get_tex(f"{mn_len:.1f}").scale(0.8)
    # label_vn = MathTex(f"{vn_len:.2f}").move_to(Line(V,N).get_center()).shift(UP*0.3 + RIGHT*0.3).scale(0.8)

    triangle = VGroup(vm_line, mn_line, vn_line, dot_M, dot_N, dot_V, label_M, label_N, label_V, right_angle)
    dimensions = VGroup(brace_vm, label_vm, brace_mn, label_mn)
    
    return VGroup(triangle, dimensions)


class WorkedExamplePyramid(VoiceoverScene): # Changed base class to VoiceoverScene
    def construct(self):
        # Set the speech service (requires internet connection)
        self.set_speech_service(GTTSService())

        # Removed set_camera_orientation

        # --- Problem Setup with Random Integers ---
        # Renamed variables slightly for clarity in triangle context
        vm_height = random.randint(5, 12)
        mn_base = random.randint(4, 10) / 2.0 # Base of the triangle
        vn_hyp_sq = vm_height**2 + mn_base**2
        vn_hyp = math.sqrt(vn_hyp_sq)

        # --- Problem Text (Focus on Triangle) ---
        # Updated problem string for triangle context using single f-string and careful escaping
        problem_string = f"""\\begin{{minipage}}{{12cm}}
\\raggedright Consider the right-angled triangle VMN, where the right angle is at M. \\\\
 The length of the vertical side VM is {vm_height} cm. \\\\
 The length of the horizontal base MN is {mn_base:.1f} cm. \\\\
 i) Use the Pythagorean Theorem to find the length of the hypotenuse VN.
\\end{{minipage}}"""
        
        # Reverted positioning and scaling for 2D
        problem_text = (Tex(problem_string) # No tex_environment needed
                       .scale(0.6)
                       .to_edge(UP, buff=0.5)
                       .set_color(YELLOW)
                       )
        # Removed add_fixed_in_frame_mobjects

        # --- Generate Diagram (Reverted to 2D Triangle) ---
        # Removed Pyramid/3D helper code
        diagram = (create_vmn_triangle(vm_height, mn_base, vn_hyp)
                   .scale(0.4) # Adjusted scale for 2D layout
                   .next_to(problem_text, DOWN, buff=0.4)
                   .to_edge(LEFT, buff=1.0)
                   )
        
        # --- Display Problem Text and Diagram First (with voiceover) ---
        with self.voiceover(text="Let's look at the problem description.") as tracker:
            self.play(Write(problem_text), run_time=tracker.duration)
        
        with self.voiceover(text="Here is a diagram of the right-angled triangle V M N.") as tracker:
            self.play(Create(diagram), run_time=tracker.duration)
        # self.wait(2) # Replaced by voiceover timing

        # --- Define Steps Data (Simplified) ---
        # Adjusted variable names and scale for 2D
        # Added voiceover text string for each step
        steps_data = [
            (Tex, f"Height VM = {vm_height}", 0.5, None, f"The height V M is {vm_height}."),
            (Tex, f"Base MN = {mn_base:.1f}", 0.5, None, f"The base M N is {mn_base:.1f}."),
            (Tex, f"Triangle VMN is right-angled at M.", 0.5, None, "The triangle V M N is right-angled at M."),
            (MathTex, f"VN^2 = VM^2 + MN^2", 0.5, None, "By the Pythagorean Theorem, V N squared equals V M squared plus M N squared."),
            (MathTex, f"VN^2 = ({vm_height})^2 + ({mn_base:.1f})^2", 0.5, None, f"Substituting the values, V N squared equals {vm_height} squared plus {mn_base:.1f} squared."),
            (MathTex, f"VN^2 = {vm_height**2} + {mn_base**2:.2f}", 0.5, None, f"Calculating the squares, we get {vm_height**2} plus {mn_base**2:.2f}."),
            (MathTex, f"VN^2 = {vn_hyp_sq:.2f}", 0.5, None, f"So, V N squared equals {vn_hyp_sq:.2f}."),
            (MathTex, f"VN = \\sqrt{{ {vn_hyp_sq:.2f} }} \\approx {vn_hyp:.2f}", 0.5, None, f"Taking the square root, V N is approximately {vn_hyp:.2f}."),
            (Tex, f"Hypotenuse VN $\\approx$ {vn_hyp:.2f} cm", 0.8, GREEN, f"Therefore, the hypotenuse V N is approximately {vn_hyp:.2f} centimeters.")
        ]

        steps_mobs = VGroup() # Group to hold all displayed steps

        # --- Position and Animate Calculation Steps (Reverted to 2D, with voiceover) ---
        # Reposition relative to the diagram's top-right corner
        anchor_point = diagram.get_corner(UP + RIGHT) + RIGHT * 0.8

        for i, (MobClass, text, scale_val, color, vo_text) in enumerate(steps_data):
            step_mob = MobClass(text).scale(scale_val)
            if color:
                step_mob.set_color(color)

            # Position the new step relative to diagram/previous step
            if i == 0:
                step_mob.move_to(anchor_point, aligned_edge=UP + LEFT)
            else:
                step_mob.next_to(steps_mobs[-1], DOWN, buff=0.25, aligned_edge=LEFT)
            
            # Removed add_fixed_in_frame_mobjects
            steps_mobs.add(step_mob)
            
            # Add voiceover for each step
            with self.voiceover(text=vo_text) as tracker:
                self.play(Write(step_mob), run_time=max(tracker.duration, 0.5)) # Ensure minimum runtime
            # self.wait(0.8) # Replaced by voiceover timing

        # Removed move_camera
        with self.voiceover(text="The calculation is complete.") as tracker:
            self.wait(tracker.duration)
        # self.wait(3) # Final pause 