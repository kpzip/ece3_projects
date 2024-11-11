import numpy as np
from manim import *
import math
import lib
import scipy as sp

A4 = 440.0
Cs5 = 554.37
E5 = 659.25
A5 = 2 * A4

time_min_x = 0
time_max_x = 7

freq_min_x = 0
freq_max_x = 7

class FourierTransforms(Scene):

    def construct(self):
        ft_intro_text = Text("Fourier Transforms", gradient=(BLUE, DARK_BROWN)).scale(2)

        ft_eq = MathTex(r"\hat{f}(\xi)=\int_{-\infty}^{\infty}f(x)e^{-2\pi ix\xi}dx", color=PURPLE).scale(0.6).shift(1.5 * DOWN)

        time_domain = Axes(x_range=[time_min_x, time_max_x, 0.5], y_range=[-1.3, 1.3, 1], x_length=25, axis_config={"include_numbers": True}, x_axis_config={"numbers_with_elongated_ticks": range(time_min_x, time_max_x, 1)}).scale(0.4).shift(2 * UP)
        time_domain_title = MathTex(r"\text{``Time Domain''}", color=YELLOW).shift(3.5 * UP)
        time_domain_labels = time_domain.get_axis_labels(x_label=MathTex(r"\text{Time}").scale(0.5), y_label=MathTex(r"\text{Intensity}").scale(0.5))

        wave1_func_comp1 = lambda x: 0.333 * lib.normalized_sin(1 * x)
        wave1_func_comp2 = lambda x: 0.667 * lib.normalized_sin(1.33 * x)
        wave1_func = lambda x: wave1_func_comp1(x) + wave1_func_comp2(x)
        initial_wave_draw_tracker = ValueTracker(0)
        initial_wave_draw = always_redraw(lambda: time_domain.plot(wave1_func, color=PURPLE, x_range=[time_domain.x_range[0], initial_wave_draw_tracker.get_value()]))
        initial_wave_draw_dot = always_redraw(lambda: Dot(point=time_domain.c2p(initial_wave_draw_tracker.get_value(), initial_wave_draw.underlying_function(initial_wave_draw_tracker.get_value())), color=PURPLE))
        wave1 = time_domain.plot(wave1_func, color=PURPLE)
        wave1_eq = MathTex(r"f(x)", r"=", r"\frac{1}{3}", r"\sin(", r"1", r"\cdot2\pi x)", r"+", r"\frac{2}{3}", r"\sin(", r"\frac{4}{3}", r"\cdot2\pi x)").scale(0.6).shift(0.3 * UP + 2 * LEFT)
        wave1_eq[0][:].set_color(PURPLE)
        wave1_eq[2][:].set_color(RED)
        wave1_eq[3][:].set_color(RED)
        wave1_eq[4][:].set_color(RED)
        wave1_eq[5][:].set_color(RED)
        wave1_eq[7][:].set_color(BLUE)
        wave1_eq[8][:].set_color(BLUE)
        wave1_eq[9][:].set_color(BLUE)
        wave1_eq[10][:].set_color(BLUE)

        wave2_approx_amount = 8
        wave2 = always_redraw(lambda: time_domain.plot(lib.square_wave_fourier(wave2_approx_amount), color=BLUE))

        components_tracker = ValueTracker(0)
        wave1_comp1 = always_redraw(lambda: time_domain.plot(lambda x: wave1_func_comp1(x) + components_tracker.get_value(), color=RED))
        wave1_comp2 = always_redraw(lambda: time_domain.plot(lambda x: wave1_func_comp2(x) - components_tracker.get_value(), color=BLUE))

        frequency_domain = Axes(x_range=[time_min_x, time_max_x, 0.5], y_range=[0, 0.72, 0.5], x_length=25, axis_config={"include_numbers": True}, x_axis_config={"numbers_with_elongated_ticks": range(freq_min_x, freq_max_x, 1)}).scale(0.4).shift(-2 * UP)
        frequency_domain_title = MathTex(r"\text{``Frequency Domain''}", color=YELLOW).shift(0.5 * DOWN)
        frequency_domain_labels = frequency_domain.get_axis_labels(x_label=MathTex(r"\text{Frequency}").scale(0.5), y_label=MathTex(r"\text{Contributing Factor}").scale(0.5))

        ft1_func = lib.fft_func(wave1_func, freq_max_x)
        real_ft1_func = lib.analytical_fft([0.333, 0.667], [1, 1.33])

        # initial_ft_draw_tracker = ValueTracker(0)
        # initial_ft_draw = always_redraw(lambda: frequency_domain.plot(ft1_func, color=PURPLE, x_range=[time_domain.x_range[0], initial_ft_draw_tracker.get_value()]))
        # initial_ft_draw_dot = always_redraw(lambda: Dot(point=frequency_domain.c2p(initial_ft_draw_tracker.get_value(), initial_ft_draw.underlying_function(initial_ft_draw_tracker.get_value())), color=PURPLE))
        ft1 = frequency_domain.plot(ft1_func, color=PURPLE)
        real_ft1 = frequency_domain.plot(real_ft1_func, color=PURPLE, x_range=frequency_domain.x_range[:2] + [0.0001], use_smoothing=False)
        ft2 = always_redraw(lambda: frequency_domain.plot(lib.fft_func(wave2.underlying_function, freq_max_x), color=BLUE))

        # Animation

        # Intro
        self.play(Write(ft_intro_text))
        self.wait(0.5)
        self.play(Unwrite(ft_intro_text))
        self.wait(0.5)

        # Time Space
        self.play(Write(time_domain))
        self.wait(0.5)
        self.play(Write(time_domain_title), Write(time_domain_labels[1]), Write(time_domain_labels[0]))
        self.wait(1)
        self.play(Wiggle(time_domain_labels[1]))
        self.wait(0.6)
        self.play(Wiggle(time_domain_labels[0]))
        self.wait(1)

        # Frequency Space
        self.play(Write(frequency_domain))
        self.wait(0.5)
        self.play(Write(frequency_domain_title), Write(frequency_domain_labels[1]), Write(frequency_domain_labels[0]))
        self.wait(1)
        self.play(Wiggle(frequency_domain_labels[1]))
        self.wait(0.6)
        self.play(Wiggle(frequency_domain_labels[0]))
        self.wait(1)

        # Wave1 and components
        self.add(initial_wave_draw, initial_wave_draw_dot)
        self.play(initial_wave_draw_tracker.animate.set_value(time_domain.x_range[1]))
        self.play(FadeOut(initial_wave_draw_dot))
        self.remove(initial_wave_draw)
        self.add(wave1)
        self.wait(1.5)
        # Components
        wave1_copy1 = wave1.copy()
        wave1_copy2 = wave1.copy()
        self.remove(wave1)
        self.play(Transform(wave1_copy1, wave1_comp1), Transform(wave1_copy2, wave1_comp2))
        self.remove(wave1_copy1, wave1_copy2)
        self.add(wave1_comp1, wave1_comp2)
        self.play(components_tracker.animate.set_value(0.7))
        self.wait(0.2)
        self.play(Wiggle(wave1_comp1), Wiggle(wave1_comp2))
        self.wait(0.2)
        self.play(components_tracker.animate.set_value(0.2))
        self.play(Transform(wave1_comp1, wave1, replace_mobject_with_target_in_scene=True), Transform(wave1_comp2, wave1, replace_mobject_with_target_in_scene=True))
        self.remove(wave1_comp1, wave1_comp2)
        self.add(wave1)
        self.wait(0.5)

        # constructive interference
        c_arrow_1_pointing_to = time_domain.c2p(5.35, 0.80)
        c_arrow_1 = Arrow(start=c_arrow_1_pointing_to + np.array([1.8, 0.5, 0]), end=c_arrow_1_pointing_to)
        c_arrow_2_pointing_to = time_domain.c2p(6.2, 0.95)
        c_arrow_2 = Arrow(start=c_arrow_2_pointing_to + np.array([1.4, 0.4, 0]), end=c_arrow_2_pointing_to)
        constructive_arrows = VGroup(c_arrow_1, c_arrow_2)
        constructive_text = MathTex(r"\text{``constructive interference''}").scale(0.4).shift(3.5 * UP + 4.5 * RIGHT)
        self.play(Write(constructive_arrows))
        self.play(Write(constructive_text))
        self.wait(1.5)

        # destructive interference
        d_arrow_1_pointing_to = time_domain.c2p(4.5, 0.25)
        d_arrow_1 = Arrow(start=d_arrow_1_pointing_to + np.array([0.5, -1.5, 0]), end=d_arrow_1_pointing_to)
        d_arrow_2_pointing_to = time_domain.c2p(5.2, 0.25)
        d_arrow_2 = Arrow(start=d_arrow_2_pointing_to + np.array([0.3, -1.5, 0]), end=d_arrow_2_pointing_to)
        destructive_arrows = VGroup(d_arrow_1, d_arrow_2)
        destructive_text = MathTex(r"\text{``destructive interference''}").scale(0.4).shift(2.5 * RIGHT + 0.7 * UP)
        self.play(Write(destructive_arrows))
        self.play(Write(destructive_text))
        self.wait(1.5)
        self.play(Unwrite(constructive_arrows), Unwrite(constructive_text))
        self.play(Unwrite(destructive_arrows), Unwrite(destructive_text))

        # fft
        wave1_copy4 = wave1.copy()
        self.play(Transform(wave1_copy4, ft_eq), run_time=2)
        self.remove(wave1_copy4)
        self.add(ft_eq)
        self.wait(1)
        self.play(Transform(ft_eq, ft1), run_time=2)
        self.remove(ft_eq)
        # self.add(initial_ft_draw, initial_ft_draw_dot)
        # self.play(initial_ft_draw_tracker.animate.set_value(time_domain.x_range[1]))
        # self.play(FadeOut(initial_ft_draw_dot))
        # self.remove(initial_ft_draw)
        self.add(ft1)
        self.wait(1.5)

        # ft1 explanation
        lines1 = frequency_domain.get_lines_to_point(frequency_domain.c2p(1.0, 0.35))
        lines2 = frequency_domain.get_lines_to_point(frequency_domain.c2p(1.29, 0.51))
        self.wait(0.5)
        self.play(Write(lines1))
        self.wait(0.5)
        self.play(Write(lines2))
        self.wait(2)
        wave1_copy4 = wave1.copy()
        self.play(Transform(wave1_copy4, wave1_eq))
        self.remove(wave1_copy4)
        self.add(wave1_eq)
        self.play(Wiggle(wave1_eq[4], scale_value=2.5), Wiggle(lines1[0], scale_value=1.5))
        self.play(Wiggle(wave1_eq[2], scale_value=1.5), Wiggle(lines1[1], scale_value=1.5))
        self.play(Wiggle(wave1_eq[9], scale_value=1.5), Wiggle(lines2[0], scale_value=1.5))
        self.play(Wiggle(wave1_eq[7], scale_value=1.5), Wiggle(lines2[1], scale_value=1.5))
        self.wait(2)
        self.play(Unwrite(lines1), Unwrite(lines2))

        # fft approximation versus real ft
        approx_arrow_pointing_to = frequency_domain.c2p(1.5, 0.25)
        approx_arrow = Arrow(start=approx_arrow_pointing_to + np.array([1.5, 0.5, 0]), end=approx_arrow_pointing_to)
        fft = MathTex(r"\text{``FFT''}").scale(0.6).shift(2 * DOWN + 1 * LEFT)
        real = MathTex(r"\text{Real Fourier Transform}", r"").scale(0.6).shift(2 * DOWN)
        real_asterix = MathTex(r"\text{Real Fourier Transform}", r"\text{*}").scale(0.6).shift(2 * DOWN)
        self.play(Write(approx_arrow), Write(fft))
        self.wait(4)
        ft1_c1 = ft1.copy()
        self.remove(ft1)
        self.add(ft1_c1)
        self.play(Transform(fft, real), Transform(ft1_c1, real_ft1))
        self.remove(fft, ft1_c1)
        self.add(real, real_ft1)
        rft_point1 = Dot(point=frequency_domain.c2p(1, 0.333), color=PURPLE)
        rft_point2 = Dot(point=frequency_domain.c2p(1.33, 0.667), color=PURPLE)
        rft_point1_tex = MathTex(r"(1, \frac{1}{3})", color=PURPLE).scale(0.5).move_to(rft_point1).shift(0.5 * LEFT)
        rft_point2_tex = MathTex(r"(\frac{4}{3}, \frac{2}{3})", color=PURPLE).scale(0.5).move_to(rft_point2).shift(0.5 * RIGHT + 0.1 * DOWN)
        self.play(Write(rft_point1), Write(rft_point1_tex))
        self.play(Write(rft_point2), Write(rft_point2_tex))
        self.wait(1)
        self.play(TransformMatchingTex(real, real_asterix, fade_transform_mismatches=True))
        self.remove(real)
        self.add(real_asterix)
        asterix_text = MathTex(r"\text{*in reality the the spikes are delta functions and their integrals are the amplitudes.}").scale(0.4).shift(3.7 * DOWN)
        self.play(Write(asterix_text), run_time=1.5)
        self.wait(1.5)
        self.play(Unwrite(rft_point1), Unwrite(rft_point2), Unwrite(rft_point1_tex), Unwrite(rft_point2_tex), Unwrite(real_asterix), Unwrite(approx_arrow), Unwrite(asterix_text))
        self.play(Transform(real_ft1, ft1))
        self.remove(real_ft1)
        self.add(ft1)
        self.wait(1)

        # fft with sin wave approximation
        self.play(Transform(wave1, wave2), Transform(ft1, ft2))
        self.remove(wave1, ft1)
        self.add(wave2, ft2)
        self.wait(0.5)
        wave2_approx_amount = 9
        self.wait(0.5)

        # End Pause
        self.wait(2)
