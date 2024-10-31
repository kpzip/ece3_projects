from manim import *
import math

min_x = -3
max_x = 3
x_step = 0.5
sin_waves_text_color = YELLOW

class SineWaves(Scene):
    def construct(self):

        # Define Values
        text = Text("Sine Waves", color=sin_waves_text_color).scale(3)
        
        a_fadein_text = MathTex("a")
        a_fadein_text[0][:1].set_color(RED)
        a_fadein_group = VGroup(a_fadein_text).arrange_submobjects().scale(0.5).shift(4 * RIGHT + 1 * DOWN).shift(DOWN)
        sin_func_text = MathTex(r"f(x)=\sin(", r"2\pi", r"", r"x)")
        sin_func_text_with_a = MathTex(r"f(x)=\sin(", r"2\pi", r"a", r"x)").scale(0.5).shift(4 * RIGHT + 1 * DOWN)

        sin_func_text[0][:4].set_color(BLUE)
        sin_func_text[1][:2].set_color(YELLOW)
        sin_func_text[2][:1].set_color(BLUE)

        sin_func_text_with_a[0][:4].set_color(BLUE)
        sin_func_text_with_a[1][:2].set_color(YELLOW)
        sin_func_text_with_a[2][:1].set_color(RED)
        sin_func_text_with_a[3][:1].set_color(BLUE)
        
        a = ValueTracker(1)

        a_line = NumberLine(x_range=[0, 5, 1], include_numbers=True, numbers_with_elongated_ticks=[0, 5]).scale(0.7).shift(4 * RIGHT + 2.5 * DOWN)
        a_dot = always_redraw(lambda: Dot(point=a_line.n2p(a.get_value()), color=RED))
        a_value = always_redraw(lambda: Text(f"a = {a.get_value():.2f}", color=RED).scale(0.5).shift(4 * RIGHT + 2 * DOWN))

        vt = ValueTracker(min_x)
        axes = Axes(x_range=[min_x, max_x, x_step], y_range=[-1.2, 1.2, 1], x_length=15, axis_config={"include_numbers": True}, x_axis_config={"numbers_with_elongated_ticks": range(min_x, max_x, 1)}).scale(0.7).shift(1.6 * UP)

        sin_wave = always_redraw(lambda: axes.plot(lambda x: math.sin(2 * PI * a.get_value() * x), color=BLUE, x_range=[min_x, vt.get_value()]))
        sin_dot = always_redraw(lambda: Dot(point=axes.c2p(vt.get_value(), sin_wave.underlying_function(vt.get_value())), color=BLUE))
        
        fourier_transform = MathTex(r"\hat{f} (\xi)=\int_{-\infty}^{\infty}f(x)e^{-2\pi ix\xi}dx").scale(0.5).shift(4 * RIGHT + 1.5 * DOWN)


        # Animation

        # Sin Waves intro text
        self.play(Write(text, stroke_color=sin_waves_text_color))
        self.wait(0.5)
        self.play(Unwrite(text, stroke_color=sin_waves_text_color))
        
        # Draw sin wave and write down equation
        self.wait(0.5)
        # self.add(index_labels(sin_func_text_with_a[0]))
        self.play(Write(sin_func_text))
        self.play(sin_func_text.animate.scale(0.5).shift(4 * RIGHT + 1 * DOWN))
        self.play(Write(axes))
        self.wait(0.5)
        self.add(sin_wave, sin_dot)
        self.play(vt.animate.set_value(max_x), run_time=2)
        self.play(FadeOut(sin_dot))

        # introduce 'a' variable
        self.play(TransformMatchingTex(Group(sin_func_text, a_fadein_group), sin_func_text_with_a, run_time=1))
        self.play(Write(a_value))
        self.play(Write(a_line))
        self.play(Write(a_dot, run_time=0.5))
        self.play(a.animate.set_value(2), run_time=1)
        self.wait(0.5)
        self.play(a.animate.set_value(0), run_time=3)
        self.wait(0.5)
        self.play(a.animate.set_value(3), run_time=4)
        self.wait(0.5)
        self.play(a.animate.set_value(1), run_time=2)

        # self.add(index_labels(fourier_transform[0]))
        # self.play(Write(fourier_transform))
        self.wait(2)

        


