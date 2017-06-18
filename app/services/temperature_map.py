from colorsys import hsv_to_rgb

from app.utils import rgb_to_hex


def calculate_color(value, interval):
    if interval == 0:
        return rgb_to_hex(1, 0, 0)
    
    hue = 240 - 240 * value / interval
    return rgb_to_hex(*hsv_to_rgb(hue / 360, 1, 1))
