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

        components_tracker = ValueTracker(0)
        wave1_comp1 = always_redraw(lambda: time_domain.plot(lambda x: wave1_func_comp1(x) + components_tracker.get_value(), color=RED))
        wave1_comp2 = always_redraw(lambda: time_domain.plot(lambda x: wave1_func_comp2(x) - components_tracker.get_value(), color=BLUE))

        frequency_domain = Axes(x_range=[time_min_x, time_max_x, 0.5], y_range=[-0.65, 0.65, 0.5], x_length=25, axis_config={"include_numbers": True}, x_axis_config={"numbers_with_elongated_ticks": range(freq_min_x, freq_max_x, 1)}).scale(0.4).shift(-2 * UP)
        frequency_domain_title = MathTex(r"\text{``Frequency Domain''}", color=YELLOW).shift(0.5 * DOWN)
        frequency_domain_labels = frequency_domain.get_axis_labels(x_label=MathTex(r"\text{Frequency}").scale(0.5), y_label=MathTex(r"\text{Contributing Factor}").scale(0.5))

        N = 600
        T = freq_max_x / 600.0
        linspace = np.linspace(0.0, N * T, N, endpoint=False)
        yf = sp.fft.fft(wave1_func(linspace))
        xf = sp.fft.fftfreq(N, T)[:N // 2]
        ft1_func = sp.interpolate.interp1d(xf, 2.0/N * np.abs(yf[0:N//2]), bounds_error=False, fill_value="extrapolate")

        initial_ft_draw_tracker = ValueTracker(0)
        initial_ft_draw = always_redraw(lambda: frequency_domain.plot(ft1_func, color=PURPLE, x_range=[time_domain.x_range[0], initial_ft_draw_tracker.get_value()]))
        initial_ft_draw_dot = always_redraw(lambda: Dot(point=frequency_domain.c2p(initial_ft_draw_tracker.get_value(), initial_ft_draw.underlying_function(initial_ft_draw_tracker.get_value())), color=PURPLE))
        ft1 = frequency_domain.plot(ft1_func, color=PURPLE)

        # Animation

        # Intro
        self.play(Write(ft_intro_text))
        self.wait(0.5)
        self.play(Unwrite(ft_intro_text))
        self.wait(0.5)

        # Time Space
        self.play(Write(time_domain))
        self.wait(0.5)
        self.add(initial_wave_draw, initial_wave_draw_dot)
        self.play(initial_wave_draw_tracker.animate.set_value(time_domain.x_range[1]))
        self.play(FadeOut(initial_wave_draw_dot))
        self.remove(initial_wave_draw)
        self.add(wave1)
        self.wait(0.5)
        self.play(Write(time_domain_title))
        self.wait(1)
        self.play(Write(time_domain_labels[1]))
        self.play(Write(time_domain_labels[0]))
        self.wait(1)

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

        # Frequency Space
        self.play(Write(frequency_domain))
        self.wait(0.5)
        self.add(initial_ft_draw, initial_ft_draw_dot)
        self.play(initial_ft_draw_tracker.animate.set_value(time_domain.x_range[1]))
        self.play(FadeOut(initial_ft_draw_dot))
        self.remove(initial_ft_draw)
        self.add(ft1)
        self.wait(0.5)
        self.play(Write(frequency_domain_title))
        self.wait(1)
        self.play(Write(frequency_domain_labels[1]))
        self.play(Write(frequency_domain_labels[0]))
        self.wait(1)

        # End Pause
        self.wait(2)