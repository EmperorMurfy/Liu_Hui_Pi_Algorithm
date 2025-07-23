from manim import *
import numpy as np
import math

class liuHuiPiInequality(Scene):
    def construct(self):
        LIGHT_BLUE = "#90D5FF"
        LIGHT_GREEN = "#A0FF90"
        BRIGHT_RED = "#FF0000"
        self.camera.frame_width = 14
        radius = 2.5 
        
        
        center = ORIGIN
        circ = ParametricFunction(
            lambda u: np.array([radius * math.cos(u), radius * math.sin(u), 0]),
            t_range=[0, 2*PI],
            color=WHITE,
            stroke_width=3
        ).shift(center)   
        
        # stick with label 
        stick = Line(center, center + radius * RIGHT, color=WHITE, stroke_width=2)
        label = MathTex("r = 1", font_size=36)
        label.next_to(stick.get_end(), RIGHT, buff=0.2)  
        
        # sync stick with circle anim
        angle_tracker = ValueTracker(0)
        def update_stick(mob):
            angle = angle_tracker.get_value()
            end_point = center + radius * np.array([math.cos(angle), math.sin(angle), 0])
            mob.become(Line(center, end_point, color=WHITE, stroke_width=2))
        
        def update_label(mob):
            mob.next_to(stick.get_end(), RIGHT, buff=0.2)
        
        stick.add_updater(update_stick)
        label.add_updater(update_label)
        self.add(stick, label)
        self.play(
            Create(circ),
            angle_tracker.animate.set_value(2 * PI),   
            run_time=2
        )
        self.wait(1)

        # stop updater
        stick.remove_updater(update_stick)
        label.remove_updater(update_label)   

       
        area_label_initial = MathTex("a = \\pi r^2", font_size=36)
        area_label_initial.align_to(label, LEFT)
        self.play(Transform(label, area_label_initial), run_time=0.5)

        area_label_secondary= MathTex("a = \\pi (1)^2", font_size=36)
        area_label_secondary.align_to(label, LEFT)   
        self.play(Transform(label, area_label_secondary), run_time=0.5)
      
        self.wait(0.5)

        area_label_final = MathTex("a = \\pi", font_size=36)
        area_label_final.align_to(label, LEFT)   
        self.play(Transform(label, area_label_final), run_time=1)
        self.wait(1)
       

        # remove stick and label, move circle to left
        self.play(FadeOut(stick), FadeOut(label))  
        self.play(circ.animate.move_to(LEFT * 3), run_time=2) 

        # Generate vertices for polygons    
        gon_6_vertices = generate_polygon_vertices(center, radius, 6)
        gon_12_vertices = generate_polygon_vertices(center, radius, 12)

        # generates hexagon
        a_n = MathTex("A_{n}", font_size = 45, color = LIGHT_BLUE)
        a_n.next_to(circ, RIGHT, buff = 1)
        a_n.shift(UP * 2.25)

        a_n_second = MathTex("A_{6}", font_size = 45, color = LIGHT_BLUE)
        a_n_second.next_to(circ, RIGHT, buff = 1)
        a_n_second.shift(UP * 2.25)

        a_n_final = MathTex("A_{n}", font_size = 45, color = LIGHT_BLUE)
        a_n_final.next_to(circ, RIGHT, buff = 1)
        a_n_final.shift(UP * 2.25)

        gon_6 = Polygon(*gon_6_vertices, color=WHITE, stroke_width=2, fill_opacity=0.5, fill_color=LIGHT_BLUE)
        gon_6.shift(LEFT * 3)
        
        self.play(FadeIn(gon_6))
        self.wait(2)
        self.play(FadeIn(a_n))
        self.wait(3)
        self.play(Transform(a_n, a_n_second))
        self.wait(2)         
        self.play(FadeOut(gon_6))
        self.wait(3)
     

        # generates dodecagon
        a_2n = MathTex("A_{12}", font_size = 45, color = LIGHT_GREEN)
        a_2n.next_to(circ, RIGHT, buff = 1)
        a_2n.shift(UP * 1.25)

      #  a_2n_second = MathTex("A_{12}", font_size = 45, color = LIGHT_GREEN)
      #  a_2n_second.next_to(circ, RIGHT, buff = 1)
      #  a_2n_second.shift(UP * 1.25)

        a_2n_final = MathTex("A_{2n}", font_size = 45, color = LIGHT_GREEN)
        a_2n_final.next_to(circ, RIGHT, buff = 1)
        a_2n_final.shift(UP * 1.25)

        gon_12 = Polygon(*gon_12_vertices, color=WHITE, stroke_width=2, fill_opacity=0.5, fill_color=LIGHT_GREEN)
        gon_12.shift(LEFT * 3)

        self.play(FadeIn(gon_12), Transform(a_n, a_n_final))
        self.wait(2)
        self.play(FadeIn(a_2n))
        self.wait(3)
       # self.play(Transform(a_2n, a_2n_second))
       # self.wait(2)
        self.play(Transform(a_2n, a_2n_final))
        self.wait(3)
        
        # lower bound 
        message_1 = Text("Lower Bound", font_size=45)
        message_1.next_to(circ, RIGHT, buff = 1)

        a_2n = MathTex(r"A_{2n}", font_size=45, color=LIGHT_GREEN)
        less_than_1 = MathTex(r"<", font_size=45, color=WHITE)
        a_circle_initial = MathTex(r"A_{circle}", font_size=45, color=WHITE)
        a_circle_final = MathTex("\\pi", font_size=45, color=WHITE)

        lower_bound_initial = VGroup(a_2n, less_than_1, a_circle_initial).arrange(RIGHT, buff=0.2) 
        lower_bound_initial.next_to(circ, RIGHT, buff=1)
        lower_bound_initial.shift(DOWN * 1.25)  

        lower_bound_final = VGroup(a_2n, less_than_1, a_circle_final).arrange(RIGHT, buff=0.2) 
        lower_bound_final.next_to(circ, RIGHT, buff=1)
        lower_bound_final.shift(DOWN * 1.25)            

        self.play(FadeIn(lower_bound_initial), FadeIn(message_1))
        self.wait(2)
        self.play(Transform(lower_bound_initial, lower_bound_final))         
        self.wait(3)
        self.play(FadeOut(lower_bound_initial), FadeOut(message_1))
        self.play(FadeIn(gon_6)) # "By overlapping these two polygons..."

        # generates inital wedges
        wedge_triangles = VGroup()
        for i in range(6):
            v1 = gon_12_vertices[2 * i]         
            v2 = gon_12_vertices[2 * i + 1]    
            v3 = gon_12_vertices[(2 * i + 2) % 12]   

            # Use vertical position to determine color
            avg_y = (v1[1] + v2[1] + v3[1]) / 3
            fill_color = BRIGHT_RED
            
            wedge = Polygon(v1, v2, v3, color=WHITE, stroke_width=2, fill_opacity=1, fill_color=fill_color)
            wedge_triangles.add(wedge)

        wedge_triangles.shift(LEFT * 3)    
        d_2n = MathTex(r"D_{2n}", font_size=45, color=BRIGHT_RED)
        eq = MathTex(r"=", font_size=45, color=WHITE)
        a_2n = MathTex(r"A_{2n}", font_size=45, color=LIGHT_GREEN)
        minus = MathTex(r"-", font_size=45, color=WHITE)
        a_n = MathTex(r"A_{n}", font_size=45, color=LIGHT_BLUE)

        # Group and arrange horizontally
        d_2n = VGroup(d_2n, eq, a_2n, minus, a_n).arrange(RIGHT, buff=0.1)
        d_2n.next_to(a_n, RIGHT, buff = 1)
        d_2n.shift(UP * 2.25)
        
        self.play(AnimationGroup(
            Create(wedge_triangles),
            FadeIn(d_2n),
            lag_ratio = 0.75,
            run_time=3
        ))

        # generate new wedges by splitting the original wedges in half
        new_wedge_triangles = VGroup()
        animations = [] # for simultaneous animations

        for wedge in wedge_triangles:
            v1, v2, v3 = wedge.get_vertices()
            midpoint_base = (v1 + v3) / 2

            # creates new wedges
            new_wedge1 = Polygon(v1, midpoint_base, v2, color=WHITE, stroke_width=2, fill_opacity=1, fill_color=BRIGHT_RED)
            new_wedge2 = Polygon(midpoint_base, v3, v2, color=WHITE, stroke_width=2, fill_opacity=1, fill_color=BRIGHT_RED)
            
            # adds to group
            new_wedge_triangles.add(new_wedge1, new_wedge2)

            animations.append(Create(new_wedge1))
            animations.append(Create(new_wedge2))

       
        self.play(AnimationGroup(*animations, lag_ratio=0), run_time=2)
        self.remove(wedge_triangles)
         

        highlight_circle = Circle(radius=2.5, fill_opacity=0.5, fill_color=YELLOW)
        highlight_circle.move_to(circ.get_center())
        
        # layering priorities 
        highlight_circle.set_z_index(5) 
        circ.set_z_index(4)   
        new_wedge_triangles.set_z_index(3)
        gon_6.set_z_index(2)   
        gon_12.set_z_index(1)   
     
     
        # rotate new_wedge_triangles outwards simultaneously with alternating directions
        rotations = []

        for i, wedge in enumerate(new_wedge_triangles):
            v1, v2, v3 = wedge.get_vertices()

            edges = [(v1, v2), (v2, v3), (v3, v1)]
            hypotenuse = max(edges, key=lambda edge: np.linalg.norm(edge[1] - edge[0]))
            hypotenuse_midpoint = (hypotenuse[0] + hypotenuse[1]) / 2
            angle = -PI if i % 2 == 0 else PI
            rotations.append(Rotate(wedge, angle=angle, about_point=hypotenuse_midpoint))

        # Play the rotation animations
        self.play(AnimationGroup(*rotations, lag_ratio=0), run_time=3)
        self.wait(2)
        self.play(FadeIn(highlight_circle))  
        self.play(FadeOut(highlight_circle))
        self.wait(2)

        # upper bound
        message_2 = Text("Upper Bound", font_size=45)
        message_2.next_to(circ, RIGHT, buff = 1)

        a_2n = MathTex(r"A_{2n}", font_size=45, color=LIGHT_GREEN)
        a_circle_initial = MathTex(r"A_{circle}", font_size=45, color=WHITE)
        a_circle_final = MathTex("\\pi", font_size=45, color=WHITE)
        greater_than = MathTex(r">", font_size=45, color=WHITE)
        a_2n_plus = MathTex(r"A_{2n} +", font_size=45, color=LIGHT_GREEN)
        d_2n = MathTex(r"D_{2n}", font_size=45, color=BRIGHT_RED)

        upper_bound_initial = VGroup(a_2n_plus, d_2n, greater_than, a_circle_initial).arrange(RIGHT, buff=0.2)
        upper_bound_initial.next_to(circ, RIGHT, buff=1)
        upper_bound_initial.shift(DOWN * 1.25)  

        upper_bound_final = VGroup(a_2n_plus, d_2n, greater_than, a_circle_final).arrange(RIGHT, buff=0.2)
        upper_bound_final.next_to(circ, RIGHT, buff=1)
        upper_bound_final.shift(DOWN * 1.25)

        self.play(FadeIn(upper_bound_initial), FadeIn(message_2))
        self.wait(2)
        self.play(Transform(upper_bound_initial, upper_bound_final))         
        self.wait(3)
        self.play(FadeOut(upper_bound_initial), FadeOut(message_2))
        self.wait(3)
    
        # "Now with our lower bound and upper bound..."
        message = Text("Liu Hui's π inequality", font_size=45)
        message.next_to(circ, RIGHT, buff = 1)
        
        a_2n = MathTex(r"A_{2n}", font_size=45, color=LIGHT_GREEN)
        less_than_1 = MathTex(r"<", font_size=45, color=WHITE)
        a_circle = MathTex(r"A_{circle}", font_size=45, color=WHITE)
        less_than_2 = MathTex(r"<", font_size=45, color=WHITE)
        a_2n_plus = MathTex(r"A_{2n} +", font_size=45, color=LIGHT_GREEN)
        d_2n = MathTex(r"D_{2n}", font_size=45, color=BRIGHT_RED)

        area_of_circle_initial = VGroup(a_2n, less_than_1, a_circle, less_than_2, a_2n_plus, d_2n).arrange(RIGHT, buff=0.2)
        area_of_circle_initial.next_to(circ, RIGHT, buff=1)
        area_of_circle_initial.shift(DOWN * 1)

        a_2n_final = MathTex(r"A_{2n}", font_size=45, color=LIGHT_GREEN)
        less_than_pi = MathTex(r"< \pi <", font_size=45, color=WHITE)
        a_2n_plus_final = MathTex(r"A_{2n} +", font_size=45, color=LIGHT_GREEN)
        d_2n_final = MathTex(r"D_{2n}", font_size=45, color=BRIGHT_RED)

        area_of_circle_final = VGroup(a_2n_final, less_than_pi, a_2n_plus_final, d_2n_final).arrange(RIGHT, buff=0.2)
        area_of_circle_final.next_to(circ, RIGHT, buff=1)
        area_of_circle_final.shift(DOWN * 1)

        # Display the initial inequality
        self.play(FadeIn(message), FadeIn(area_of_circle_initial))
        self.wait(2)

        # Transform to the final inequality "we can denote..."
        self.play(Transform(area_of_circle_initial, area_of_circle_final))
        

        # End of Sequence
        self.wait(12)
        
        
        
def generate_polygon_vertices(center, radius, sides):
    return [
        center + radius * np.array([np.cos(i * 2 * PI / sides), np.sin(i * 2 * PI / sides), 0])
        for i in range(sides)
    ]