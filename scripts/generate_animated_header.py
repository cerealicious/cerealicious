"""
Cerealicious Animated Header Generator
Generates a zero-g floating mechanical keyboard typing 'cerealicious'
with colorful cereal loops and marshmallows popping out on keypresses.

Requires: Pillow (PIL)
Usage: py scripts/generate_animated_header.py
"""

import math
import random
import os
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# CONFIGURATION & THEME
# ==========================================
WIDTH = 840
HEIGHT = 300
FPS = 25
TEXT = "cerealicious"
TOTAL_KEYS = len(TEXT)

# Timing (in frames)
KEY_INTERVAL = 4       # Frames between key presses (~100 WPM)
KEY_PRESS_DURATION = 3 # How long key stays pressed down
POST_TYPE_HOLD = 35    # Frames to admire the floating cereal before looping
TOTAL_FRAMES = (TOTAL_KEYS * KEY_INTERVAL) + POST_TYPE_HOLD

# Color Palette (Zero-G Dark Space with Pastel Cereal Accents)
BG_COLOR = (13, 17, 23)        # GitHub Dark Slate (#0D1117)
CHASSIS_BG = (22, 27, 34)      # Darker slate card (#161B22)
CHASSIS_BORDER = (48, 54, 61)  # GitHub border (#30363D)

KEYCAP_TOP_NORMAL = (40, 46, 56)
KEYCAP_SLOPE_NORMAL = (28, 33, 40)
KEYCAP_TEXT_NORMAL = (201, 209, 217)

KEYCAP_TOP_PRESSED = (65, 75, 95)
KEYCAP_SLOPE_PRESSED = (38, 44, 54)
KEYCAP_TEXT_PRESSED = (255, 255, 255)

# Cereal Loop Flavors (Pastel Froot Loops & Marshmallows)
CEREAL_COLORS = [
    (255, 107, 139),  # Berry Pink
    (255, 184, 77),   # Sunshine Lemon / Honey Puff
    (107, 203, 119),  # Crisp Lime
    (77, 150, 255),   # Blueberry Sky
    (155, 93, 229),   # Grape Violet
    (255, 145, 0),    # Citrus Tangerine
]

MARSHMALLOW_COLORS = [
    (255, 220, 230),  # Pink Heart
    (220, 245, 255),  # Blue Moon
    (255, 250, 210),  # Yellow Star
    (230, 255, 235),  # Mint Clover
]

# Layout metrics
KEY_W = 44
KEY_H = 46
KEY_GAP = 12
KEY_BEVEL = 6
KEY_RADIUS = 7

KEYBOARD_TOTAL_W = TOTAL_KEYS * KEY_W + (TOTAL_KEYS - 1) * KEY_GAP
START_X = (WIDTH - KEYBOARD_TOTAL_W) // 2
BASE_Y = HEIGHT - 85


def get_font(size, bold=False):
    """Attempt to load a crisp modern system font with fallback."""
    font_names = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for font_path in font_names:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    return ImageFont.load_default()


FONT_KEYCAP = get_font(18, bold=True)
FONT_SUBTITLE = get_font(13, bold=False)
FONT_TAG = get_font(11, bold=True)


