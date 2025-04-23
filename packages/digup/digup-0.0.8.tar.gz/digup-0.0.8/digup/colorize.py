"""
For 8-bit color, the syntax is

    \033[<prefix>;<mode>;<value>m

Where:
- \033 is the escape char
- prefix is 38 (foreground) or 48 for background
- mode is 5 (8-bits, 256 colors) or 2 (24-bits, True Colors)
- value is a value
- \033[0m reset the color

"""

import colorsys


def colorize(text: str, foreground: int | None = None, background: int | None = None) -> str:
    """
    :param text:
    :param foreground: [0, 255]
    :param background: [0, 255]
    :return:
    """
    if foreground is None and background is None:
        return text

    colors = []
    if foreground is not None:
        colors.append(f"38;5;{foreground}")
    if background is not None:
        colors.append(f"48;5;{background}")

    return f"\033[{';'.join(colors)}m{text}\033[0m"


def rgb_to_ansi(r: int, g: int, b: int) -> int:
    """ "
    r,g,c are the coordinates in the 6x6x6 cube [0, 5]
    """
    return 16 + (36 * r) + (6 * g) + b


def hue_gradient(size: int):
    for index in range(size):
        r, g, b = colorsys.hsv_to_rgb(index / size, 1, 1)
        yield rgb_to_ansi(int(r * 5 + 0.5), int(g * 5 + 0.5), int(b * 5 + 0.5))


if __name__ == "__main__":
    for i in range(256):
        print(colorize(f" {i:3} ", foreground=i), end="")
        if (i + 1) % 16 == 0:
            print()
    print()
    for i in range(256):
        print(colorize(f" {i:3} ", background=i), end="")
        if (i + 1) % 16 == 0:
            print()
    print()

    for ansi in hue_gradient(32):
        print(colorize(f" {ansi:3} ", ansi), end="")
