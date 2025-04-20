def _rgb255(h: float) -> tuple[int, int, int]:
    r, g, b, a = _hsv_to_rgb(h, 1.0, 1.0, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)


def _hsv_to_rgb(h: float, s: float, v: float, a: float) -> tuple:
    if not s:
        return v, v, v, a

    if h == 1.0:
        h = 0.0

    i = int(h * 6.0)
    f = h * 6.0 - i

    w = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    if i == 0:
        return v, t, w, a
    if i == 1:
        return q, v, w, a
    if i == 2:
        return w, v, t, a
    if i == 3:
        return w, q, v, a
    if i == 4:
        return t, w, v, a
    #  i == 5:
    return v, w, q, a


_gradient_length = 24
_gradient_colors = [_rgb255(i / _gradient_length) for i in range(_gradient_length)]
_tail_colors = [(125, 125, 125)] * 1000
LINEAR_COLORS = _gradient_colors + _tail_colors

DISTINCT_COLORS = [
    (0, 130, 200),  # Blue
    (60, 180, 75),  # Green
    (230, 25, 75),  # Red
    (245, 130, 48),  # Orange
    (145, 30, 180),  # Purple
    (70, 240, 240),  # Cyan
    (240, 50, 230),  # Magenta
    (210, 245, 60),  # Lime
    (250, 190, 190),  # Pink
    (0, 128, 128),  # Teal
    (230, 190, 255),  # Lavender
    (170, 110, 40),  # Brown
    (255, 250, 200),  # Light Yellow
    (128, 0, 0),  # Maroon
    (170, 255, 195),  # Mint
    (128, 128, 0),  # Olive
    (255, 215, 180),  # Apricot
    (0, 0, 128),  # Navy
    (128, 128, 128),  # Grey
    (255, 255, 255),  # White
    (0, 0, 0),  # Black
    (255, 255, 0),  # Yellow
    (255, 153, 204),  # Bubblegum
    (102, 51, 153),  # Deep Purple
] + _tail_colors
