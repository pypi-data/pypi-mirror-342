# main.py
"""
Test script for the key-image generator.
Creates a 4096×4096 PNG with:
 - triangle overlay
 - arms and cubes
 - center shape (rounded edges, internal white X box)
 - UUID-based unique color picking
 - number box
 - corner plus signs
"""

import sys
import uuid
from PIL import Image, ImageDraw
from .palettes import BACKGROUND_COLORS, ARM_COLORS, CUBE_COLORS, CENTER_COLORS
from .shapes import draw_triangle_overlay, draw_arms, draw_center_shape, draw_auth_box, draw_corner_crosses

CANVAS = 4096

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <uuid> <output_path>")
        sys.exit(1)

    u_str = sys.argv[1]
    out_path = sys.argv[2]

    # UUID → bytes
    u = uuid.UUID(u_str)
    raw = u.bytes
    params = list(raw)

    # Unique color assignment
    used_indexes = set()

    def pick_unique_color(palette, byte_val):
        for i in range(len(palette)):
            idx = (byte_val + i) % len(palette)
            if idx not in used_indexes:
                used_indexes.add(idx)
                return palette[idx]
        return palette[byte_val % len(palette)]

    bg_color     = pick_unique_color(BACKGROUND_COLORS, params[0])
    arm_color    = pick_unique_color(ARM_COLORS, params[1])
    cube_color   = pick_unique_color(CUBE_COLORS, params[2])
    center_color = pick_unique_color(CENTER_COLORS, params[3])
    center_accent = pick_unique_color(CENTER_COLORS, params[9])

    # Arm configuration (scaled down)
    arm_count  = (params[4] % 3) + 3
    arm_length = 900 + (params[5] % 200)     # smaller range
    arm_width  = 250 + (params[6] % 100)     # thinner arms

    # Triangle overlay configuration
    tri_seed   = params[7]
    fill_prob  = (params[8] / 255.0) * 0.8 + 0.1

    # Auth number 01–99
    auth_number = (params[11] % 99) + 1

    # Create base canvas
    im = Image.new("RGB", (CANVAS, CANVAS), bg_color)
    draw = ImageDraw.Draw(im)

    # Draw triangle overlay
    draw_triangle_overlay(
        draw,
        seed=tri_seed,
        canvas_size=CANVAS,
        triangle_size=300,
        fill_prob=fill_prob,
        outline_width=12
    )

    # Draw arms and cubes
    draw_arms(
        im,
        count=arm_count,
        length=arm_length,
        width=arm_width,
        color=arm_color,
        canvas_size=CANVAS,
        rotation_offset=45,
        cube_color=cube_color
    )

    # Draw center shape (rounded, with white X box)
    draw_center_shape(
        draw,
        canvas_size=CANVAS,
        shape_color=center_color,
        accent_color=center_accent,
        uuid_byte=params[10]
    )

    # Draw number box
    draw_auth_box(draw, auth_number, canvas_size=CANVAS)

    # Draw corner pluses if enabled
    draw_corner_crosses(draw, canvas_size=CANVAS, enabled=params[12] % 2 == 1)

    # Save result
    im.save(out_path)
    print(f"Generated key image: {out_path}")

if __name__ == '__main__':
    main()
