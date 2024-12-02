import os
import sys


def render():
    quality = 'l'
    if '-high' in sys.argv:
        quality = 'h'
    if '-4k' in sys.argv:
        quality = 'k'
    os.system(f"manim -pq{quality} intro_intro.py IntroIntro")
    os.system(f"manim -pq{quality} intro.py SineWaves")
    os.system(f"manim -pq{quality} ft_example.py FourierTransforms")
    os.system(f"manim -pq{quality} ft_explanation.py FourierTransformInternals")
    os.system(f"manim -pq{quality} ft_applications.py Applications")
    os.system(r"(echo file 'media\videos\intro_intro\2160p60\IntroIntro.mp4' & echo file 'media\videos\intro\2160p60\SineWaves.mp4' & echo file 'media\videos\ft_example\2160p60\FourierTransforms.mp4' & echo file 'media\videos\ft_explanation\2160p60\FourierTransformInternals.mp4' & echo file 'media\videos\ft_applications\2160p60\Applications.mp4' )>list.txt")
    os.system(r"ffmpeg -safe 0 -f concat -i list.txt -c copy media/output.mp4")

if __name__ == '__main__':
    render()
