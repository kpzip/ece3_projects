from manim import *
import lib


class Applications(Scene):

    def construct(self):
        apps_intro_text = Text("Applications", gradient=(RED, GREEN)).scale(2)

        initial_wave_func = lambda x: (lib.normalized_sin(x * 1) + lib.normalized_sin(x * 2) + lib.normalized_sin(x * 3) + lib.normalized_sin(x * 5))
        initial_axes = Axes(x_range=[0, 15, 1], y_range=[0, 1.3, 1], x_length=10, y_length=3).scale(0.5).shift(3 * LEFT + 1.5 * UP)
        initial_wave_draw_tracker = ValueTracker(0)
        initial_wave_plot = always_redraw(lambda: initial_axes.plot(lambda x: 0.5 * 0.25 * initial_wave_func(x) + 0.5, color=BLUE, x_range=[0, initial_wave_draw_tracker.get_value()]))

        initial_ft_wave_func = lib.fft_func(initial_wave_func, 15)
        initial_ft_axes = Axes(x_range=[0, 15, 1], y_range=[0, 1.3, 1], x_length=10, y_length=3).scale(0.5).shift(3 * LEFT + 1.5 * DOWN)
        initial_ft_wave_plot = initial_ft_axes.plot(initial_ft_wave_func, color=PURPLE)

        filtered_wave_func = lambda x: lib.normalized_sin(x * 1)
        filtered_axes = Axes(x_range=[0, 15, 1], y_range=[0, 1.3, 1], x_length=10, y_length=3).scale(0.5).shift(3 * RIGHT + 1.5 * UP)
        filtered_wave_plot = filtered_axes.plot(lambda x: 0.5 * 0.5 * filtered_wave_func(x) + 0.5, color=BLUE)

        filtered_ft_wave_func = lib.fft_func(filtered_wave_func, 15)
        filtered_ft_axes = Axes(x_range=[0, 15, 1], y_range=[0, 1.3, 1], x_length=10, y_length=3).scale(0.5).shift(3 * RIGHT + 1.5 * DOWN)
        filtered_ft_plot_unfiltered = filtered_ft_axes.plot(initial_ft_wave_func, color=PURPLE)
        filtered_ft_wave_plot = filtered_ft_axes.plot(filtered_ft_wave_func, color=PURPLE)

        first_arrow = MathTex(r"\Downarrow").shift(3 * LEFT)
        second_arrow = MathTex(r"\Rightarrow").shift(1.5 * DOWN)
        third_arrow = MathTex(r"\Uparrow").shift(3 * RIGHT)

        self.play(Write(apps_intro_text))
        self.wait(0.5)
        self.play(Unwrite(apps_intro_text))
        self.wait(0.5)

        self.play(Write(initial_axes))
        self.wait(2)
        self.add(initial_wave_plot)
        self.play(initial_wave_draw_tracker.animate.set_value(15))
        initial_wave_plot.clear_updaters()
        self.wait(10)
        self.play(Write(initial_ft_axes))
        self.play(ReplacementTransform(initial_wave_plot.copy(), initial_ft_wave_plot), Write(first_arrow))
        self.wait(4)
        self.play(Write(filtered_ft_axes))
        self.play(ReplacementTransform(initial_ft_wave_plot.copy(), filtered_ft_plot_unfiltered), Write(second_arrow))
        self.wait(1)
        self.play(ReplacementTransform(filtered_ft_plot_unfiltered, filtered_ft_wave_plot))
        self.wait(7)
        self.play(Write(filtered_axes))
        self.play(ReplacementTransform(filtered_ft_wave_plot.copy(), filtered_wave_plot), Write(third_arrow))
        self.wait(15)
        self.play(Unwrite(VGroup(initial_axes, initial_ft_axes, filtered_ft_axes, filtered_axes, first_arrow, second_arrow, third_arrow)), FadeOut(Group(initial_wave_plot, initial_ft_wave_plot, filtered_wave_plot, filtered_ft_wave_plot)))
        self.wait(4)



        # Oscilloscope
        main_outline = Rectangle(height=2, width=4)
        viewport = Rectangle(height=1, width=1.8).move_to(main_outline).shift(0.9 * LEFT + 0.3 * UP)
        left_foot = Rectangle(height=0.2, width=0.5).next_to(main_outline, DOWN, buff=0).shift(1.4 * LEFT)
        right_foot = Rectangle(height=0.2, width=0.5).next_to(main_outline, DOWN, buff=0).shift(1.4 * RIGHT)
        knob_1 = Circle(radius=0.1, color=WHITE).move_to(main_outline).shift(0.5 * RIGHT + 0.6 * DOWN)
        knob_2 = Circle(radius=0.1, color=WHITE).move_to(knob_1).shift(0.5 * RIGHT)
        knob_3 = Circle(radius=0.1, color=WHITE).move_to(knob_2).shift(0.5 * RIGHT)

        in_1 = Circle(radius=0.15, color=WHITE).move_to(main_outline).shift(1.6 * LEFT + 0.6 * DOWN)
        in_2 = Circle(radius=0.15, color=WHITE).move_to(in_1).shift(0.5 * RIGHT)

        dot_1 = Dot(color=RED).scale(0.5).move_to(main_outline).shift(0.8 * UP + 1.8 * RIGHT)
        dot_2 = Dot(color=BLUE).scale(0.5).move_to(dot_1).shift(0.2 * LEFT)

        scope_axes = Axes(x_length=1.8, y_length=1, x_range=[0, 4], y_range=[0, 5]).move_to(viewport).shift(0.08 * LEFT)
        sin_func = lambda x: np.sin(2 * PI * x)
        sine_wave = scope_axes.plot(lambda x: sin_func(x) + 3, color=GREEN)
        fft_func = lib.fft_func(sin_func, 5)
        fft_plot = scope_axes.plot(lambda x: fft_func(x) + 0.1, color=YELLOW)

        ch1 = Tex("CH1", color=GREEN).scale(0.5).shift(2.5 * LEFT + 0.5 * UP)
        fft_ch1 = Tex("FFT(CH1)", color=YELLOW).scale(0.5).shift(2.75 * LEFT)



        scope = VGroup(main_outline, viewport, left_foot, right_foot, knob_1, knob_2, knob_3, in_1, in_2, dot_1, dot_2)
        scope_entirety = Group(sine_wave, fft_plot, scope)

        # Draw it
        self.play(Write(scope))
        self.play(FadeIn(sine_wave))
        self.play(Write(ch1))
        self.play(FadeIn(fft_plot))
        self.play(Write(fft_ch1))
        self.wait(5)
        self.play(Unwrite(VGroup(ch1, fft_ch1)), scope_entirety.animate.shift(4 * LEFT).scale(0.7))
        self.wait(10)

        # Mp3
        width = 1
        height = 1.6
        delta = 0.2
        file_logo = Polygon(np.array([0.5 * width, 0.5 * height - delta, 0]), np.array([0.5 * width - delta, 0.5 * height, 0]), np.array([-0.5 * width, 0.5 * height, 0]), np.array([-0.5 * width, -0.5 * height, 0]), np.array([0.5 * width, -0.5 * height, 0]), fill_color=WHITE, color=WHITE, fill_opacity=1)

        peel_corner = Polygon(np.array([0.5 * width, 0.5 * height - delta, 0]), np.array([0.5 * width - delta, 0.5 * height - delta, 0]), np.array([0.5 * width - delta, 0.5 * height, 0]), fill_opacity=1, fill_color=GRAY, color=GRAY)
        banner = Rectangle(width=1.3, height=0.28, fill_color=BLUE, color=BLUE, fill_opacity=1).move_to(file_logo).shift(0.3 * DOWN)
        text = Tex(".mp3", color=WHITE).scale(0.5).move_to(banner)

        self.play(Write(file_logo), Write(peel_corner))
        self.play(Write(banner))
        self.play(Write(text))
        file_group = VGroup(file_logo, peel_corner, banner, text)
        self.play(file_group.animate.shift(3 * RIGHT))
        self.wait(5)
        self.play(Unwrite(scope), FadeOut(file_group), FadeOut(fft_plot), FadeOut(sine_wave))
        thanks = Tex("Thanks for watching!")
        self.play(Write(thanks))
        self.wait(5)
