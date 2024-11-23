from manim import *
import numpy as np
import lib

first_wave_color = YELLOW

class FourierTransformInternals(Scene):

    def construct(self):
        ft_intro_text = Text("How It Works", gradient=(RED, BLUE)).scale(2)
        transform_tex_initial_animation = MathTex(r"\hat{f}(", r"\xi", r")", r"=", r"\int_{-\infty}^{\infty}", r"f(x)", r"e^{-2\pi i", r"x", r"\xi}", r"dx", color=WHITE).shift(3 * RIGHT)
        complex_plane_initial_animation = ComplexPlane(x_range=[-1.3, 1.3, 1], y_range=[-1.3, 1.3, 1], x_length=6, y_length=6).add_coordinates().shift(3 * LEFT)
        transform_tex_scale = 0.7
        transform_tex_shift = 1 * RIGHT + 1.2 * DOWN
        transform_tex = transform_tex_initial_animation.copy().scale(transform_tex_scale).shift(transform_tex_shift)
        complex_plane_scale = 0.5
        complex_plane_shift = 1 * LEFT + 1.2 * DOWN
        complex_plane = complex_plane_initial_animation.copy().scale(complex_plane_scale).shift(complex_plane_shift)
        axes_max_x = 5
        axes = Axes(x_range=[0, axes_max_x, 0.5], y_range=[0, 1.2, 1], x_length=25, y_length=5, axis_config={"include_numbers": True}, x_axis_config={"numbers_with_elongated_ticks": range(0, axes_max_x, 1)}).scale(0.4).shift(2.5 * UP)

        sin_wave_func = lambda x: 0.5 * np.cos(x * 2 * np.pi * 2) + 0.5
        sin_wave_draw_tracker = ValueTracker(0)
        sin_wave_cartesian_graph_drawing = always_redraw(lambda: axes.plot(sin_wave_func, x_range=[0, sin_wave_draw_tracker.get_value()], color=first_wave_color))
        sin_wave_cartesian_arrow = always_redraw(lambda: Arrow(start=axes.c2p(sin_wave_draw_tracker.get_value(), 0), end=axes.c2p(sin_wave_draw_tracker.get_value(), sin_wave_func(sin_wave_draw_tracker.get_value())), buff=0, color=YELLOW))
        sin_wave_cartesian_graph = axes.plot(sin_wave_func, color=first_wave_color)

        xi_tracker_init = 1.1
        xi_tracker = ValueTracker(xi_tracker_init)
        xi_tex = always_redraw(lambda: MathTex(r"\xi=", f"{xi_tracker.get_value():.2f}").scale(0.6).shift(2 * DOWN))
        xi_slider = NumberLine(x_range=[0, 5, 1], include_numbers=True, numbers_with_elongated_ticks=[0, 5]).scale(0.7).shift(2.4 * DOWN)
        xi_dot = always_redraw(lambda: Dot(point=xi_slider.n2p(xi_tracker.get_value())))

        # set to 16 PI for final render, since this seems to cause a lot of lag when rendering
        theta_range = np.array([0, (2 * PI)])
        sin_wave_radial_graph = complex_plane.plot_polar_graph(lambda x: sin_wave_func(x / (xi_tracker_init * 2 * PI)), theta_range=theta_range * xi_tracker_init, color=first_wave_color)
        sin_wave_radial_graph_adjustable = always_redraw(lambda: complex_plane.plot_polar_graph(lambda x: sin_wave_func(x / (xi_tracker.get_value() * 2 * PI)), theta_range=theta_range * xi_tracker.get_value(), color=first_wave_color))

        arrow_tracker = ValueTracker(0)

        arrow = always_redraw(lambda: Arrow(start=complex_plane.get_origin(), end=complex_plane.c2p(np.cos(arrow_tracker.get_value() * 2 * np.pi), np.sin(arrow_tracker.get_value() * 2 * np.pi)), color=YELLOW, buff=0))
        sin_following_arrow = always_redraw(lambda: Arrow(start=complex_plane.get_origin(), end=complex_plane.c2p(
            np.cos(arrow_tracker.get_value() * 2 * np.pi) * sin_wave_radial_graph.underlying_function(arrow_tracker.get_value() * 2 * PI),
            np.sin(arrow_tracker.get_value() * 2 * np.pi) * sin_wave_radial_graph.underlying_function(arrow_tracker.get_value() * 2 * PI)),
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
        self.play(Circumscribe(transform_tex[6]), run_time=2)
        self.wait(4)
        self.play(Write(arrow))
        self.wait(0.5)
        rev_time = 2.5
        self.play(arrow_tracker.animate.set_value(1), run_time=rev_time, rate_func=linear)
        self.play(arrow_tracker.animate.set_value(1.5), FadeIn(complex_unit_circle), run_time=rev_time/2, rate_func=linear)
        self.play(arrow_tracker.animate.set_value(2), FadeOut(complex_unit_circle), run_time=rev_time/2, rate_func=linear)
        self.play(arrow_tracker.animate.set_value(3), run_time=rev_time, rate_func=linear)
        arrow_tracker.set_value(0)
        self.wait(3)

        # Radial Graphing + Sin Wave
        self.play(Circumscribe(transform_tex[5]), Circumscribe(transform_tex[7]), run_time=2)
        self.wait(2)
        self.play(Write(axes))
        self.wait(1)
        self.play(FadeIn(sin_wave_cartesian_arrow))
        self.add(sin_wave_cartesian_graph_drawing)
        self.play(sin_wave_draw_tracker.animate.set_value(axes_max_x), run_time=7, rate_func=linear)
        self.play(FadeOut(sin_wave_cartesian_arrow))
        self.remove(sin_wave_cartesian_graph_drawing)
        self.add(sin_wave_cartesian_graph)
        self.wait(1)
        sin_wave_draw_tracker.set_value(0)
        sin_wave_copy = sin_wave_cartesian_graph.copy()
        self.add(sin_wave_copy)
        self.play(Transform(sin_wave_copy, sin_wave_radial_graph))
        self.remove(sin_wave_copy)
        self.add(sin_wave_radial_graph)
        self.wait(1)
        self.remove(arrow)
        self.add(sin_following_arrow)
        self.play(arrow_tracker.animate.set_value(xi_tracker_init), run_time=rev_time * 1.5, rate_func=linear)
        self.play(FadeOut(sin_following_arrow))
        self.wait(3)

        # xi
        self.play(Circumscribe(transform_tex[8]), Circumscribe(transform_tex[1]))
        self.wait(2)
        self.remove(sin_wave_radial_graph)
        self.add(sin_wave_radial_graph_adjustable)
        self.play(Write(xi_tex))
        self.play(Write(xi_slider), Write(xi_dot))
        self.wait(1)
        self.play(xi_tracker.animate.set_value(2), run_time=4)
        self.wait(0.5)
        self.play(xi_tracker.animate.set_value(3), run_time=3)
        self.wait(2)
        test_freq_tex = MathTex(r"\xi \text{ Acts as our ``test frequency''}").scale(0.6)
        self.play(Write(test_freq_tex))
        self.wait(0.5)
        self.play(xi_tracker.animate.set_value(0.5), run_time=6)
        self.wait(0.5)
        self.play(xi_tracker.animate.set_value(2), run_time=2)
        self.play(Unwrite(test_freq_tex))
        brace1 = BraceBetweenPoints(axes.c2p(1, 0.9), axes.c2p(1.5, 0.9), direction=UP)
        brace2 = BraceBetweenPoints(axes.c2p(1.5, 0.9), axes.c2p(2, 0.9), direction=UP)
        freq_text = MathTex(r"\text{2 Hz}").scale(0.6).move_to(axes.c2p(1.5, 1.3))
        self.play(Write(brace1))
        self.play(Write(brace2))
        self.play(Write(freq_text))
        self.wait(1)
        self.play(Unwrite(freq_text))
        self.play(Unwrite(brace1), Unwrite(brace2))
        self.wait(2)

        # integral
        self.play(Circumscribe(transform_tex[4]), Circumscribe(transform_tex[9]))
        area_polygon = Polygon(*sin_wave_radial_graph_adjustable.points, color=first_wave_color, fill_color=first_wave_color, fill_opacity=0.5)
        self.wait(0.5)
        self.play(FadeIn(area_polygon))
        self.wait(1)
        cross = Cross().move_to(area_polygon)
        self.play(Write(cross))
        self.wait(0.5)
        self.play(FadeOut(area_polygon), FadeOut(cross))
        self.wait(2)

        integral_explanation_tex_0 = MathTex(r"\text{For a sin wave,}").scale(0.7).shift(0.3 * UP)
        integral_explanation_tex_1 = MathTex(r"\text{If }", r"\xi\neq f_{n}", r"\text{, } \hat{f}(\xi)=0").scale(0.7).shift(0.3 * DOWN)
        integral_explanation_tex_2 = MathTex(r"\text{If }", r"\xi=f_{n}", r"\text{, } \hat{f}(\xi)=\infty").scale(0.7).shift(0.9 * DOWN)
        self.play(Write(integral_explanation_tex_0))
        self.play(Write(integral_explanation_tex_1))
        self.play(Write(integral_explanation_tex_2))
        self.wait(1)
        self.play(xi_tracker.animate.set_value(3), run_time=4)
        self.wait(0.2)
        self.play(xi_tracker.animate.set_value(0.5), run_time=2)
        self.wait(0.2)
        self.play(xi_tracker.animate.set_value(2), run_time=3)
        self.wait(1)
        more_examples_tex = MathTex(r"\text{More Examples!}").scale(0.8)
        self.play(Unwrite(integral_explanation_tex_0), Unwrite(integral_explanation_tex_1), Unwrite(integral_explanation_tex_2))
        self.play(Write(more_examples_tex))
        self.play(xi_tracker.animate.set_value(xi_tracker_init), run_time=2)
        self.wait(0.5)

        # 2 frequencies
        wave_2_func = lambda x: 0.25 * np.cos(x * 2 * np.pi * 2) + 0.25 * np.cos(x * 2 * np.pi * 5) + 0.5
        wave_2 = axes.plot(wave_2_func, color=BLUE)
        wave_2_radial = always_redraw(lambda: complex_plane.plot_polar_graph(lambda x: wave_2_func(x / (xi_tracker.get_value() * 2 * PI)), theta_range=theta_range * xi_tracker.get_value(), color=BLUE))
        self.play(ReplacementTransform(sin_wave_cartesian_graph, wave_2), ReplacementTransform(sin_wave_radial_graph_adjustable, wave_2_radial))
        self.wait(0.5)
        self.play(xi_tracker.animate.set_value(2), run_time=2)
        self.wait(1.5)
        self.play(xi_tracker.animate.set_value(5), run_time=2)

        # Wait at the end
        self.wait(2)
