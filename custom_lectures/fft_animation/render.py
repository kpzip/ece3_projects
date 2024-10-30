import os

def render():
    os.system(r"manim -pql scene.py SineWaves")

if __name__ == '__main__':
    render()
