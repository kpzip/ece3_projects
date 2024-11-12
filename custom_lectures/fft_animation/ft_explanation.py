from manim import *
import numpy as np
import lib

class FourierTransformInternals(Scene):

    def construct(self):
        ft_intro_text = Text("How It Works", gradient=(RED, BLUE)).scale(2)
        transform_tex_initial_animation = MathTex(r"\hat{f}(\xi)", r"=", r"\int_{-\infty}^{\infty}", r"f(x)", r"e^{-2\pi i", r"x", r"\xi}", r"dx", color=WHITE).shift(3 * RIGHT)
        complex_plane_initial_animation = ComplexPlane(x_range=[-1.3, 1.3, 1], y_range=[-1.3, 1.3, 1], x_length=6, y_length=6).add_coordinates().shift(3 * LEFT)
        transform_tex_scale = 0.7
        transform_tex_shift = 1 * RIGHT + 1.2 * DOWN
        transform_tex = transform_tex_initial_animation.copy().scale(transform_tex_scale).shift(transform_tex_shift)
        complex_plane_scale = 0.5
        complex_plane_shift = 1 * LEFT + 1.2 * DOWN
        complex_plane = complex_plane_initial_animation.copy().scale(complex_plane_scale).shift(complex_plane_shift)
        axes_max_x = 10
        axes = Axes(x_range=[0, axes_max_x, 1], y_range=[0, 1.2, 1], x_length=25, y_length=5, axis_config={"include_numbers": True}).scale(0.4).shift(2.5 * UP)

        sin_wave_func = lambda x: 0.5 * np.cos(x * 2 * np.pi) + 0.5
        sin_wave_draw_tracker = ValueTracker(0)
        sin_wave_cartesian_graph_drawing = always_redraw(lambda: axes.plot(sin_wave_func, x_range=[0, sin_wave_draw_tracker.get_value()], color=RED))
        sin_wave_cartesian_arrow = always_redraw(lambda: Arrow(start=axes.c2p(sin_wave_draw_tracker.get_value(), 0), end=axes.c2p(sin_wave_draw_tracker.get_value(), sin_wave_func(sin_wave_draw_tracker.get_value())), buff=0, color=YELLOW))
        sin_wave_cartesian_graph = axes.plot(sin_wave_func, color=RED)

        sin_wave_radial_graph = complex_plane.plot_polar_graph(sin_wave_func, theta_range=[0, 3*PI], color=RED)

        arrow_tracker = ValueTracker(0)
        drawable_arrow = Arrow(start=complex_plane.get_origin(), end=complex_plane.c2p(1, 0), color=YELLOW, buff=0)
        arrow = always_redraw(lambda: Arrow(start=complex_plane.get_origin(), end=complex_plane.c2p(np.cos(arrow_tracker.get_value() * 2 * np.pi), np.sin(arrow_tracker.get_value() * 2 * np.pi)), color=YELLOW, buff=0))
        sin_following_arrow = always_redraw(lambda: Arrow(start=complex_plane.get_origin(), end=complex_plane.c2p(
            np.cos(arrow_tracker.get_value() * 2 * np.pi) * sin_wave_func(arrow_tracker.get_value() * 2 * PI),
            np.sin(arrow_tracker.get_value() * 2 * np.pi) * sin_wave_func(arrow_tracker.get_value() * 2 * PI)),
                                            color=YELLOW, buff=0))
        complex_unit_circle = Circle.from_three_points(complex_plane.c2p(1, 0), complex_plane.c2p(-1, 0), complex_plane.c2p(0, 1), color=PURPLE)


        # Intro
        self.play(Write(ft_intro_text))
        self.wait(0.5)
        self.play(Unwrite(ft_intro_text))
        self.wait(0.5)

        # Draw fourier transform + radial axes
        self.play(Write(transform_tex_initial_animation), Write(complex_plane_initial_animation))
        self.play(transform_tex_initial_animation.animate.shift(transform_tex_shift).scale(transform_tex_scale), complex_plane_initial_animation.animate.shift(complex_plane_shift).scale(complex_plane_scale))
        self.remove(transform_tex_initial_animation, complex_plane_initial_animation)
        self.add(transform_tex, complex_plane)
        self.wait(2)

        # Arrow rotating - euler's formula
        self.play(Circumscribe(transform_tex[4]), run_time=2)
        self.wait(2)
        self.play(Write(drawable_arrow))
        self.remove(drawable_arrow)
        self.add(arrow)
        self.wait(0.5)
        rev_time = 2.5
        self.play(arrow_tracker.animate.set_value(1), run_time=rev_time, rate_func=linear)
        self.play(arrow_tracker.animate.set_value(1.5), FadeIn(complex_unit_circle), run_time=rev_time/2, rate_func=linear)
        self.play(arrow_tracker.animate.set_value(2), FadeOut(complex_unit_circle), run_time=rev_time/2, rate_func=linear)
        self.play(arrow_tracker.animate.set_value(3), run_time=rev_time, rate_func=linear)
        arrow_tracker.set_value(0)
        self.wait(1)

        # Radial Graphing + Sin Wave
        self.play(Circumscribe(transform_tex[3]), Circumscribe(transform_tex[5]), run_time=2)
        self.play(Write(axes))
        self.play(FadeIn(sin_wave_cartesian_arrow))
        self.add(sin_wave_cartesian_graph_drawing)
        self.play(sin_wave_draw_tracker.animate.set_value(axes_max_x), run_time=7, rate_func=linear)
        self.play(FadeOut(sin_wave_cartesian_arrow))
        self.remove(sin_wave_cartesian_graph_drawing)
        self.add(sin_wave_cartesian_graph)
        sin_wave_draw_tracker.set_value(0)
        sin_wave_copy = sin_wave_cartesian_graph.copy()
        self.add(sin_wave_copy)
        self.play(Transform(sin_wave_copy, sin_wave_radial_graph))
        self.remove(sin_wave_copy)
        self.add(sin_wave_radial_graph)
        self.remove(arrow)
        self.add(sin_following_arrow)
        self.play(arrow_tracker.animate.set_value(1.5), run_time=(rev_time * 1.5) * 1.5, rate_func=linear)
        self.play(FadeOut(sin_following_arrow))


        # Wait at the end
        self.wait(2)
