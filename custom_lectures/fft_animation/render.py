import os
import sys

def render():
    quality = 'l'
    if '-high' in sys.argv:
        quality = 'h'
    if '-4k' in sys.argv:
        quality = 'k'
    os.system(f"manim -pq{quality} scene.py SineWaves")

if __name__ == '__main__':
    render()
