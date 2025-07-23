from manim import *
import numpy as np
import math
# useful for "devising area of a circle"

class circleArea(MovingCameraScene):
    def construct(self):
        self.camera.frame_width = 14
        radius = 2.5  # radius used for code 
        
        # circle (inscribed at 0, 0, 0)
        center = ORIGIN
        circ = ParametricFunction(
            lambda u: np.array([radius * math.cos(u), radius * math.sin(u), 0]),
            t_range=[0, 2*PI],
            color=BLUE,
            stroke_width=3
        ).shift(center)  # shifted to center
        
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

        # remove stick 
        stick.remove_updater(update_stick)
        label.remove_updater(update_label)   
        self.play(FadeOut(stick), FadeOut(label))  

        # Generate vertices for polygons
        gon_6_vertices = generate_polygon_vertices(center, radius, 6)
        gon_12_vertices = generate_polygon_vertices(center, radius, 12)
        gon_24_vertices = generate_polygon_vertices(center, radius, 24)
        gon_48_vertices = generate_polygon_vertices(center, radius, 48)
        gon_96_vertices = generate_polygon_vertices(center, radius, 96)

        # create polygons
        gon_6 = Polygon(*gon_6_vertices, fill_opacity=0, stroke_opacity=0)
        gon_12 = Polygon(*gon_12_vertices, color=GREEN, stroke_width=3, fill_opacity=0.3)
        gon_24 = Polygon(*gon_24_vertices, color=GREEN, stroke_width=3, fill_opacity=0.3)
        gon_48 = Polygon(*gon_48_vertices, color=GREEN, stroke_width=3, fill_opacity=0.3)
        gon_96 = Polygon(*gon_96_vertices, color=GREEN, stroke_width=3, fill_opacity=0.3)
        # gon_96_opacity = Polygon(*gon_96_vertices, color=GREEN, stroke_width=3, fill_opacity=1)
        gon_current = Polygon(*gon_6_vertices, fill_opacity=0, stroke_opacity=0)

        # Create 6 equilateral triangles from hexagon
        hex_triangles = VGroup()
        for i in range(6):
            triangle = Polygon(center, gon_6_vertices[i], gon_6_vertices[(i + 1) % 6],
                               color=BLACK, stroke_width=2, fill_opacity=0.5, fill_color=GREEN)
            hex_triangles.add(triangle)
         
        # addresses layering issue between decagon and hexagon w/ color
        hex_triangles.set_z_index(1) # take priority 
        gon_current.set_z_index(0)

        self.play(Create(hex_triangles))
        self.wait(10)

        # "Comparing the hexagon to the full circle, you might notice that..."
        # Zoom in towards the area between gon 6 and circle
        self.play(
            self.camera.frame.animate.move_to(gon_6.get_center() + LEFT * 2 + DOWN).set(width=4),
            run_time=2
        )
        self.wait(5)

        # "As you may know, a hexagon is.."
        # Reset the camera to its original position and zoom level
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=14),
            run_time=2
        )

        self.wait(3)

        # increase sides of polygon
        self.play(Transform(gon_current, gon_12))  
        self.wait(1)

        # Transform gon_12 back into gon_6
        self.play(Transform(gon_current, gon_6))
        self.wait(1)

          # divide hexagon to hex_triangles
        n_initial = MathTex(r"n = \text{the number of sides on any polygon}", font_size=24, color=WHITE)
        n_initial.next_to(circ, DOWN, buff=0.5)
        self.play(FadeIn(n_initial))
        self.wait(4)
        self.play(Transform(gon_current, gon_6), Transform(n_initial, MathTex("n = 6", font_size=24).next_to(circ, DOWN, buff=0.5)))
        self.wait(2)
        
        # Double the sides of the initial polygon
        self.play(Transform(gon_current, gon_12), Transform(n_initial, MathTex("n = 12", font_size=24).next_to(circ, DOWN, buff=0.5)))  
        self.play(Transform(gon_current, gon_24), Transform(n_initial, MathTex("n = 24", font_size=24).next_to(circ, DOWN, buff=0.5)))
        self.play(Transform(gon_current, gon_48), Transform(n_initial, MathTex("n = 48", font_size=24).next_to(circ, DOWN, buff=0.5)))
        self.play(Transform(gon_current, gon_96), Transform(n_initial, MathTex("n = 96", font_size=24).next_to(circ, DOWN, buff=0.5)))
        #self.wait(5)
        #self.play(Transform(gon_current, gon_96_opacity))
        #self.wait(3)
        self.play(FadeOut(gon_current), FadeOut(n_initial))  
        self.wait(5)
        
        # declare wedge triangles
        # top will be blue, bottom will be red
        wedge_triangles = VGroup()
        for i in range(6):
            v1 = gon_12_vertices[2 * i]         
            v2 = gon_12_vertices[2 * i + 1]    
            v3 = gon_12_vertices[(2 * i + 2) % 12]   

            # Use vertical position to determine color
            avg_y = (v1[1] + v2[1] + v3[1]) / 3
            fill_color = BLUE if avg_y > center[1] else RED
            
            wedge = Polygon(v1, v2, v3, color=BLACK, stroke_width=2, fill_opacity=0.6, fill_color=fill_color)
            wedge_triangles.add(wedge)

        # "Now, if you took the excess area..."
        gon_current = Polygon(*gon_6_vertices, fill_opacity=0, stroke_opacity=0)
        n_initial = MathTex("n = 12", font_size=24)
        n_initial.next_to(circ, DOWN, buff=0.5)

        self.play(Transform(gon_current, Polygon(*gon_12_vertices, color=YELLOW, stroke_width=3, fill_opacity=0.3)), FadeIn(n_initial))  
        self.wait(3)
        self.play(FadeOut(gon_current), FadeOut(n_initial))

        self.play(Create(wedge_triangles), run_time=3)
        self.wait(5)

