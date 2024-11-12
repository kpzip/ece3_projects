from manim import *
import numpy as np
import lib

class FourierTransformInternals(Scene):

    def construct(self):
        ft_intro_text = Text("How It Works", gradient=(RED, BLUE)).scale(2)
        transform_tex_initial_animation = MathTex(r"\hat{f}(\xi)", r"=", r"\int_{-\infty}^{\infty}f(x)e^{-2\pi ix\xi}dx", color=WHITE).shift(3 * RIGHT)
        radial_axes_initial_animation = ComplexPlane(x_range=[-1.3, 1.3, 1], y_range=[-1.3, 1.3, 1], x_length=6, y_length=6, axis_config={"include_numbers": True}).shift(3 * LEFT)
        transform_tex = MathTex(r"\hat{f}(\xi)", r"=", r"\int_{-\infty}^{\infty}f(x)e^{-2\pi ix\xi}dx", color=WHITE).scale(0.6).shift(4 * RIGHT + 1.2 * DOWN)
        radial_axes = ComplexPlane(x_range=[-1.3, 1.3, 1], y_range=[-1.3, 1.3, 1], x_length=6, y_length=6, axis_config={"include_numbers": True}).scale(0.5).shift(4 * LEFT + 1.2 * DOWN)

        arrow_tracker = ValueTracker(0)
        drawable_arrow = Arrow(start=radial_axes.get_origin(), end=radial_axes.c2p(1, 0), color=YELLOW)
        arrow = always_redraw(lambda: Arrow(start=radial_axes.get_origin(), end=radial_axes.c2p(np.cos(arrow_tracker.get_value() * 2 * np.pi), np.sin(arrow_tracker.get_value() * 2 * np.pi)), color=YELLOW))

        # Intro
        self.play(Write(ft_intro_text))
        self.wait(0.5)
        self.play(Unwrite(ft_intro_text))
        self.wait(0.5)

        # Draw fourier transform + radial axes
        self.play(Write(transform_tex_initial_animation), Write(radial_axes_initial_animation))
        self.play(transform_tex_initial_animation.animate.shift(1 * RIGHT + 1.2 * DOWN).scale(0.6), radial_axes_initial_animation.animate.shift(1 * LEFT + 1.2 * DOWN).scale(0.5))
        self.remove(transform_tex_initial_animation, radial_axes_initial_animation)
        self.add(transform_tex, radial_axes)
        self.wait(0.5)

        # Arrow rotating - euler's formula
        self.play(Write(drawable_arrow))
        self.remove(drawable_arrow)
        self.add(arrow)
        self.wait(0.5)
        self.play(arrow_tracker.animate.set_value(4), run_time=12, rate_func=linear)

        # Wait at the end
        self.wait(2)
