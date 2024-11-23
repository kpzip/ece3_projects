import numpy as np
from manim import *
import math
from lib import *

min_x = -3
max_x = 3
x_step = 0.5
sin_waves_text_color = YELLOW

VERY_DARK_BLUE = ManimColor("#144157")

class SineWaves(Scene):
    def construct(self):

        # Define Values
        text = Text("Sine Waves", color=sin_waves_text_color).scale(3)

        sin_func_text = MathTex(r"g(x)=\sin(", r"2\pi", r"", r"x)", "")
        sin_func_text_with_f = MathTex(r"g(x)=\sin(", r"2\pi", r"f", r"x)", "").scale(0.5).shift(4 * RIGHT + 1 * DOWN)
        multiple_sin_funcs = MathTex(r"g(x)", r"=", r"\alpha_{1}", r"\sin(", r"2\pi", r"f_{1}", r"x", r")+", r"\alpha_{2}", r"\sin(", r"2\pi", r"f_{2}", r"x", r")+\dots+", r"\alpha_{n}", r"\sin(", r"2\pi", r"f_{n}", r"x", r")").scale(0.5).move_to(sin_func_text_with_f).shift(0.5 * LEFT)
        multiple_sin_funcs[0][:].set_color(BLUE)
        multiple_sin_funcs[6][:].set_color(BLUE)
        multiple_sin_funcs[12][:].set_color(BLUE)
        multiple_sin_funcs[18][:].set_color(BLUE)
        multiple_sin_funcs_constants = [multiple_sin_funcs[2], multiple_sin_funcs[5], multiple_sin_funcs[8], multiple_sin_funcs[11], multiple_sin_funcs[14], multiple_sin_funcs[17]]
        for c in multiple_sin_funcs_constants:
            c[:].set_color(RED)
        multiple_sin_funcs[4][:].set_color(YELLOW)
        multiple_sin_funcs[10][:].set_color(YELLOW)
        multiple_sin_funcs[16][:].set_color(YELLOW)

        f_fadein_text = MathTex("f")
        f_fadein_text[0][:1].set_color(RED)
        f_fadein_group = VGroup(f_fadein_text).arrange_submobjects().scale(0.5).move_to(sin_func_text_with_f).shift(DOWN)


        sin_func_text[0][:4].set_color(BLUE)
        sin_func_text[1][:2].set_color(YELLOW)
        sin_func_text[2][:1].set_color(BLUE)

        sin_func_text_with_f[0][:4].set_color(BLUE)
        sin_func_text_with_f[1][:2].set_color(YELLOW)
        sin_func_text_with_f[2][:1].set_color(RED)
        sin_func_text_with_f[3][:1].set_color(BLUE)
        
        f = ValueTracker(1)

        f_line = NumberLine(x_range=[0, 5, 1], include_numbers=True, numbers_with_elongated_ticks=[0, 5]).scale(0.7).shift(4 * RIGHT + 2.5 * DOWN)
        f_dot = always_redraw(lambda: Dot(point=f_line.n2p(f.get_value()), color=RED))
        f_value = always_redraw(lambda: MathTex(r"f", r"=", f"{f.get_value():.2f}", color=RED).scale(0.5).shift(4 * RIGHT + 2 * DOWN))
        f_value_unknown = MathTex(r"f", r"=", r"\text{???}", color=RED).scale(0.5).move_to(f_value)
        f_alpha_value_unknown = MathTex(r"f_{1},f_{2},\dots f_{n},\alpha_{1},\alpha_{2},\dots \alpha_{n}", r"=", r"\text{???}", color=RED).scale(0.5).move_to(f_value)
        question_value_fadein = MathTex(r"\text{???}", color=RED)
        question_value_fadein_group = VGroup(question_value_fadein).arrange_submobjects().scale(0.5).move_to(f_value).shift(DOWN)

        vt = ValueTracker(min_x)
        axes = Axes(x_range=[min_x, max_x, x_step], y_range=[-1.2, 1.2, 1], x_length=15, axis_config={"include_numbers": True}, x_axis_config={"numbers_with_elongated_ticks": range(min_x, max_x, 1)}).scale(0.7).shift(1.6 * UP)

        sin_wave = always_redraw(lambda: axes.plot(lambda x: math.sin(2 * PI * f.get_value() * x), color=BLUE, x_range=[min_x, vt.get_value()]))
        sin_dot = always_redraw(lambda: Dot(point=axes.c2p(vt.get_value(), sin_wave.underlying_function(vt.get_value())), color=BLUE))

        square_approx = axes.plot(square_wave_fourier(9), color=BLUE, x_range=[min_x, max_x])

        lambda_line = always_redraw(lambda: NumberLine(x_range=[0, 1, 1], length=(axes.c2p(1/f.get_value(), 0)[0])).move_to(axes.c2p(0, -1.3), aligned_edge=np.array([-0.5, 0.0, 0.0])))

        def lambda_tex():
            tex = MathTex(r"\lambda=\frac{1}{f}")
            tex.scale(0.5).move_to(lambda_line)
            tex.shift(0.3 * DOWN)
            tex[0][4].set_color(RED)
            return tex

        lambda_symbol = always_redraw(lambda_tex)


        # Animation

        # Sin Waves intro text
        self.play(Write(text, stroke_color=sin_waves_text_color))
        self.wait(0.5)
        self.play(Unwrite(text, stroke_color=sin_waves_text_color))
        
        # Draw sin wave and write down equation
        self.wait(0.5)
        # self.add(index_labels(sin_func_text_with_f[0]))
        self.play(Write(sin_func_text))
        self.wait(2)
        self.play(sin_func_text.animate.scale(0.5).shift(4 * RIGHT + 1 * DOWN))
        self.play(Write(axes))
        self.wait(0.5)
        self.add(sin_wave, sin_dot)
        self.play(vt.animate.set_value(max_x), run_time=2)
        self.play(FadeOut(sin_dot))
        self.wait(7)

        # introduce 'f' variable
        self.play(TransformMatchingTex(Group(sin_func_text, f_fadein_group), sin_func_text_with_f, run_time=1))
        self.play(Write(f_value))
        self.play(Write(f_line))
        self.play(Write(f_dot, run_time=0.5))
        self.play(f.animate.set_value(2), run_time=1)
        self.wait(0.5)
        self.play(f.animate.set_value(0), run_time=3)
        self.wait(0.5)
        self.play(f.animate.set_value(3), run_time=4)
        self.wait(0.5)
        self.play(f.animate.set_value(1), run_time=2)
        self.wait(8)
        self.play(Write(lambda_line))
        self.play(Write(lambda_symbol))

        # show wavelength
        sin_wave_highlighted_section = axes.plot(sin_wave.underlying_function, color=BLUE, x_range=[0, 1 / f.get_value()])
        sin_wave_before_highlighted_section = axes.plot(sin_wave.underlying_function, color=BLUE, x_range=[axes.x_range[0], 0])
        sin_wave_after_highlighted_section = axes.plot(sin_wave.underlying_function, color=BLUE, x_range=[1 / f.get_value(), axes.x_range[1]])
        self.remove(sin_wave)
        self.add(sin_wave_before_highlighted_section, sin_wave_highlighted_section, sin_wave_after_highlighted_section)
        self.play(FadeToColor(sin_wave_before_highlighted_section, color=VERY_DARK_BLUE, run_time=0.5), FadeToColor(sin_wave_after_highlighted_section, color=VERY_DARK_BLUE, run_time=0.5))
        self.wait(0.5)
        self.play(Wiggle(sin_wave_highlighted_section))
        self.wait(0.5)
        self.play(FadeToColor(sin_wave_before_highlighted_section, color=BLUE, run_time=0.5), FadeToColor(sin_wave_after_highlighted_section, color=BLUE, run_time=0.5))
        self.remove(sin_wave_before_highlighted_section, sin_wave_highlighted_section, sin_wave_after_highlighted_section)
        self.add(sin_wave)
        self.wait(0.5)
        self.play(f.animate.set_value(2), run_time=1)
        self.wait(0.5)
        self.play(f.animate.set_value(4), run_time=1.25)
        self.wait(0.5)
        self.play(f.animate.set_value(0.5), run_time=1)
        self.wait(0.5)
        self.play(f.animate.set_value(1), run_time=1)
        self.wait(10)

        # ??? wavelength
        self.play(Unwrite(f_dot, run_time=1), Unwrite(f_line, run_time=1), TransformMatchingTex(Group(f_value, question_value_fadein_group), f_value_unknown, run_time=1))
        self.wait(0.35)
        self.play(f.animate.set_value(0.6666), run_time=1.25)
        self.wait(2)

        # freq calculation from eyeball wavelength
        freq_eyeball1 = MathTex(r"f=\frac{1}{\lambda}").center().scale(0.5).shift(2 * DOWN)
        freq_eyeball2 = MathTex(r"\lambda\approx1.5").scale(0.5).move_to(freq_eyeball1).shift(0.5 * DOWN)
        freq_eyeball3 = MathTex(r"f\approx\frac{1}{1.5}=0.6\overline6").scale(0.5).move_to(freq_eyeball2).shift(0.5 * DOWN)
        self.wait(0.25)
        self.play(Write(freq_eyeball1))
        self.play(Write(freq_eyeball2))
        self.play(Write(freq_eyeball3))
        self.wait(2)
        self.play(Unwrite(freq_eyeball1), Unwrite(freq_eyeball2), Unwrite(freq_eyeball3))
        self.wait(0.3)

        # multiple sin waves
        self.play(Unwrite(lambda_line), Unwrite(lambda_symbol))
        self.play(Transform(sin_func_text_with_f, multiple_sin_funcs, replace_mobject_with_target_in_scene=True))
        self.wait(0.1)
        self.play(Transform(sin_wave, square_approx, replace_mobject_with_target_in_scene=True))
        self.play(TransformMatchingTex(f_value_unknown, f_alpha_value_unknown, transform_mismatches=True))
        self.wait(10)
        self.play([Wiggle(c, scale_value=1.5) for c in multiple_sin_funcs_constants])
        self.wait(10)

        # is it possible?
        is_it_possible = MathTex(r"\text{Is it possible to find }", r"f_{i}", r"\text{ and }", r"\alpha_{i}", r"\text{ from the graph?}").scale(0.75).center().shift(3 * UP)
        is_it_possible[1][:].set_color(RED)
        is_it_possible[3][:].set_color(RED)
        even_better = MathTex(r"\text{Even better yet, can we find a function }", r"\hat{g}(\xi)", r"\text{ such that}").scale(0.75).move_to(is_it_possible).shift(0.75 * DOWN)
        even_better[1][:].set_color(BLUE)
        kinda_fourier_func = MathTex(r"\hat{g}(", r"\xi_{i}", r")", r"=", r"\alpha_{i}").scale(0.75).move_to(even_better).shift(0.75 * DOWN)
        kinda_fourier_func[0][:].set_color(BLUE)
        kinda_fourier_func[2][:].set_color(BLUE)
        kinda_fourier_func[1][:].set_color(BLUE)
        kinda_fourier_func[4][:].set_color(RED)
        where = MathTex(r"\text{where }", r"\xi_{i}", r"\text{ is some frequency and }", r"\alpha_{i}", r"\text{ is that frequencies ``intensity''?}").scale(0.75).move_to(kinda_fourier_func).shift(0.75 * DOWN)
        where[1][:].set_color(BLUE)
        where[3][:].set_color(RED)
        final_group = Group(axes, multiple_sin_funcs, f_alpha_value_unknown, square_approx)
        self.play(f_alpha_value_unknown.animate.shift(UP), multiple_sin_funcs.animate.shift(6.5 * LEFT))
        self.play(final_group.animate.scale(0.75).shift(3 * DOWN))
        self.play(Write(is_it_possible))
        self.wait(1.5)
        self.play(Write(even_better))
        self.play(Write(kinda_fourier_func))
        self.play(Write(where))
        self.wait(1)
        self.play(Unwrite(is_it_possible, run_time=1))
        self.play(Unwrite(even_better, run_time=1))
        self.play(Unwrite(kinda_fourier_func, run_time=1))
        self.play(Unwrite(where, run_time=1))

        # fourier transformation debut
        yes = MathTex(r"\text{Yes!}").scale(0.75).shift(3 * UP)
        self.wait(10)
        fourier_transform = MathTex(r"\hat{g}(\xi)=\int_{-\infty}^{\infty}g(x)e^{-2\pi ix\xi}dx").scale(0.75).move_to(yes).shift(1.25 * DOWN)
        self.play(Write(yes))
        self.play(Write(fourier_transform))

        # self.add(index_labels(fourier_transform[0]))
        # self.play(Write(fourier_transform))
        self.wait(15)

        # disappear
        self.play(Unwrite(fourier_transform, run_time=0.75), Unwrite(yes, run_time=0.75), Unwrite(axes, run_time=0.75), Unwrite(multiple_sin_funcs, run_time=0.75), Unwrite(f_alpha_value_unknown, run_time=0.75), FadeOut(square_approx, run_time=0.25))
        self.wait(0.5)
