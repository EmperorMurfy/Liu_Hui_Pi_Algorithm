from manim import *
import numpy as np
import math

class estimatingPi(Scene):
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

        # replace radius label with area label
        area_label_initial = MathTex("a = \\pi r^2", font_size=36)
        area_label_initial.align_to(label, LEFT)
        self.play(Transform(label, area_label_initial), run_time=0.5)

        area_label_secondary= MathTex("a = \\pi (1)^2", font_size=36)
        area_label_secondary.align_to(label, LEFT)   
        self.play(Transform(label, area_label_secondary), run_time=0.5)
      
        self.wait(0.5)

        area_label_final = MathTex("a = \\pi", font_size=36)
        area_label_final.align_to(label, LEFT)  # Ensure left alignment is maintained
        self.play(Transform(label, area_label_final), run_time=1)
        self.wait(1)

        # remove stick and label, move circle to left
        self.play(FadeOut(stick), FadeOut(label))  
        self.play(circ.animate.move_to(LEFT * 3), run_time=2) 

        # Generate vertices for polygons    
        gon_6_vertices = generate_polygon_vertices(center, radius, 6)
        gon_12_vertices = generate_polygon_vertices(center, radius, 12)

        gon_6 = Polygon(*gon_6_vertices, color=WHITE, stroke_width=2, fill_opacity=0.5, fill_color=LIGHT_BLUE)
        gon_6.shift(LEFT * 3)
        
        
        # ABOVE IS REDUDANT CODE TO SETUP SCENE, BELOW IS ACTUAL ANIMATION
        # area of polygon with n sides
        a_n_area_initial = MathTex(r"A_n = \frac{\text{apothem} \cdot \text{n} \cdot \text{side length}}{2}", font_size=36, color=LIGHT_BLUE)
        a_n_area_initial.next_to(circ, RIGHT, buff = 1)
        a_n_area_initial.shift(UP * 2.25)

        # area of polygon with 2n sides
        a_2n_area_initial = MathTex(r"A_2n = \frac{\text{apothem} \cdot \text{2n} \cdot \text{side length}}{2}", font_size=36, color=LIGHT_GREEN)
        a_2n_area_initial.next_to(circ, RIGHT, buff = 1)
        a_2n_area_initial.shift(UP * 1.25)

        # liu hui's pi inequality
        a_2n_initial = MathTex(r"A_{2n}", font_size=45, color=LIGHT_GREEN)
        less_than_pi = MathTex(r"< \pi <", font_size=45, color=WHITE)
        a_2n_plus_initial = MathTex(r"A_{2n} +", font_size=45, color=LIGHT_GREEN)
        d_2n_initial = MathTex(r"D_{2n}", font_size=45, color=BRIGHT_RED)

        area_of_circle_initial = VGroup(a_2n_initial, less_than_pi, a_2n_plus_initial, d_2n_initial).arrange(RIGHT, buff=0.2)
        area_of_circle_initial.next_to(circ, RIGHT, buff=1)
        
        # d2n formula
        d_2n = MathTex(r"D_{2n}", font_size=45, color=BRIGHT_RED)
        eq = MathTex(r"=", font_size=45, color=WHITE)
        a_2n = MathTex(r"A_{2n}", font_size=45, color=LIGHT_GREEN)
        minus = MathTex(r"-", font_size=45, color=WHITE)
        a_n = MathTex(r"A_{n}", font_size=45, color=LIGHT_BLUE)
        
        d_2n = VGroup(d_2n, eq, a_2n, minus, a_n).arrange(RIGHT, buff=0.1)
        d_2n.next_to(circ, RIGHT, buff = 1)
        d_2n.shift(DOWN * 1.25)
        
        self.play(FadeIn(gon_6), FadeIn(area_of_circle_initial), FadeIn(d_2n), FadeIn(a_n_area_initial))
        self.wait(3)
        
        a_n_side_length = MathTex(r"\text{side length} = 1", font_size=36, color=LIGHT_BLUE)
        a_n_side_length.next_to(circ, RIGHT, buff = 1)
        a_n_side_length.shift(UP * 1.45)

        a_n_n = MathTex(r"\text{n} = 6", font_size=36, color=LIGHT_BLUE)
        a_n_n.next_to(circ, RIGHT, buff = 1)
        a_n_n.shift(UP * 0.85)

        self.play(FadeIn(a_n_side_length), FadeIn(a_n_n))
        self.wait(2)

        a_n_area_second= MathTex(r"A_n = \frac{\text{apothem} \cdot \text{6} \cdot \text{1}}{2}", font_size=36, color=LIGHT_BLUE)
        a_n_area_second.next_to(circ, RIGHT, buff = 1)
        a_n_area_second.shift(UP * 2.25)

        self.play(AnimationGroup(
            Transform(a_n_area_initial, a_n_area_second, run_time=1),
            AnimationGroup(
                FadeOut(a_n_side_length),
                FadeOut(a_n_n),
                lag_ratio=0
            ),
            lag_ratio=0.5
        ))

        self.wait(2)

        a_n_apothem_initial = MathTex(r"\text{apothem} = height", font_size=36, color=LIGHT_BLUE)
        a_n_apothem_initial.next_to(circ, RIGHT, buff = 1)
        a_n_apothem_initial.shift(UP * 1.45)

        self.play(FadeIn(a_n_apothem_initial))
        self.wait(2)

        a_n_apothem_second = MathTex(r"\text{apothem} = \frac{\sqrt{3}}{2}", font_size=36, color=LIGHT_BLUE)
        a_n_apothem_second.next_to(circ, RIGHT, buff = 1)
        a_n_apothem_second.shift(UP * 1.45)

        self.play(AnimationGroup(
            Transform(a_n_apothem_initial, a_n_apothem_second),
            FadeOut(a_n_apothem_initial),
            lag_ratio=0.5
        ))
        self.wait(2)

        a_n_area_third = MathTex(r"A_n = \frac{\sqrt{3}}{2} \cdot 6 \cdot \frac{1}{2}", font_size=36, color=LIGHT_BLUE)
        a_n_area_third.next_to(circ, RIGHT, buff = 1)
        a_n_area_third.shift(UP * 2.25)

        self.play(Transform(a_n_area_initial, a_n_area_third))
        self.wait(2)

        a_n_area_final = MathTex(r"A_n = 2.59\overline{8}", font_size=36, color=LIGHT_BLUE)
        a_n_area_final.next_to(circ, RIGHT, buff = 1)
        a_n_area_final.shift(UP * 2.25)

        self.play(Transform(a_n_area_initial, a_n_area_final))
        self.wait(3)

        # "In the same way, we can apply this process to a dodecagon
         # area of polygon with 2n sides

        gon_12 = Polygon(*gon_12_vertices, color=WHITE, stroke_width=2, fill_opacity=0.5, fill_color=LIGHT_GREEN)
        gon_12.shift(LEFT * 3)

        gon_6.set_z_index(2)   
        gon_12.set_z_index(1) 

        self.play(FadeIn(gon_12))
        self.wait(2)

        a_2n_area_second = MathTex(
            r"A_{2n} = \frac{0.96\overline{5} \cdot 12 \cdot 0.51\overline{7}}{2}",
            font_size=36,
            color=LIGHT_GREEN
        )
        a_2n_area_second.next_to(circ, RIGHT, buff = 1)
        a_2n_area_second.shift(UP * 1.25)

        self.play(Transform(a_2n_area_initial, a_2n_area_second))
        self.wait(2)

        a_2n_area_final = MathTex(r"A_2n = 3", font_size=36, color=LIGHT_GREEN)
        a_2n_area_final.next_to(circ, RIGHT, buff = 1)
        a_2n_area_final.shift(UP * 1.25)

        self.play(Transform(a_2n_area_initial, a_2n_area_final))
        self.wait(3)

        # wedges

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

         # layering priorities 
       
        circ.set_z_index(4)   
        new_wedge_triangles.set_z_index(3)
        gon_6.set_z_index(2)
        gon_12.set_z_index(1)   
           
        self.wait(2)
        self.play(
            Transform(
                a_2n_initial,
                MathTex(r"3", font_size=45, color=LIGHT_GREEN).move_to(a_2n_initial.get_center())
            ),
            Transform(
                a_2n,
                MathTex(r"3", font_size=45, color=LIGHT_GREEN).move_to(a_2n.get_center())
            ),
            Transform(
                a_2n_plus_initial,
                MathTex(r"3 + ", font_size=45, color=LIGHT_GREEN).move_to(a_2n_plus_initial.get_center())
            ),
            Transform(
                a_n,
                MathTex(r"2.59\overline{8}", font_size=45, color=LIGHT_BLUE)
                .next_to(minus, RIGHT, buff=0.3)  # Adjust spacing to avoid overlap
            )
        )

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
        d_2n_final = MathTex(r"D_{2n} = 0.40\overline{1}", font_size=45, color=BRIGHT_RED)
        d_2n_final.next_to(circ, RIGHT, buff = 1)
        d_2n_final.shift(DOWN * 1.25)

        self.play(Transform(d_2n, d_2n_final), FadeOut(a_2n_area_initial), FadeOut(a_n_area_initial))
        self.wait(2)

        area_of_circle_final = MathTex(
            r"3 \,<\, \pi \,<\, 3.40\overline{1}",
            font_size=45,
            color=WHITE
        )
        area_of_circle_final.next_to(circ, RIGHT, buff=1)

        self.play(Transform(area_of_circle_initial, area_of_circle_final), FadeOut(d_2n))
        self.wait(3)



        




 
        
