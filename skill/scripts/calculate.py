"""Magic Circle Calculator

Computes magic circles -- concentric ring arrangements of integers where
each ring and radial line aims to sum to the magic constant M(n).

Renders the result as an ASCII diagram to standard output.

Reference: Andrews, W.S. "Magic Squares and Cubes", Dover (1960), Ch. XII.
"""

import json
import math
from pathlib import Path

from rendering import format_output

CONSTANTS_PATH = Path(__file__).with_name("constants.json")


def magic_constant(order):
    """Magic constant M(n) = n(n^2 + 1) / 2."""
    return order * (order * order + 1) // 2


def load_config(path):
    """Load circle configuration from JSON."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    return raw


def distribute_values(order, rings):
    """Place integers 1..n^2 into concentric rings."""
    total = order * order
    values = list(range(1, total + 1))
    result = []
    pos = 0
    for ring in rings:
        count = min(ring["points"], total - pos)
        if count <= 0:
            break
        segment = values[pos:pos + count]
        shift = (ring.get("offset_deg", 0) * count) // 360
        result.append(segment[shift:] + segment[:shift])
        pos += count
    return result


def render_diagram(circle, width, height, glyphs):
    """Render the circle arrangement as ASCII art."""
    grid = [[" "] * width for _ in range(height)]
    cx, cy = width // 2, height // 2
    n_rings = len(circle)

    for ri, ring in enumerate(circle):
        r = (ri + 1) * min(cx, cy) // (n_rings + 1)
        glyph = glyphs[ri % len(glyphs)] if glyphs else "."
        for deg in range(360):
            a = math.radians(deg)
            x, y = int(cx + r * math.cos(a)), int(cy + r * math.sin(a))
            if 0 <= x < width and 0 <= y < height and grid[y][x] == " ":
                grid[y][x] = glyph
        for i, val in enumerate(ring):
            a = 2 * math.pi * i / len(ring)
            x, y = int(cx + r * math.cos(a)), int(cy + r * math.sin(a))
            for j, ch in enumerate(str(val)):
                if 0 <= x + j < width and 0 <= y < height:
                    grid[y][x + j] = ch

    return "\n".join("".join(row).rstrip() for row in grid)


def main():
    config = load_config(CONSTANTS_PATH)
    order = config["circle_order"]
    rings = config["rings"]
    rendering = config["rendering"]
    mc = magic_constant(order)

    circle = distribute_values(order, rings)
    glyphs = list(rendering.get("ring_glyphs", "."))
    diagram = render_diagram(
        circle, rendering["canvas_width"], rendering["canvas_height"], glyphs
    )

    output = format_output(diagram)
    print(output)
    print(f"\nMagic constant M({order}) = {mc}")
    total = sum(len(r) for r in circle)
    print(f"Values placed: {total}/{order * order}")


if __name__ == "__main__":
    main()