class CerealParticle:
    """A single piece of cereal floating into zero-gravity."""
    def __init__(self, x, y, start_frame):
        self.x = x
        self.y = y
        self.start_frame = start_frame
        
        # Physics: initial upward burst + sideways drift in zero-G
        angle = random.uniform(-math.pi * 0.85, -math.pi * 0.15)
        speed = random.uniform(4.5, 9.5)
        self.vx = math.cos(angle) * speed * 0.7
        self.vy = math.sin(angle) * speed
        
        # Zero-G micro-gravity / air resistance
        self.gravity = 0.16
        self.friction = 0.985
        
        # Appearance
        self.shape = random.choice(["loop", "loop", "loop", "puff", "marshmallow"])
        if self.shape == "loop":
            self.color = random.choice(CEREAL_COLORS)
            self.radius = random.uniform(7.0, 9.5)
            self.hole_ratio = random.uniform(0.38, 0.46)
        elif self.shape == "puff":
            self.color = random.choice(CEREAL_COLORS)
            self.radius = random.uniform(5.5, 7.5)
            self.hole_ratio = 0
        else: # Marshmallow star / square
            self.color = random.choice(MARSHMALLOW_COLORS)
            self.radius = random.uniform(6.0, 8.0)
            self.hole_ratio = 0
            
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-7, 7)
        self.wobble_freq = random.uniform(0.08, 0.15)
        self.wobble_phase = random.uniform(0, math.pi * 2)

    def get_state(self, current_frame):
        """Compute position and rotation for the current frame."""
        age = current_frame - self.start_frame
        if age < 0:
            return None  # Not spawned yet
        
        # Simulate trajectory
        curr_x = self.x
        curr_y = self.y
        curr_vx = self.vx
        curr_vy = self.vy
        
        for _ in range(age):
            curr_x += curr_vx
            curr_y += curr_vy
            curr_vy += self.gravity
            curr_vx *= self.friction
            curr_vy *= self.friction
        
        # Add a subtle zero-g sine wobble
        wobble_x = math.sin(age * self.wobble_freq + self.wobble_phase) * 2.0
        wobble_y = math.cos(age * self.wobble_freq + self.wobble_phase) * 1.5
        
        rot = self.rotation + (age * self.rot_speed)
        
        # Fade out gently if near boundary or end of life
        alpha = 1.0
        if curr_y < 25:
            alpha = max(0.0, curr_y / 25.0)
        
        return {
            "x": curr_x + wobble_x,
            "y": curr_y + wobble_y,
            "rot": rot,
            "radius": self.radius,
            "color": self.color,
            "shape": self.shape,
            "hole_ratio": self.hole_ratio,
            "alpha": alpha
        }


def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    """Draw a smooth rounded rectangle."""
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)


def draw_keycap(draw, x, y, letter, is_pressed, key_index, current_frame):
    """Draw a 3D mechanical keycap with bevel, legend, and press displacement."""
    press_offset = 5 if is_pressed else 0
    top_y = y + press_offset
    
    # Underglow LED lighting when pressed or after typed
    typed_time = key_index * KEY_INTERVAL
    if current_frame >= typed_time:
        # Soft underglow spot
        glow_alpha = 0.5 if is_pressed else 0.18
        accent = CEREAL_COLORS[key_index % len(CEREAL_COLORS)]
        glow_bbox = (x - 6, y + 10, x + KEY_W + 6, y + KEY_H + 14)
        glow_color = (
            int(accent[0] * glow_alpha + BG_COLOR[0] * (1 - glow_alpha)),
            int(accent[1] * glow_alpha + BG_COLOR[1] * (1 - glow_alpha)),
            int(accent[2] * glow_alpha + BG_COLOR[2] * (1 - glow_alpha))
        )
        draw_rounded_rect(draw, glow_bbox, radius=KEY_RADIUS + 3, fill=glow_color)

    # Keycap bottom bevel/skirt (chassis seat)
    skirt_bbox = (x, top_y + KEY_BEVEL, x + KEY_W, top_y + KEY_H)
    skirt_color = KEYCAP_SLOPE_PRESSED if is_pressed else KEYCAP_SLOPE_NORMAL
    draw_rounded_rect(draw, skirt_bbox, radius=KEY_RADIUS, fill=skirt_color)

    # Keycap top surface
    top_margin = 3
    top_h = KEY_H - KEY_BEVEL - top_margin
    top_bbox = (x + top_margin, top_y + top_margin, x + KEY_W - top_margin, top_y + top_margin + top_h)
    top_color = KEYCAP_TOP_PRESSED if is_pressed else KEYCAP_TOP_NORMAL
    
    # Border for mechanical definition
    border_color = (75, 85, 105) if is_pressed else (55, 62, 75)
    draw_rounded_rect(draw, top_bbox, radius=KEY_RADIUS - 2, fill=top_color, outline=border_color, width=1)

    # Keycap legend (letter)
    text = letter.upper()
    text_color = KEYCAP_TEXT_PRESSED if is_pressed else KEYCAP_TEXT_NORMAL
    
    # Center text
    bbox = FONT_KEYCAP.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = top_bbox[0] + (top_bbox[2] - top_bbox[0] - tw) // 2
    ty = top_bbox[1] + (top_bbox[3] - top_bbox[1] - th) // 2 - 2
    draw.text((tx, ty), text, font=FONT_KEYCAP, fill=text_color)


