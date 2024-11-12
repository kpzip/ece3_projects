from manim import *
import lib

class FourierTransformInternals(Scene):

    def construct(self):
        ft_intro_text = Text("How It Works", gradient=(RED, BLUE)).scale(2)
        transform_tex = MathTex(r"\hat{f}(\xi)", r"=", r"\int_{-\infty}^{\infty}f(x)e^{-2\pi ix\xi}dx", color=WHITE).shift(3 * RIGHT)
        radial_axes = Axes(x_range=[-1.3, 1.3, 1], y_range=[-1.3, 1.3, 1], x_length=6, y_length=6, axis_config={"include_numbers": True}).shift(3 * LEFT)

        # Intro
        self.play(Write(ft_intro_text))
        self.wait(0.5)
        self.play(Unwrite(ft_intro_text))
        self.wait(0.5)

        # Draw fourier transform + radial axes
        self.play(Write(transform_tex), Write(radial_axes))
        self.play(transform_tex.animate.shift(1 * RIGHT + 1.2 * DOWN).scale(0.6), radial_axes.animate.shift(1 * LEFT + 1.2 * DOWN).scale(0.5))

        # Wait at the end
        self.wait(2)
