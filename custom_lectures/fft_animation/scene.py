from manim import *


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        text = Text("\"Read address 0xff\"").shift(2 * UP).set_fill(YELLOW)
        
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen
        self.play(DrawBorderThenFill(text, stroke_color=YELLOW))
        self.wait(0.5)