def draw_cereal_particle(draw, state):
    """Draw a floating cereal loop or marshmallow piece."""
    if not state or state["alpha"] <= 0.05:
        return
        
    x = state["x"]
    y = state["y"]
    r = state["radius"]
    color = state["color"]
    shape = state["shape"]
    
    # Outer bound check
    if x < -20 or x > WIDTH + 20 or y < -20 or y > HEIGHT + 20:
        return

    if shape == "loop":
        # Froot Loop donut: outer colored circle, inner cutout with subtle shading
        bbox_outer = (x - r, y - r, x + r, y + r)
        draw.ellipse(bbox_outer, fill=color)
        
        # Subtle 3D highlight on top-left of ring
        hl_color = (
            min(255, int(color[0] * 1.35)),
            min(255, int(color[1] * 1.35)),
            min(255, int(color[2] * 1.35))
        )
        draw.arc(bbox_outer, start=200, end=340, fill=hl_color, width=2)
        
        # Inner donut hole filled with background (or chassis if low)
        hole_r = r * state["hole_ratio"]
        hole_bg = BG_COLOR
        bbox_inner = (x - hole_r, y - hole_r, x + hole_r, y + hole_r)
        draw.ellipse(bbox_inner, fill=hole_bg)

    elif shape == "puff":
        # Solid crunchy cereal puff (golden or pastel sphere)
        bbox = (x - r, y - r, x + r, y + r)
        draw.ellipse(bbox, fill=color)
        # Highlight
        hl_r = r * 0.4
        draw.ellipse((x - r*0.4, y - r*0.4, x - r*0.4 + hl_r, y - r*0.4 + hl_r), fill=(255, 255, 255))
        
    elif shape == "marshmallow":
        # Lucky Charms diamond/star marshmallow
        pts = [
            (x, y - r),
            (x + r * 0.8, y),
            (x, y + r),
            (x - r * 0.8, y)
        ]
        draw.polygon(pts, fill=color, outline=(255, 255, 255))


