import random
from manim import (
    Scene, MathTex, Tex, Write, Transform, VGroup, FadeOut, UP, DOWN, LEFT, RIGHT, 
    AnimationGroup, Create, Line, Dot, DashedLine, Square, BraceBetweenPoints,
    ORIGIN, YELLOW, GREEN
)
import math

# Helper function to create the VMN triangle diagram
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

class WorkedExamplePyramid(Scene):
    def construct(self):
        # Revert camera height change
        # self.camera.frame_height = 11 # Removed
        
        # --- Problem Setup with Random Integers ---
        base_side = random.randint(4, 10); base_side += base_side % 2
        height = random.randint(5, 12)
        mn_length = base_side / 2
        vn_length_sq = height**2 + mn_length**2
        vn_length = math.sqrt(vn_length_sq)

        # --- Problem Text (Yellow Color) ---
        problem_string = (
            r"\begin{minipage}{12cm}" # Start minipage
            f"\\raggedright ABCD is the square base of a right pyramid with vertex V. "
            f"The centre of the base is M.\\\\ "
            f"The sides of the square base are {base_side} cm and the vertical height is {height} cm.\\\\ "
            f"N is the midpoint of BC.\\\\ "
            f"i) Use the Pythagorean Theorem to find the distance VN."
            r"\end{minipage}" # End minipage
        )
        # Create Tex object, remove tex_environment parameter
        # Correctly indent chained method calls
        problem_text = (Tex(problem_string)
                       .scale(0.6)
                       .to_edge(UP, buff=0.5)
                       .set_color(YELLOW) # Set color
                       )

        # --- Generate Diagram (Adjust scale and position) ---
        diagram = (create_vmn_triangle(height, mn_length, vn_length)
                   .scale(0.5) # Set scale to 0.3 as requested
                   .next_to(problem_text, DOWN, buff=0.4)
                   .to_edge(LEFT, buff=1.0)
                   )
        
        # --- Display Problem Text and Diagram First ---
        self.play(Write(problem_text))
        self.play(Create(diagram))
        self.wait(2)

        # --- Define Steps Data (Simplified) ---
        steps_data = [
            (Tex, f"Height VM = {height}", 0.5, None),                  
            (Tex, f"Base MN = {mn_length:.1f}", 0.5, None), # Use MN length directly
            (Tex, f"Triangle VMN is right-angled at M.", 0.5, None),    
            (MathTex, f"VN^2 = VM^2 + MN^2", 0.5, None), # Pythagorean Theorem
            (MathTex, f"VN^2 = ({height})^2 + ({mn_length:.1f})^2", 0.85, None), # Use VM and MN values
            (MathTex, f"VN^2 = {height**2} + {mn_length**2:.2f}", 0.85, None),  
            (MathTex, f"VN^2 = {vn_length_sq:.2f}", 0.85, None),           
            (MathTex, f"VN = \\sqrt{{ {vn_length_sq:.2f} }} \\approx {vn_length:.2f}", 0.85, None), 
            (Tex, f"Slant height VN $\\approx$ {vn_length:.2f} cm", 0.9, GREEN) 
        ]

        steps_mobs = VGroup() # Group to hold all displayed steps
        
        # --- Position and Animate Calculation Steps --- 
        # Reposition relative to the now smaller diagram's top-right corner
        anchor_point = diagram.get_corner(UP + RIGHT) + RIGHT * 0.8 # Less right buffer needed now

        for i, (MobClass, text, scale_val, color) in enumerate(steps_data):
            # Apply the reduced scale
            step_mob = MobClass(text).scale(scale_val)
            if color:
                step_mob.set_color(color)

            # Position the new step
            if i == 0:
                # Align the top-left of the first step with the anchor point
                step_mob.move_to(anchor_point, aligned_edge=UP + LEFT)
            else:
                # Position below the previous step
                step_mob.next_to(steps_mobs[-1], DOWN, buff=0.25, aligned_edge=LEFT) # Restore buffer slightly
            
            steps_mobs.add(step_mob) 
            self.play(Write(step_mob), run_time=0.8)
            self.wait(0.8) 

        self.wait(3) # Final pause 