def generate_polygon_vertices(center, radius, sides):
    return [
        center + radius * np.array([np.cos(i * 2 * PI / sides), np.sin(i * 2 * PI / sides), 0])
        for i in range(sides)
    ]

class circleAreaFormula(Scene):
    def construct(self):
        # initial area formula
        area_formula = MathTex("A = \\text{width} \\times \\text{height}", font_size=72)
        self.play(FadeIn(area_formula))
       

        # replace height with r 
        area_formula_2 = MathTex("A = \\text{width} \\times r", font_size=72)
        area_formula_2.move_to(area_formula.get_center())
        self.play(Transform(area_formula, area_formula_2))

        # replace width with 1/2 * circumference
        area_formula_3 = MathTex("A = \\left(\\frac{1}{2} \\times \\text{circumference}\\right) \\times r", font_size=72)
        area_formula_3.move_to(area_formula.get_center())
        self.play(Transform(area_formula, area_formula_3))
        self.wait(3)

        # circumference formula
        circumferemce_formula = MathTex("\\text{circumference} = 2\\pi r", font_size=48)
        circumferemce_formula.next_to(area_formula_3, DOWN, buff=1.5)
        self.play(FadeIn(circumferemce_formula))
        self.wait(3)

        # replace circumference with 2pi*r
        area_formula_4 = MathTex("A = \\left(\\frac{1}{2} \\times 2\\pi r\\right) \\times r", font_size=72)
        area_formula_4.move_to(area_formula.get_center())
        self.play(AnimationGroup(
            Transform(area_formula, area_formula_4),
            FadeOut(circumferemce_formula),
            lag_ratio=0.5
        ))
        self.wait(3)

        # simplify to A = pi * r^2
        area_formula_final = MathTex("A = \\pi r^2", font_size=72)
        area_formula_final.move_to(area_formula.get_center())
        self.play(Transform(area_formula, area_formula_final))
        self.wait(5)

        # Height = r 
       # TODO : Implement the formula scene 
       # Area = base * height
       # height = r
       # base = 1/2 * circumference
       # circumference = 2pi*r 
       # 

class nApproachesInfinity(Scene):
    def construct(self):
        # Show n -> infinity
        n_infinity = MathTex("n \\to \\infty", font_size=72)
        n_infinity.move_to(ORIGIN)
        self.wait(1)
        self.play(FadeIn(n_infinity))
        self.wait(2)

#  Zoom in to a specific portion of the screen
# self.play(
#   self.camera.frame.animate.move_to(target_position).set(width=target_width),
#    run_time=2
# )