def render_all_frames():
    """Simulate and render all animation frames."""
    # Seed deterministic random for clean reproducible aesthetic
    random.seed(42)
    
    # Pre-generate cereal particles for each keystroke
    particles = []
    for key_idx, char in enumerate(TEXT):
        press_frame = key_idx * KEY_INTERVAL
        key_x = START_X + key_idx * (KEY_W + KEY_GAP) + (KEY_W // 2)
        key_y = BASE_Y + 5
        
        # Each press spawns 3 to 5 cereal pieces
        num_pieces = random.randint(3, 5)
        for _ in range(num_pieces):
            particles.append(CerealParticle(key_x, key_y, press_frame))

    frames = []
    
    # Zero-G floating background stars/dots
    ambient_stars = [
        (random.randint(20, WIDTH - 20), random.randint(15, HEIGHT - 100), random.uniform(0.6, 2.0), random.choice(CEREAL_COLORS))
        for _ in range(24)
    ]
    
    print(f"Rendering {TOTAL_FRAMES} frames at {WIDTH}x{HEIGHT}...")
    
    for frame_idx in range(TOTAL_FRAMES):
        img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        # Subtle Zero-G Ambient Float for Keyboard Chassis
        # Slow floating sine wave: bobbing up and down gently
        float_offset_y = math.sin(frame_idx * 0.1) * 3.5
        current_base_y = BASE_Y + float_offset_y

        # Draw ambient zero-G stardust / micro-particles
        for star_x, star_y, star_r, star_col in ambient_stars:
            star_float_y = star_y + math.sin((frame_idx + star_x) * 0.08) * 4.0
            dimmed_col = (star_col[0] // 4, star_col[1] // 4, star_col[2] // 4)
            draw.ellipse((star_x - star_r, star_float_y - star_r, star_x + star_r, star_float_y + star_r), fill=dimmed_col)

        # Draw subtle header backdrop card / chassis
        chassis_pad = 16
        chassis_bbox = (
            START_X - chassis_pad,
            int(current_base_y - chassis_pad),
            START_X + KEYBOARD_TOTAL_W + chassis_pad,
            int(current_base_y + KEY_H + chassis_pad + 2)
        )
        draw_rounded_rect(draw, chassis_bbox, radius=16, fill=CHASSIS_BG, outline=CHASSIS_BORDER, width=1)
        
        # Top banner labels: "MECHANICAL SWITCH: LUBED BERRY LINEARS" & "BOWL STATUS: ZERO-G"
        draw.text((START_X - 10, int(current_base_y - 36)), "SWITCH: CHERRY MX BERRY // PROFILE: OEM ZERO-G", font=FONT_TAG, fill=(110, 118, 129))
        draw.text((START_X + KEYBOARD_TOTAL_W - 135, int(current_base_y - 36)), "STATUS: FLOATING 🥣", font=FONT_TAG, fill=(255, 184, 77))

        # Draw floating cereal pieces that are behind keycaps or in mid-air
        for p in particles:
            st = p.get_state(frame_idx)
            if st and st["y"] < current_base_y:
                draw_cereal_particle(draw, st)

        # Draw all 12 keycaps
        for key_idx, char in enumerate(TEXT):
            press_frame = key_idx * KEY_INTERVAL
            is_pressed = (press_frame <= frame_idx < press_frame + KEY_PRESS_DURATION)
            
            key_x = START_X + key_idx * (KEY_W + KEY_GAP)
            draw_keycap(draw, key_x, int(current_base_y), char, is_pressed, key_idx, frame_idx)

        # Draw cereal pieces that popped in front of the keycaps
        for p in particles:
            st = p.get_state(frame_idx)
            if st and st["y"] >= current_base_y:
                draw_cereal_particle(draw, st)
                
        # Draw playful terminal cursor at current typing position
        typed_count = min(TOTAL_KEYS, frame_idx // KEY_INTERVAL)
        if typed_count < TOTAL_KEYS and (frame_idx // 3) % 2 == 0:
            cursor_x = START_X + typed_count * (KEY_W + KEY_GAP) + KEY_W + 4
            cursor_y = int(current_base_y + 12)
            draw.rectangle((cursor_x, cursor_y, cursor_x + 3, cursor_y + KEY_H - 24), fill=(255, 107, 139))
            
        frames.append(img)

    return frames


def main():
    os.makedirs("assets", exist_ok=True)
    frames = render_all_frames()
    
    output_path = os.path.join("assets", "header.gif")
    print(f"Saving animated GIF to {output_path} (duration={1000 // FPS}ms/frame)...")
    
    # Convert frames to palette for optimal GIF compression and crisp edges
    palette_frames = []
    for f in frames:
        p_frame = f.convert("P", palette=Image.ADAPTIVE, colors=128)
        palette_frames.append(p_frame)
        
    palette_frames[0].save(
        output_path,
        save_all=True,
        append_images=palette_frames[1:],
        optimize=True,
        duration=1000 // FPS,
        loop=0
    )
    
    file_size_kb = os.path.getsize(output_path) / 1024
    print(f"Successfully generated {output_path} ({file_size_kb:.1f} KB)")


if __name__ == "__main__":
    main()