def generate_polygon_vertices(center, radius, sides):
    return [
        center + radius * np.array([np.cos(i * 2 * PI / sides), np.sin(i * 2 * PI / sides), 0])
        for i in range(sides)
    ]

class apothemFormula(Scene):
    def construct(self):
        self.camera.frame_width = 14

        height_initial = MathTex(r"\text{height} = \sqrt{r^2 - \left(\frac{\text{side length}}{2}\right)^2}", font_size=45, color=WHITE)
        self.play(FadeIn(height_initial))
        self.wait(2)    
        height_second = MathTex(r"\text{height} = \sqrt{1^2 - \left(\frac{1}{2}\right)^2}", font_size=45, color=WHITE)
        self.play(Transform(height_initial, height_second))
        self.wait(2)    
        height_final = MathTex(r"\text{height} = \frac{\sqrt{3}}{2}", font_size=45, color=WHITE)
        self.play(Transform(height_initial, height_final))
        self.wait(2)  

class dodecagonProcess(Scene):
    def construct(self):
        self.camera.frame_width = 14

       

        side_length_2n_initial = MathTex(
            r"\text{side length}_{2n} = \sqrt{\left(\frac{\text{side length}_n}{2}\right)^2 + \left(r - \sqrt{r^2 - \left(\frac{\text{side length}_n^2}{4}\right)}\right)^2}",
            font_size=36,
            color=WHITE
        )

        self.play(FadeIn(side_length_2n_initial))
        self.wait(2)

        side_length_n = MathTex(r"\text{side length}_n = 1 ", font_size=36, color=WHITE)
        side_length_n.next_to(side_length_2n_initial, UP, buff=0.5)
        radius = MathTex(r"r = 1", font_size=36, color=WHITE)
        radius.next_to(side_length_n, UP, buff=0.5)

        self.play(
            FadeIn(side_length_n),
            FadeIn(radius)
        )

        self.wait(2)

        side_length_2n_second = MathTex(
            r"\text{side length}_{2n} = \sqrt{\left(\frac{1}{2}\right)^2 + \left(1 - \sqrt{1^2 - \left(\frac{1^2}{4}\right)}\right)^2}",
            font_size=36,
            color=WHITE
        )

        self.play(AnimationGroup(
            Transform(side_length_2n_initial, side_length_2n_second),
            AnimationGroup(
                FadeOut(side_length_n),
                FadeOut(radius),
                lag_ratio=0
            ),
            lag_ratio=0.5
        ))

        self.wait(2)

        side_length_2n_final = MathTex(
            r"\text{side length}_{2n} = 0.51\overline{7}",
            font_size=36,
            color=WHITE
        )

        self.play(Transform(side_length_2n_initial, side_length_2n_final))
        self.wait(2)







