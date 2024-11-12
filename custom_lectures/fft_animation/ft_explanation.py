from manim import *
import lib

class FourierTransformInternals(Scene):

    def construct(self):
        ft_intro_text = Text("How It Works", gradient=(RED, BLUE)).scale(2)

        # Intro
        self.play(Write(ft_intro_text))
        self.wait(0.5)
        self.play(Unwrite(ft_intro_text))
        self.wait(0.5)

        # Wait at the end
        self.wait(2)
