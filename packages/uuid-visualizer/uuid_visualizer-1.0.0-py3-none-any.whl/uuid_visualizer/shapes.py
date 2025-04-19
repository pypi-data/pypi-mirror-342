# shapes.py
"""
Shape-drawing routines for the key-image generator.
Includes triangle overlay (tessellated like honeycomb), dynamic arms, end-of-arm cubes, center shape (with rounded edges), number box, and optional corner plus signs.
"""
import random
import math
from PIL import ImageDraw, ImageFont, Image



def draw_triangle_overlay(draw: ImageDraw.Draw,
                          seed: int,
                          canvas_size: int = 4096,
                          grid_size: int = 12,
                          triangle_size: int = 300,
                          fill_prob: float = 0.5,
                          outline_width: int = 12):
    rng = random.Random(seed)

    base = triangle_size
    height = triangle_size * math.sqrt(3) / 2
    spacing_x = base / 2
    spacing_y = height / 2

    base_pts_up = [(0, -height / 2), (-base / 2, height / 2), (base / 2, height / 2)]
    base_pts_down = [(0, height / 2), (-base / 2, -height / 2), (base / 2, -height / 2)]

    def translate(pts, dx, dy):
        return [(x + dx, y + dy) for x, y in pts]

    def draw_triangle(pts, fill_mode):
        if fill_mode == 1:
            draw.polygon(pts, outline=(255, 255, 255), width=outline_width)
        elif fill_mode == 2:
            draw.polygon(pts, fill=(255, 255, 255))

    cols = int(canvas_size / spacing_x) + 2
    rows = int(canvas_size / spacing_y) + 2

    for row in range(rows):
        for col in range(cols):
            x = spacing_x * col + (spacing_x / 2 if row % 2 else 0)
            y = spacing_y * row

            upward = rng.choice([True, False])
            fill_mode = rng.randint(1, 2)
            base = base_pts_up if upward else base_pts_down

            pts = translate(base, x, y)
            draw_triangle(pts, fill_mode)


def draw_arms(im: Image.Image,
              count: int,
              length: int,
              width: int,
              color: tuple,
              canvas_size: int = 4096,
              rotation_offset: float = 0,
              cube_color: tuple = (255, 0, 255)):
    count = max(3, min(4, count))
    cx = cy = canvas_size // 2

    # Scale arm dimensions up by custom factors
    length *= 2
    width *= 2.4

    arm_layer = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    arm_draw = ImageDraw.Draw(arm_layer)
    rgba = color if len(color) == 4 else (*color, 255)
    arm_draw.rounded_rectangle(
        [(cx - width/2, cy - length), (cx + width/2, cy)],
        radius=int(width/2), fill=rgba)

    for i in range(count):
        angle = (360 / count) * i + rotation_offset
        rotated = arm_layer.rotate(angle, center=(cx, cy))
        im.paste(rotated, (0, 0), rotated)

    draw = ImageDraw.Draw(im)
    outer_size = width * 1.6875 * 0.5  # downscale 25%
    inner_size = outer_size * 0.6
    outer_radius = int(width * 0.3375 * 0.5)
    inner_radius = int(inner_size * 0.2)

    for i in range(count):
        angle_deg = (360 / count) * i + rotation_offset
        angle = math.radians(angle_deg)
        x = cx + math.cos(angle) * (length - width / 2 + 100)
        y = cy + math.sin(angle) * (length - width / 2 + 100)

        outer_box = [(x - outer_size / 2, y - outer_size / 2),
                     (x + outer_size / 2, y + outer_size / 2)]
        inner_box = [(x - inner_size / 2, y - inner_size / 2),
                     (x + inner_size / 2, y + inner_size / 2)]

        draw.rounded_rectangle(outer_box, radius=outer_radius, fill=cube_color)
        draw.rounded_rectangle(inner_box, radius=inner_radius, fill=(0, 0, 0))


def draw_center_shape(draw: ImageDraw.Draw,
                       canvas_size: int,
                       shape_color: tuple,
                       accent_color: tuple,
                       uuid_byte: int):
    cx = cy = canvas_size // 2
    radius = 800  # scaled up slightly
    shape_type = uuid_byte % 2  # 0 = circle, 1 = hexagon (square removed)

    if shape_type == 0:
        draw.ellipse(
            [(cx - radius, cy - radius), (cx + radius, cy + radius)],
            fill=shape_color
        )
    else:
        sides = 6
        angle = 2 * math.pi / sides
        points = [
            (cx + math.cos(i * angle) * radius,
             cy + math.sin(i * angle) * radius)
            for i in range(sides)
        ]
        draw.polygon(points, fill=shape_color)

    # Inner white rounded square with black X
    box_size = 350
    inner_radius = 30
    box = [(cx - box_size/2, cy - box_size/2), (cx + box_size/2, cy + box_size/2)]
    draw.rounded_rectangle(box, radius=inner_radius, fill=(255, 255, 255))
    draw.line([(cx - box_size/3, cy - box_size/3), (cx + box_size/3, cy + box_size/3)], fill=(0, 0, 0), width=12)
    draw.line([(cx + box_size/3, cy - box_size/3), (cx - box_size/3, cy + box_size/3)], fill=(0, 0, 0), width=12)

def draw_auth_box(draw: ImageDraw.Draw, value: int, canvas_size: int):
    num = max(1, min(99, value))
    text = f"{num:02d}"

    box_width = int(675 * 1.25)
    box_height = int(360 * 1.25)
    box_x = 0
    box_y = canvas_size // 2 - box_height // 2

    draw.rectangle(
        [(box_x, box_y), (box_x + box_width, box_y + box_height)],
        fill=(0, 0, 0)
    )

    try:
        font = ImageFont.truetype("arial.ttf", size=480)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = box_x + (box_width - text_w) // 2
    text_y = box_y + (box_height - text_h) // 2 - 100  # adjust upward

    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)


def draw_corner_crosses(draw: ImageDraw.Draw, canvas_size: int, enabled: bool):
    if not enabled:
        return

    size = 250
    thickness = 12
    offset = 350

    positions = [
        (offset, offset),  # top-left
        (canvas_size - offset, offset),  # top-right
        (offset, canvas_size - offset),  # bottom-left
        (canvas_size - offset, canvas_size - offset)  # bottom-right
    ]

    for x, y in positions:
        draw.line([(x - size//2, y), (x + size//2, y)], fill=(0, 0, 0), width=thickness)
        draw.line([(x, y - size//2), (x, y + size//2)], fill=(0, 0, 0), width=thickness)