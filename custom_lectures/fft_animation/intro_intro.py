from manim import *


class IntroIntro(Scene):

    def construct(self):
        fourier_transforms_text = Tex("Fourier Transforms!").scale(0.8)
        fourier_transform_eq = MathTex(r"\hat{f}(", r"\xi", r")", r"=", r"\int_{-\infty}^{\infty}", r"f(x)",
                                       r"e^{-2\pi i", r"x", r"\xi}", r"dx", color=WHITE)
        math_magic = MathTex(r"\text{Math }\Leftrightarrow\text{ Magic}")

        self.play(Write(fourier_transforms_text))
        self.wait(5)
        self.play(ReplacementTransform(fourier_transforms_text, fourier_transform_eq))

        self.wait(4)
        self.play(Unwrite(fourier_transform_eq))
        self.play(Write(math_magic))
        self.wait(6)
        self.play(Unwrite(math_magic))
