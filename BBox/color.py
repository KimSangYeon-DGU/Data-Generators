import matplotlib
import matplotlib.pyplot as plt

def get_color_bgr(color_name):
    bgr = []
    c = matplotlib.colors.to_rgb(color_name) 
    for i in range(3):
        bgr.append(c[2-i]*255)
    return bgr