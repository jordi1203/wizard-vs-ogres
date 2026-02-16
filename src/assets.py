
import pygame
import math
import random
from src.config import *

def draw_wizard(surface, x, y, facing_right, is_casting=False, wand_color=(255, 255, 255)):
    """Draws a much more detailed Wizard."""
    
    # Body Colors with gradients (simulated by layering)
    robe_base = (0, 0, 180)
    robe_highlight = (50, 50, 220)
    skin_tone = (255, 220, 180)
    
    direction = 1 if facing_right else -1
    
    # Animation: Breathing/Idle
    t = pygame.time.get_ticks()
    breath = math.sin(t / 500) * 3
    
    # --- Aura (Epic Effect) ---
    if is_casting or wand_color != (255, 255, 255):
        # Draw pulsing aura
        aura_radius = 40 + math.sin(t/200) * 5
        s = pygame.Surface((100, 100), pygame.SRCALPHA)
        r, g, b = wand_color[:3]
        pygame.draw.circle(s, (r, g, b, 50), (50, 50), aura_radius)
        surface.blit(s, (x - 50, y - 50 - 20))

    # --- Cape (Flowing) ---
    cape_points = [
        (x - 10, y - 60), # Neck
        (x + 10, y - 60),
        (x + 25 * (-direction) + math.sin(t/300)*5, y - 5 + breath), # Bottom corner out
        (x + 5 * (-direction), y - 5 + breath) # Bottom corner in
    ]
    pygame.draw.polygon(surface, (50, 0, 70), cape_points)
    
    # --- Robe (Body) ---
    body_rect = pygame.Rect(x - PLAYER_SIZE // 2, y - PLAYER_SIZE + breath, PLAYER_SIZE, PLAYER_SIZE)
    
    # Gradient-like shading for robe
    # Main
    points = [
        (x - 20, y - 65 + breath), 
        (x + 20, y - 65 + breath), 
        (x + 25, y), 
        (x - 25, y)
    ]
    pygame.draw.polygon(surface, robe_base, points)
    # Highlight strip
    pygame.draw.line(surface, robe_highlight, (x - 10, y - 65 + breath), (x - 12 + direction*5, y), 8)
    
    # Gold Trim with Runes (simulated dots)
    pygame.draw.line(surface, (255, 215, 0), (x - 25, y), (x + 25, y), 4) # Hem
    for i in range(-20, 21, 10):
        pygame.draw.circle(surface, (0, 255, 255), (x + i, y - 2), 2) # Glowing rune dots

    # --- Head ---
    head_y = y - 70 + breath
    
    # Beard (Epic Long Beard)
    beard_color = (255, 255, 255)
    off = math.sin(t / 400) * 5
    beard_points = [
        (x - 15, head_y + 5),
        (x + 15, head_y + 5),
        (x + (15 * direction) + off, head_y + 35), 
        (x + off, head_y + 25)
    ]
    pygame.draw.polygon(surface, beard_color, beard_points)

    # Face
    pygame.draw.circle(surface, skin_tone, (x, int(head_y)), 15)
    
    # --- Hat (Wizard) ---
    hat_color = (20, 20, 100)
    hat_y = head_y - 10
    
    # Brim (Curved)
    pygame.draw.ellipse(surface, hat_color, (x - 25, hat_y, 50, 15))
    
    # Cone (Bent/Crumbled look)
    hat_tip_x = x - (30 * direction) + math.sin(t/600)*2
    hat_tip_y = hat_y - 50
    pygame.draw.polygon(surface, hat_color, [
        (x - 18, hat_y + 5),
        (x + 18, hat_y + 5),
        (x, hat_y - 25), # Mid break
        (hat_tip_x, hat_tip_y)
    ])
    
    # --- Eyes (Glowing) ---
    eye_x = x + (8 * direction)
    pygame.draw.circle(surface, (0, 0, 0), (eye_x, int(head_y)), 4)
    # Glowing pupils
    pygame.draw.circle(surface, wand_color, (eye_x + direction, int(head_y)), 2)

    # --- Staff (Epic) ---
    staff_x = x + (35 * direction)
    staff_y = y - 40 + breath
    
    # Stick
    pygame.draw.line(surface, (80, 50, 20), (staff_x, staff_y + 40), (staff_x + 5*direction, staff_y - 40), 4)
    
    # Crystal Holder claw
    top_x = staff_x + 5*direction
    top_y = staff_y - 40
    pygame.draw.circle(surface, (200, 200, 200), (top_x, top_y + 5), 6) # Metal ring
    
    # Crystal
    crystal_glow = wand_color
    pulse = (math.sin(t/150) + 1) * 3 # 0 to 6
    if is_casting: pulse += 5
    
    pygame.draw.circle(surface, crystal_glow, (top_x, top_y), 6 + int(pulse/2))
    pygame.draw.circle(surface, (255, 255, 255), (top_x, top_y), 4)
    
    # Floating Particles around staff
    if is_casting:
        for _ in range(3):
            rx = top_x + random.randint(-15, 15)
            ry = top_y + random.randint(-15, 15)
            pygame.draw.circle(surface, crystal_glow, (rx, ry), 2)

    return (top_x, top_y) # Exact tip position

def draw_scaled_wizard(surface, x, y, scale=1.0):
    """Draws the wizard scaled up for menus/intros."""
    w, h = 300, 300
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    
    # Draw at center of temp surface
    # Feet at 280 (leaving room). Center X at 150.
    # Wand Color: RED FIRE (255, 69, 0)
    draw_wizard(s, 150, 280, facing_right=True, is_casting=True, wand_color=(255, 69, 0))
    
    if scale != 1.0:
        s = pygame.transform.scale(s, (int(w*scale), int(h*scale)))
        
    rect = s.get_rect(midbottom=(x, y))
    surface.blit(s, rect)


def draw_ogre(surface, x, y, facing_right, scale=1.0, tick=0, is_attacking=False, attack_phase=0.0):
    """Draws a Green Ogre with rich tones."""
    _draw_monster_base(surface, x, y, facing_right, scale, 
                       skin_color=(80, 150, 50), 
                       outfit_color=(120, 65, 20), 
                       weapon="CLUB", tick=tick, is_attacking=is_attacking, attack_phase=attack_phase)

def draw_goblin(surface, x, y, facing_right, scale=0.8, tick=0, is_attacking=False, attack_phase=0.0):
    """Draws a small, fast Goblin."""
    _draw_monster_base(surface, x, y, facing_right, scale, 
                       skin_color=(150, 200, 50), 
                       outfit_color=(100, 50, 50), 
                       weapon="DAGGER",
                       is_goblin=True, tick=tick, is_attacking=is_attacking, attack_phase=attack_phase)

def draw_troll(surface, x, y, facing_right, scale=1.3, tick=0, is_attacking=False, attack_phase=0.0):
    """Draws a large, regenerating Troll."""
    _draw_monster_base(surface, x, y, facing_right, scale, 
                       skin_color=(100, 100, 120), 
                       outfit_color=(50, 50, 50), 
                       weapon="ROCK", tick=tick, is_attacking=is_attacking, attack_phase=attack_phase)

def draw_skeleton(surface, x, y, facing_right, scale=1.0, tick=0, is_attacking=False, attack_phase=0.0):
    """Draws a detailed Skeleton Archer with articulated bones, hood, and quiver."""
    direction = 1 if facing_right else -1
    
    w, h = 300, 300 
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w//2, h - 10
    
    # Animation
    walk_speed = tick / 150
    if is_attacking:
        walk_speed = 0
        leg_l_off = 0
        leg_r_off = 0
    else:
        stride = 10
        leg_l_off = math.sin(walk_speed) * stride
        leg_r_off = math.sin(walk_speed + math.pi) * stride

    # Color Palette
    BONE = (230, 225, 215)
    BONE_SHADOW = (180, 175, 165)
    BONE_HIGHLIGHT = (245, 242, 235)
    JOINT = (200, 195, 185)
    EYE_GLOW = (50, 255, 80)
    HOOD_COLOR = (40, 35, 45)
    HOOD_EDGE = (60, 55, 65)
    
    # --- Ghostly Aura ---
    aura_s = pygame.Surface((80, 120), pygame.SRCALPHA)
    aura_pulse = int(15 + math.sin(tick / 200) * 8)
    pygame.draw.ellipse(aura_s, (50, 255, 80, aura_pulse), (0, 0, 80, 120))
    s.blit(aura_s, (cx - 40, cy - 140))
    
    # --- LEGS (Articulated Femur + Tibia) ---
    leg_h = 40
    for leg_idx, leg_off in enumerate([leg_l_off, leg_r_off]):
        lx = cx + (-10 if leg_idx == 0 else 10) + int(leg_off * direction)
        shade = BONE_SHADOW if leg_idx == 0 else BONE
        
        # Femur (upper)
        knee_y = cy - leg_h // 2
        pygame.draw.line(s, shade, (lx + 3, cy - leg_h), (lx + 3, knee_y), 5)
        # Knee joint
        pygame.draw.circle(s, JOINT, (lx + 3, knee_y), 4)
        # Tibia (lower)
        foot_x = lx + 3 + int(leg_off * direction * 0.3)
        pygame.draw.line(s, shade, (lx + 3, knee_y), (foot_x, cy - 2), 4)
        # Foot bones
        pygame.draw.line(s, shade, (foot_x, cy - 2), (foot_x + 6 * direction, cy), 3)
    
    # --- PELVIS (Hip bone) ---
    pelvis_y = cy - leg_h
    pygame.draw.ellipse(s, BONE, (cx - 16, pelvis_y - 8, 32, 12))
    # Hip sockets
    pygame.draw.circle(s, BONE_SHADOW, (cx - 10, pelvis_y - 2), 3)
    pygame.draw.circle(s, BONE_SHADOW, (cx + 10, pelvis_y - 2), 3)
    
    # --- SPINE (Individual Vertebrae) ---
    spine_bot = pelvis_y - 8
    spine_top = spine_bot - 40
    num_vert = 8
    for vi in range(num_vert):
        vy = spine_bot - (vi * (spine_bot - spine_top) // num_vert)
        vert_w = 6 - vi * 0.3
        pygame.draw.ellipse(s, BONE, (cx - int(vert_w), vy - 2, int(vert_w * 2), 5))
        pygame.draw.line(s, BONE_SHADOW, (cx, vy - 2), (cx, vy + 3), 2)
    
    # --- RIBCAGE (5 pairs with sternum) ---
    # Sternum
    sternum_top = spine_top + 5
    sternum_bot = spine_top + 35
    pygame.draw.line(s, BONE, (cx, sternum_top), (cx, sternum_bot), 3)
    
    for i in range(5):
        ry = sternum_top + 3 + (i * 7)
        rib_w = 14 - i * 1
        # Left rib (curved)
        pygame.draw.arc(s, BONE, (cx - rib_w - 2, ry - 3, rib_w + 2, 8), 0, 3.14, 2)
        # Right rib
        pygame.draw.arc(s, BONE, (cx, ry - 3, rib_w + 2, 8), 0, 3.14, 2)
    
    # --- QUIVER (on back) ---
    quiver_x = cx - 20 * direction
    quiver_y = spine_top + 5
    # Quiver body
    pygame.draw.rect(s, (100, 60, 30), (quiver_x - 4, quiver_y, 8, 35))
    pygame.draw.rect(s, (80, 45, 20), (quiver_x - 4, quiver_y, 8, 35), 1)
    # Arrow shafts sticking out
    for ai in range(3):
        ax = quiver_x - 2 + ai * 2
        pygame.draw.line(s, (160, 140, 100), (ax, quiver_y), (ax, quiver_y - 12), 1)
        # Arrowhead
        pygame.draw.polygon(s, (180, 180, 180), [(ax - 1, quiver_y - 12), (ax + 1, quiver_y - 12), (ax, quiver_y - 16)])
    
    # --- SKULL (Detailed) ---
    head_y = spine_top - 22
    
    # Hood (ragged fabric)
    hood_pts = [
        (cx - 22, head_y + 5),
        (cx - 18, head_y - 22),
        (cx, head_y - 28),
        (cx + 18, head_y - 22),
        (cx + 22, head_y + 5),
        (cx + 15, head_y + 12),
        (cx - 15, head_y + 12),
    ]
    pygame.draw.polygon(s, HOOD_COLOR, hood_pts)
    # Hood edge highlight
    pygame.draw.lines(s, HOOD_EDGE, False, hood_pts[:5], 2)
    # Tattered bottom edge
    for ti in range(-15, 16, 6):
        tear_len = random.Random(ti + 42).randint(3, 8)
        pygame.draw.line(s, HOOD_COLOR, (cx + ti, head_y + 12), (cx + ti, head_y + 12 + tear_len), 2)
    
    # Cranium 
    pygame.draw.circle(s, BONE, (cx, head_y), 15)
    pygame.draw.circle(s, BONE_HIGHLIGHT, (cx - 3, head_y - 5), 6)  # Forehead highlight
    
    # Cheekbones
    pygame.draw.circle(s, BONE_SHADOW, (cx - 8, head_y + 4), 4)
    pygame.draw.circle(s, BONE_SHADOW, (cx + 8, head_y + 4), 4)
    
    # Eye sockets (deep, dark with green glow)
    for es in [-1, 1]:
        ex = cx + es * 6
        pygame.draw.circle(s, (10, 5, 5), (ex, head_y - 1), 5)  # Socket
        # Green eerie glow
        glow_s = pygame.Surface((14, 14), pygame.SRCALPHA)
        glow_alpha = 120 + int(math.sin(tick / 150 + es) * 40)
        pygame.draw.circle(glow_s, (*EYE_GLOW, max(0, min(255, glow_alpha))), (7, 7), 7)
        s.blit(glow_s, (ex - 7, head_y - 8))
        # Pupil point
        pygame.draw.circle(s, EYE_GLOW, (ex + direction, head_y - 1), 2)
    
    # Nasal cavity
    pygame.draw.polygon(s, (30, 25, 20), [(cx - 2, head_y + 4), (cx + 2, head_y + 4), (cx, head_y + 8)])
    
    # Jaw (slightly separated, with teeth)
    jaw_y = head_y + 10
    pygame.draw.rect(s, BONE, (cx - 9, jaw_y, 18, 8), border_radius=2)
    pygame.draw.line(s, BONE_SHADOW, (cx - 8, jaw_y), (cx + 8, jaw_y), 1)
    # Individual teeth
    for ti in range(-6, 7, 3):
        pygame.draw.line(s, BONE_HIGHLIGHT, (cx + ti, jaw_y), (cx + ti, jaw_y + 3), 1)
    
    # --- ARMS ---
    shoulder_y = spine_top + 5
    
    # Back arm (pull arm for string)
    back_hand_x = cx - 10 * direction
    back_hand_y = shoulder_y + 5
    elbow_back_x = cx - 5 * direction
    elbow_back_y = shoulder_y + 15
    pygame.draw.line(s, BONE_SHADOW, (cx - 2 * direction, shoulder_y), (elbow_back_x, elbow_back_y), 4)
    pygame.draw.circle(s, JOINT, (elbow_back_x, elbow_back_y), 3)
    pygame.draw.line(s, BONE_SHADOW, (elbow_back_x, elbow_back_y), (back_hand_x, back_hand_y), 3)
    
    # Front arm (bow arm - extended)
    arm_len = 32
    hand_x = cx + arm_len * direction
    hand_y = shoulder_y + 2
    elbow_x = cx + (arm_len // 2) * direction
    elbow_y = shoulder_y + 12
    
    pygame.draw.line(s, BONE, (cx + 2 * direction, shoulder_y), (elbow_x, elbow_y), 4)
    pygame.draw.circle(s, JOINT, (elbow_x, elbow_y), 3)
    pygame.draw.line(s, BONE, (elbow_x, elbow_y), (hand_x, hand_y), 4)
    # Hand bones (fingers gripping)
    for fi in range(3):
        fa = fi * 0.3 - 0.3
        pygame.draw.line(s, BONE_SHADOW, (hand_x, hand_y), 
                        (hand_x + int(math.cos(fa) * 5 * direction), hand_y + int(math.sin(fa) * 5)), 2)
    
    # --- BOW (Detailed Longbow) ---
    bow_h = 35
    bow_top = (hand_x, hand_y - bow_h)
    bow_bot = (hand_x, hand_y + bow_h)
    
    # Bow limbs (curved with wood grain)
    curve_x = hand_x + 14 * direction
    # Upper limb
    pts_upper = [(hand_x, hand_y), (curve_x, hand_y - bow_h // 2), bow_top]
    pygame.draw.lines(s, (100, 60, 25), False, pts_upper, 4)
    # Lower limb
    pts_lower = [(hand_x, hand_y), (curve_x, hand_y + bow_h // 2), bow_bot]
    pygame.draw.lines(s, (100, 60, 25), False, pts_lower, 4)
    # Wood grain highlight
    pygame.draw.lines(s, (140, 90, 40), False, pts_upper, 2)
    pygame.draw.lines(s, (140, 90, 40), False, pts_lower, 2)
    # Bow tips (nocking points)
    pygame.draw.circle(s, (160, 140, 100), bow_top, 2)
    pygame.draw.circle(s, (160, 140, 100), bow_bot, 2)
    
    # String
    draw_pct = 0.0
    if is_attacking:
        if attack_phase < 0.5:
             draw_pct = attack_phase * 2.0
        else:
             draw_pct = 0.0
    
    string_x = hand_x - int(draw_pct * 22 * direction)
    pygame.draw.line(s, (200, 195, 180), bow_top, (string_x, hand_y), 1)
    pygame.draw.line(s, (200, 195, 180), bow_bot, (string_x, hand_y), 1)
    
    # Arrow nocked
    if is_attacking and attack_phase < 0.5:
        arrow_end = (string_x, hand_y)
        arrow_tip = (hand_x + 15 * direction, hand_y)
        # Shaft
        pygame.draw.line(s, (180, 160, 120), arrow_end, arrow_tip, 2)
        # Arrowhead (red-tipped)
        pygame.draw.polygon(s, (200, 50, 50), [
            (arrow_tip[0], arrow_tip[1] - 3),
            (arrow_tip[0], arrow_tip[1] + 3),
            (arrow_tip[0] + 6 * direction, arrow_tip[1])
        ])
        # Fletching
        pygame.draw.line(s, (100, 100, 100), (arrow_end[0], arrow_end[1] - 3), (arrow_end[0] + 4 * (-direction), arrow_end[1] - 5), 1)
        pygame.draw.line(s, (100, 100, 100), (arrow_end[0], arrow_end[1] + 3), (arrow_end[0] + 4 * (-direction), arrow_end[1] + 5), 1)

    # Scale & Blit
    if scale != 1.0:
        s = pygame.transform.scale(s, (int(w*scale), int(h*scale)))
    
    surface.blit(s, s.get_rect(midbottom=(x, y)))

def _draw_monster_base(surface, x, y, facing_right, scale, skin_color, outfit_color, weapon, is_goblin=False, tick=0, is_attacking=False, attack_phase=0.0):
    direction = 1 if facing_right else -1
    
    # Increase canvas size
    w, h = 300, 300 
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w//2, h - 10
    
    # --- ANIMATION CALCULATIONS ---
    # Walk Cycle: Sin wave for legs, Abs(Sin) for bounce
    walk_speed = tick / 150 # Speed of stride
    
    if is_attacking:
        walk_speed = 0 # Plant feet
        stride_len = 0
        bob_y = math.sin(tick / 200) * 2 # Breathing
        
        # Attack Swing Animation (Driven by Phase)
        # Phase goes 0.0 -> 1.0 over the attack duration.
        # We want swing out to Peak at 0.5 (Impact) and Return by 1.0
        # Sin(0..Pi) goes 0 -> 1 -> 0
        arm_swing = math.sin(attack_phase * math.pi) * 40 
    else:
        stride_len = 12 if not is_goblin else 8
        bob_y = abs(math.sin(walk_speed)) * 5
        arm_swing = math.sin(walk_speed * 2) * 5 # Casual swing
    
    # Leg offsets (Counter-phase)
    leg_l_off = math.sin(walk_speed) * stride_len
    leg_r_off = 0 if is_attacking else math.sin(walk_speed + math.pi) * stride_len
    
    # Adjust Y base with bob
    cy -= bob_y

    # --- Color Palette Generation (Shading) ---
    def darken(c, amount=40): return (max(0, c[0]-amount), max(0, c[1]-amount), max(0, c[2]-amount))
    def lighten(c, amount=40): return (min(255, c[0]+amount), min(255, c[1]+amount), min(255, c[2]+amount))
    
    skin_shadow = darken(skin_color)
    skin_highlight = lighten(skin_color, 20)
    outfit_shadow = darken(outfit_color)
    outfit_highlight = lighten(outfit_color, 30)

    # --- ANATOMY & POSING ---
    leg_w = 26 if not is_goblin else 16
    leg_h = 45 if not is_goblin else 35
    
    # 1. Back Leg (Animated)
    bx = cx - 15 - leg_w//2 + (leg_l_off * direction) # Offset by anim
    pygame.draw.rect(s, skin_shadow, (bx, cy - leg_h, leg_w, leg_h))
    # Boot/Foot Back
    pygame.draw.rect(s, outfit_color, (bx - 5, cy - 12, leg_w + 10, 12))

    # 2. Front Leg (Animated)
    fx = cx + 10 - leg_w//2 + (leg_r_off * direction)
    pygame.draw.rect(s, skin_color, (fx, cy - leg_h, leg_w, leg_h))
    # Muscle shading on leg
    pygame.draw.rect(s, skin_shadow, (fx, cy - leg_h, 6, leg_h)) 
    # Boot/Foot Front
    pygame.draw.rect(s, outfit_color, (fx - 5, cy - 12, leg_w + 10, 12))
    # Boot Detail
    pygame.draw.rect(s, outfit_highlight, (fx, cy - 12, 5, 12))

    # 3. Torso (Massive Trapezoid)
    body_y_bottom = cy - leg_h
    body_height = 70 if not is_goblin else 45
    body_y_top = body_y_bottom - body_height
    
    waist_w = 50 if not is_goblin else 30
    shoulder_w = 90 if not is_goblin else 50
    
    torso_points = [
        (cx - waist_w//2, body_y_bottom),           # Waist L
        (cx + waist_w//2, body_y_bottom),           # Waist R
        (cx + shoulder_w//2 - 5, body_y_top),       # Shoulder R
        (cx - shoulder_w//2 + 5, body_y_top)        # Shoulder L
    ]
    pygame.draw.polygon(s, skin_color, torso_points)
    
    # Abs/Pecs Definition
    # Central line
    pygame.draw.line(s, skin_shadow, (cx, body_y_top + 20), (cx, body_y_bottom - 10), 2)
    # Pecs
    pygame.draw.arc(s, skin_shadow, (cx - 25, body_y_top + 15, 25, 15), 3.14, 0, 2)
    pygame.draw.arc(s, skin_shadow, (cx, body_y_top + 15, 25, 15), 3.14, 0, 2)
    
    # 4. Loincloth / Belt (Detailed)
    belt_h = 25
    pygame.draw.rect(s, outfit_color, (cx - waist_w//2 - 5, body_y_bottom - 10, waist_w + 10, belt_h))
    # Fur texture
    for i in range(0, waist_w + 10, 5):
        pygame.draw.line(s, outfit_shadow, (cx - waist_w//2 - 5 + i, body_y_bottom - 10), (cx - waist_w//2 - 5 + i, body_y_bottom + 15), 1)
    
    # Skull Buckle
    if not is_goblin:
        # Cranium
        pygame.draw.circle(s, (220, 220, 220), (cx, body_y_bottom), 9)
        # Eye sockets
        pygame.draw.circle(s, (20, 0, 0), (cx - 3, body_y_bottom - 1), 2)
        pygame.draw.circle(s, (20, 0, 0), (cx + 3, body_y_bottom - 1), 2)
        # Teeth
        pygame.draw.line(s, (200, 200, 200), (cx-5, body_y_bottom+6), (cx+5, body_y_bottom+6), 3)

    # 5. Head
    head_size = 24 if not is_goblin else 18
    head_y = body_y_top - head_size + 10 
    head_x = cx
    
    # Thick Neck with muscle tendons
    pygame.draw.rect(s, skin_shadow, (cx - 14, body_y_top - 5, 28, 18))
    # Neck tendons
    pygame.draw.line(s, darken(skin_shadow, 15), (cx - 8, body_y_top - 3), (cx - 10, body_y_top + 10), 2)
    pygame.draw.line(s, darken(skin_shadow, 15), (cx + 8, body_y_top - 3), (cx + 10, body_y_top + 10), 2)
    
    # Face Shape (Square Jaw) - Bigger, more imposing
    pygame.draw.circle(s, skin_color, (head_x, head_y), head_size)
    pygame.draw.rect(s, skin_color, (head_x - head_size + 2, head_y, head_size*2 - 4, head_size), border_radius=5)
    
    # Brow ridge (overhanging)
    pygame.draw.ellipse(s, skin_shadow, (head_x - head_size + 2, head_y - head_size + 2, head_size * 2 - 4, 14))
    
    # Shading under chin
    pygame.draw.rect(s, skin_shadow, (head_x - head_size + 5, head_y + head_size - 4, head_size*2 - 10, 4))
    
    # Wart texture (small bumps)
    if not is_goblin:
        wart_rng = random.Random(42)
        for _ in range(4):
            wx = head_x + wart_rng.randint(-15, 15)
            wy = head_y + wart_rng.randint(-8, 12)
            pygame.draw.circle(s, lighten(skin_color, 15), (wx, wy), 2)
            pygame.draw.circle(s, skin_shadow, (wx + 1, wy + 1), 1)

    # Facial Features
    eye_y = head_y - 2
    eye_off = 9
    
    # Brows (Angry V - thicker)
    pygame.draw.line(s, (20, 15, 5), (head_x - 16, eye_y - 7), (head_x - 2, eye_y - 1), 4)
    pygame.draw.line(s, (20, 15, 5), (head_x + 16, eye_y - 7), (head_x + 2, eye_y - 1), 4)
    
    # Glowing Eyes (with bloodshot effect)
    for e_side in [-1, 1]:
        ex = head_x + eye_off * e_side
        # Bloodshot whites
        pygame.draw.circle(s, (200, 180, 150), (ex, eye_y), 5)
        # Red veins
        pygame.draw.line(s, (180, 50, 50), (ex - 3, eye_y - 2), (ex + 1, eye_y), 1)
        # Iris
        pygame.draw.circle(s, (255, 50, 0), (ex + direction, eye_y), 3)
        # Pupil
        pygame.draw.circle(s, (0, 0, 0), (ex + direction, eye_y), 2)
        # Glare
        pygame.draw.circle(s, (255, 200, 100), (ex + direction - 1, eye_y - 1), 1)
    
    # War Paint (tribal marks)
    if not is_goblin:
        paint_color = (150, 30, 30)
        # Diagonal slash across face
        pygame.draw.line(s, paint_color, (head_x - 12, head_y - 10), (head_x + 5, head_y + 8), 3)
        # Dots around eye
        pygame.draw.circle(s, paint_color, (head_x - 14, eye_y + 2), 2)
        pygame.draw.circle(s, paint_color, (head_x - 16, eye_y + 6), 2)
    
    # Drool (animated)
    drool_len = 5 + int(math.sin(tick / 120) * 3)
    drool_x = head_x + 8 * direction
    pygame.draw.line(s, (200, 220, 180, 180), (drool_x, head_y + head_size - 2), 
                    (drool_x + 2, head_y + head_size + drool_len), 2)
    
    # Tusks (Enhanced with ivory gradient)
    if not is_goblin:
        for tusk_side in [-1, 1]:
            tx_base = head_x + tusk_side * 11
            ty_base = head_y + 14
            ty_tip = head_y + 3
            # Tusk body (ivory)
            pygame.draw.polygon(s, (240, 235, 210), [
                (tx_base - 2, ty_base), (tx_base + 2, ty_base), 
                (tx_base + tusk_side * 3, ty_tip)
            ])
            # Tusk highlight
            pygame.draw.line(s, (255, 250, 240), (tx_base, ty_base), (tx_base + tusk_side * 2, ty_tip + 3), 1)
    
    # Ears (Pointed, detailed)
    ear_y = head_y - 5
    for ear_side in [-1, 1]:
        ear_x = head_x + ear_side * head_size
        pts = [(ear_x, ear_y), (ear_x + ear_side * 18, ear_y - 12), (ear_x, ear_y + 5)]
        pygame.draw.polygon(s, skin_shadow, pts)
        # Inner ear
        inner_pts = [(ear_x + ear_side * 3, ear_y), (ear_x + ear_side * 12, ear_y - 7), (ear_x + ear_side * 3, ear_y + 3)]
        pygame.draw.polygon(s, darken(skin_color, 20), inner_pts)

    # 6. Arms & Shoulders
    
    # Enhanced Shoulder Pads
    if not is_goblin:
        pad_size = 20
        for pad_side in [-1, 1]:
            pad_cx = cx + pad_side * shoulder_w // 2
            pad_cy = body_y_top + 5
            
            # Leather base
            pygame.draw.circle(s, (50, 45, 55), (pad_cx, pad_cy), pad_size)
            # Metal rim
            pygame.draw.circle(s, (80, 80, 90), (pad_cx, pad_cy), pad_size, 3)
            # Highlight
            pygame.draw.circle(s, (100, 100, 110), (pad_cx - 3, pad_cy - 5), 6)
            
            # Multiple spikes
            for spike_angle in [-0.8, 0, 0.8]:
                sp_len = 18
                sp_x = pad_cx + int(math.cos(spike_angle - 1.57) * sp_len) * pad_side
                sp_y = pad_cy + int(math.sin(spike_angle - 1.57) * sp_len)
                pygame.draw.line(s, (190, 190, 200), (pad_cx, pad_cy), (sp_x, sp_y), 3)
                # Spike tip
                pygame.draw.circle(s, (220, 220, 230), (sp_x, sp_y), 2)
            
            # Leather strap connecting to body
            pygame.draw.line(s, (70, 50, 30), (pad_cx, pad_cy + pad_size - 5), 
                           (cx + pad_side * 10, body_y_top + 25), 3)

    # Back Arm
    pygame.draw.line(s, skin_shadow, (cx - shoulder_w//2, body_y_top + 10), (cx - shoulder_w//2, body_y_top + 50), 18)
    
    # Front Arm (Holding Weapon)
    # Shoulder joint
    arm_start_x = cx + shoulder_w//2 - 5 * direction
    arm_start_y = body_y_top + 10
    
    # Hand pos (Animated slightly with walk or attack)
    if is_attacking:
        hand_x = arm_start_x + (60 * direction) # Reach forward
        hand_y = arm_start_y + 35 + arm_swing # Swing up/down
    else:
        hand_x = arm_start_x + (40 * direction)
        hand_y = arm_start_y + 35 + arm_swing # Casual sway
    
    # Bicep/Forearm (Two segments for muscle look)
    # Upper
    pygame.draw.line(s, skin_color, (arm_start_x, arm_start_y), (arm_start_x + 10*direction, arm_start_y + 20), 18)
    # Lower
    pygame.draw.line(s, skin_color, (arm_start_x + 10*direction, arm_start_y + 20), (hand_x, hand_y), 15)
    
    # 7. Weapon Rendering (In Front of hand)
    if weapon == "CLUB":
        stick_len = 90 # Longer Stick so grip looks natural
        
        # Grip Point: 
        # Before: end_y was way up, handle drawn from hand to end.
        # Fix: Draw FULL stick, passing through hand.
        # Top of stick (head)
        top_x = hand_x + (40 * direction)
        top_y = hand_y - 70 
        
        # Bottom of stick (pommel)
        bot_x = hand_x - (10 * direction)
        bot_y = hand_y + 15
        
        # Handle
        pygame.draw.line(s, (100, 70, 30), (bot_x, bot_y), (top_x, top_y), 8)
        
        # Spiked Head (Massive) at Top
        head_radius = 28
        pygame.draw.circle(s, (80, 70, 70), (top_x, top_y), head_radius)
        # Highlight/Shine
        pygame.draw.circle(s, (120, 110, 110), (top_x - 5, top_y - 5), 8)
        
        # Metal Spikes radiating
        for angle in range(0, 360, 45):
             rad = math.radians(angle)
             sp_x = top_x + math.cos(rad) * (head_radius + 10)
             sp_y = top_y + math.sin(rad) * (head_radius + 10)
             pygame.draw.line(s, (220, 220, 220), (top_x, top_y), (sp_x, sp_y), 3)

    elif weapon == "DAGGER":
        tip_x = hand_x + (25 * direction)
        tip_y = hand_y + 10
        pygame.draw.line(s, (180, 180, 180), (hand_x, hand_y), (tip_x, tip_y), 8)
        pygame.draw.line(s, (100, 50, 0), (hand_x, hand_y), (hand_x + 5*direction, hand_y - 5), 5) # Hilt

    elif weapon == "ROCK":
        pygame.draw.circle(s, (90, 80, 80), (hand_x, hand_y + 15), 28)
        # Detail
        pygame.draw.circle(s, (60, 50, 50), (hand_x - 5, hand_y + 10), 8)

    # Scale & Blit
    if scale != 1.0:
        s = pygame.transform.scale(s, (int(w*scale), int(h*scale)))
    
    surface.blit(s, s.get_rect(midbottom=(x, y)))

def draw_projectile(surface, x, y, color=WHITE, particles=None, scale=1.0, p_type="DEFAULT"):
    """Draws ULTRA-PREMIUM projectile visualization with cinematic effects."""
    
    t = pygame.time.get_ticks()
    
    # --- PARTICLE TRAIL (Per-type color gradients) ---
    if particles:
        for p in particles:
             px, py, vx, vy, life, max_life, size = p
             alpha = int((life / max_life) * 220)
             if alpha <= 0: continue
             
             progress = 1.0 - (life / max_life)
             
             if p_type == "FIRE_RING":
                 # Molten lava gradient
                 if progress < 0.15: col = (255, 255, 200)
                 elif progress < 0.3: col = (255, 200, 50)
                 elif progress < 0.5: col = (255, 120, 0)
                 elif progress < 0.75: col = (200, 40, 0)
                 else: col = (80, 20, 0)
             elif p_type == "VOID_LANCE":
                 # Dark energy dissipation
                 if progress < 0.2: col = (200, 150, 255)
                 elif progress < 0.5: col = (120, 0, 220)
                 elif progress < 0.8: col = (60, 0, 120)
                 else: col = (20, 0, 40)
             elif p_type == "ARCANE_VOLLEY":
                 # Arcane sparkle decay
                 if progress < 0.2: col = (220, 200, 255)
                 elif progress < 0.5: col = (180, 80, 255)
                 elif progress < 0.8: col = (100, 30, 200)
                 else: col = (40, 10, 80)
             else: # Default fireball
                if progress < 0.1: col = (255, 255, 240)
                elif progress < 0.25: col = (255, 255, 100)
                elif progress < 0.45: col = (255, 180, 0)
                elif progress < 0.65: col = (255, 80, 0)
                elif progress < 0.85: col = (180, 30, 0)
                else: col = (60, 60, 60)
             
             p_size = max(1, int(size))
             s = pygame.Surface((p_size*2+2, p_size*2+2), pygame.SRCALPHA)
             
             # Glow halo behind particle
             glow_alpha = max(0, min(255, alpha // 2))
             glow_col = (col[0], col[1], col[2], glow_alpha)
             pygame.draw.circle(s, glow_col, (p_size+1, p_size+1), p_size+1)
             
             # Core particle
             core_col = (min(255, col[0]+30), min(255, col[1]+30), min(255, col[2]+30), min(255, alpha))
             pygame.draw.circle(s, core_col, (p_size+1, p_size+1), max(1, p_size-1))
             
             surface.blit(s, (px - p_size - 1, py - p_size - 1))

    if p_type == "FIRE_RING":
        # === INFERNO RING - Rotating double-ring with flame tongues ===
        ring_radius = 22 * scale 
        s_size = int(ring_radius * 3.2)
        s_ring = pygame.Surface((s_size, s_size), pygame.SRCALPHA)
        cx, cy = s_size//2, s_size//2
        
        rot = t / 40.0
        rot2 = -t / 60.0
        
        # Heat shimmer (outer aura)
        for layer in range(3):
            shimmer_r = ring_radius + 8 + layer * 4
            shimmer_alpha = 30 - layer * 8
            pygame.draw.circle(s_ring, (255, 100, 0, max(0, shimmer_alpha)), (cx, cy), int(shimmer_r), 2)
        
        # Outer ring (thick, dark orange)
        pygame.draw.circle(s_ring, (200, 60, 0), (cx, cy), int(ring_radius), 5)
        # Inner ring (bright yellow-orange)
        pygame.draw.circle(s_ring, (255, 200, 50), (cx, cy), int(ring_radius - 3), 3)
        # Core ring (white-hot)
        pygame.draw.circle(s_ring, (255, 255, 180, 180), (cx, cy), int(ring_radius - 5), 2)
        
        # Animated flame tongues on circumference
        num_flames = 12
        for i in range(num_flames):
            angle = (i / num_flames) * 6.2832 + rot
            
            fx = cx + math.cos(angle) * ring_radius
            fy = cy + math.sin(angle) * ring_radius
            
            # Flame tongue height oscillation
            flame_h = (6 + math.sin(t/60 + i*1.3) * 4) * scale
            
            # Outward direction for flame
            out_x = math.cos(angle) * flame_h
            out_y = math.sin(angle) * flame_h
            
            # Multi-layer flame tongue
            tip_x = fx + out_x
            tip_y = fy + out_y
            
            # Outer flame (red-orange)
            pygame.draw.line(s_ring, (255, 80, 0, 200), (int(fx), int(fy)), (int(tip_x), int(tip_y)), 3)
            # Inner flame (yellow)
            mid_x = fx + out_x * 0.6
            mid_y = fy + out_y * 0.6
            pygame.draw.line(s_ring, (255, 220, 50, 220), (int(fx), int(fy)), (int(mid_x), int(mid_y)), 2)
            # Hot core
            pygame.draw.circle(s_ring, (255, 255, 200, 250), (int(fx), int(fy)), 2)
        
        # Secondary counter-rotating flame ring (smaller flames)
        for i in range(8):
            angle = (i / 8) * 6.2832 + rot2
            fx = cx + math.cos(angle) * (ring_radius - 2)
            fy = cy + math.sin(angle) * (ring_radius - 2)
            f_s = int(3 * scale + math.sin(t/80 + i) * 1.5)
            pygame.draw.circle(s_ring, (255, 180, 0, 160), (int(fx), int(fy)), max(1, f_s))
        
        # Center glow (heat)
        inner_glow = pygame.Surface((int(ring_radius*1.4), int(ring_radius*1.4)), pygame.SRCALPHA)
        pygame.draw.circle(inner_glow, (255, 150, 0, 25), (int(ring_radius*0.7), int(ring_radius*0.7)), int(ring_radius*0.7))
        s_ring.blit(inner_glow, (cx - int(ring_radius*0.7), cy - int(ring_radius*0.7)))
        
        surface.blit(s_ring, (x - s_size//2, y - s_size//2))
            
    elif p_type == "VOID_LANCE":
        # === VOID LANCE - Dark energy beam with electric tendrils ===
        w_beam = int(50 * scale)
        h_beam = int(14 * scale)
        s_size_x = w_beam + 30
        s_size_y = h_beam + 30
        s_lance = pygame.Surface((s_size_x, s_size_y), pygame.SRCALPHA)
        lcx, lcy = s_size_x // 2, s_size_y // 2
        
        # Dark aura (outer glow)
        for layer in range(4):
            gw = w_beam + 12 - layer * 3
            gh = h_beam + 12 - layer * 3
            alpha_l = 25 + layer * 15
            pygame.draw.ellipse(s_lance, (80, 0, 160, alpha_l), 
                              (lcx - gw//2, lcy - gh//2, gw, gh))
        
        # Main beam body (dark purple)
        pygame.draw.ellipse(s_lance, (40, 0, 80), (lcx - w_beam//2, lcy - h_beam//2, w_beam, h_beam))
        
        # Energy core (bright violet)
        inner_w = int(w_beam * 0.7)
        inner_h = int(h_beam * 0.5)
        pygame.draw.ellipse(s_lance, (160, 80, 255), (lcx - inner_w//2, lcy - inner_h//2, inner_w, inner_h))
        
        # White-hot center line
        pygame.draw.ellipse(s_lance, (220, 200, 255), (lcx - inner_w//3, lcy - 2, inner_w*2//3, 4))
        
        # Electric tendrils along the beam
        for i in range(5):
            ang = t / 30 + i * 1.2
            tx = lcx + int(math.cos(ang + i) * (w_beam * 0.4))
            ty_off = int(math.sin(ang * 2 + i) * (h_beam * 0.8))
            tendril_y = lcy + ty_off
            pygame.draw.line(s_lance, (200, 150, 255, 180), (lcx, lcy), (tx, tendril_y), 1)
            pygame.draw.circle(s_lance, (220, 200, 255), (tx, tendril_y), 2)
        
        # Leading edge spark
        pulse_r = 3 + math.sin(t / 30) * 2
        pygame.draw.circle(s_lance, (255, 255, 255), (lcx + w_beam//2 - 4, lcy), int(pulse_r))
        
        # Afterimage trail (fading copies behind)
        for trail in range(3):
            trail_alpha = 40 - trail * 12
            trail_off = (trail + 1) * 8
            trail_s = pygame.Surface((w_beam, h_beam), pygame.SRCALPHA)
            pygame.draw.ellipse(trail_s, (60, 0, 120, max(0, trail_alpha)), (0, 0, w_beam, h_beam))
            surface.blit(trail_s, (x - w_beam//2 - trail_off, y - h_beam//2))
        
        surface.blit(s_lance, (x - s_size_x//2, y - s_size_y//2))
        
    elif p_type == "ARCANE_VOLLEY":
        # === ARCANE VOLLEY - Crystalline orbs with rune energy ===
        pulse = math.sin(t / 40) * 3
        r = int(8 * scale + pulse)
        
        s_size = (r + 10) * 2
        s_orb = pygame.Surface((s_size, s_size), pygame.SRCALPHA)
        ocx, ocy = s_size // 2, s_size // 2
        
        # Outer mystical glow
        pygame.draw.circle(s_orb, (120, 40, 200, 40), (ocx, ocy), r + 8)
        pygame.draw.circle(s_orb, (160, 80, 255, 60), (ocx, ocy), r + 4)
        
        # Main orb body
        pygame.draw.circle(s_orb, (130, 50, 220), (ocx, ocy), r)
        
        # Crystalline facet highlights
        for i in range(3):
            facet_ang = t / 60 + i * 2.1
            fhx = ocx + int(math.cos(facet_ang) * r * 0.4)
            fhy = ocy + int(math.sin(facet_ang) * r * 0.4)
            pygame.draw.circle(s_orb, (200, 180, 255, 200), (fhx, fhy), max(1, int(r * 0.3)))
        
        # Core (bright white)
        pygame.draw.circle(s_orb, (230, 220, 255), (ocx, ocy), max(1, int(r * 0.4)))
        
        # Orbiting rune sparks
        for i in range(4):
            orb_ang = t / 25 + i * 1.57
            orb_r = r + 5 + math.sin(t / 50 + i) * 3
            orb_x = ocx + int(math.cos(orb_ang) * orb_r)
            orb_y = ocy + int(math.sin(orb_ang) * orb_r)
            pygame.draw.circle(s_orb, (200, 200, 255, 200), (orb_x, orb_y), 2)
            # Tiny trail line
            trail_x = ocx + int(math.cos(orb_ang - 0.3) * orb_r)
            trail_y = ocy + int(math.sin(orb_ang - 0.3) * orb_r)
            pygame.draw.line(s_orb, (180, 150, 255, 100), (orb_x, orb_y), (trail_x, trail_y), 1)
        
        surface.blit(s_orb, (x - s_size//2, y - s_size//2))
        
    else:
        # === DEFAULT FIREBALL - Multi-layered cinematic fire ===
        base_radius = 18 * scale
        pulse = math.sin(t / 45) * (3.5 * scale)
        
        # 1. Massive soft outer glow (heat distortion)
        radius_outer = base_radius + pulse + 6
        glow_size = int(radius_outer * 4)
        s_glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        gcx, gcy = glow_size // 2, glow_size // 2
        
        # Three-layer glow
        pygame.draw.circle(s_glow, (255, 50, 0, 25), (gcx, gcy), int(radius_outer * 1.6))
        pygame.draw.circle(s_glow, (255, 100, 0, 45), (gcx, gcy), int(radius_outer * 1.2))
        pygame.draw.circle(s_glow, (255, 150, 0, 70), (gcx, gcy), int(radius_outer * 0.9))
        surface.blit(s_glow, (x - glow_size//2, y - glow_size//2))
        
        # 2. Fire body (main flame shape)
        flame_size = int(base_radius * 3.5)
        s_fire = pygame.Surface((flame_size, flame_size), pygame.SRCALPHA)
        fcx, fcy = flame_size // 2, flame_size // 2
        
        # Irregular flame shape with procedural bumps
        for layer in range(5):
            layer_r = base_radius - layer * 2 + pulse * (0.5 + layer * 0.1)
            if layer_r <= 0: continue
            
            # Color gradient from outer to inner
            colors = [
                (180, 30, 0, 120),    # Dark red outer
                (230, 60, 0, 160),    # Red-orange
                (255, 140, 0, 200),   # Orange
                (255, 220, 50, 230),  # Yellow
                (255, 255, 220, 255), # White-hot core
            ]
            col = colors[layer]
            
            # Draw bumpy circle 
            num_pts = 12
            pts = []
            for pi in range(num_pts):
                a = (pi / num_pts) * 6.2832
                bump = math.sin(t / 30 + pi * 2 + layer) * (3 * scale)
                r_pt = max(1, layer_r + bump)
                pts.append((fcx + int(math.cos(a) * r_pt), fcy + int(math.sin(a) * r_pt)))
            
            if len(pts) >= 3:
                pygame.draw.polygon(s_fire, col, pts)
        
        surface.blit(s_fire, (x - flame_size//2, y - flame_size//2))
        
        # 3. Plasma core (white-hot center)
        core_r = max(1, int(5 * scale + pulse * 0.3))
        s_core = pygame.Surface((core_r*4, core_r*4), pygame.SRCALPHA)
        pygame.draw.circle(s_core, (255, 255, 200, 250), (core_r*2, core_r*2), core_r + 2)
        pygame.draw.circle(s_core, (255, 255, 255), (core_r*2, core_r*2), core_r)
        surface.blit(s_core, (x - core_r*2, y - core_r*2))
        
        # 4. Orbiting embers
        random.seed(int(t / 25))
        for i in range(int(4 * scale)):
            ember_ang = t / 20 + i * 1.5 + random.random()
            ember_dist = base_radius * (0.8 + random.random() * 0.6)
            ex = x + int(math.cos(ember_ang) * ember_dist)
            ey = y + int(math.sin(ember_ang) * ember_dist)
            ember_size = max(1, int(2 * scale + random.random() * 2))
            
            s_ember = pygame.Surface((ember_size*2+2, ember_size*2+2), pygame.SRCALPHA)
            pygame.draw.circle(s_ember, (255, 255, 100, 200), (ember_size+1, ember_size+1), ember_size)
            pygame.draw.circle(s_ember, (255, 200, 50, 150), (ember_size+1, ember_size+1), ember_size+1)
            surface.blit(s_ember, (ex - ember_size-1, ey - ember_size-1))

def draw_background_scenery(surface, biome, width, height, scroll_x=0):
    """Draws CINEMATIC biome backgrounds with atmospheric depth and detail."""
    
    # Helper for gradients
    def draw_gradient(surf, color_top, color_bot, rect):
        h = rect.height
        for i in range(h):
            alpha = i / h
            r = int(color_top[0] * (1 - alpha) + color_bot[0] * alpha)
            g = int(color_top[1] * (1 - alpha) + color_bot[1] * alpha)
            b = int(color_top[2] * (1 - alpha) + color_bot[2] * alpha)
            pygame.draw.line(surf, (r, g, b), (rect.x, rect.y + i), (rect.x + rect.width, rect.y + i))
            
    if biome == "FOREST":
        # 1. Layered Sky (Golden hour gradient)
        draw_gradient(surface, (25, 80, 160), (120, 180, 230), pygame.Rect(0, 0, width, height // 2))
        draw_gradient(surface, (120, 180, 230), (180, 220, 200), pygame.Rect(0, height // 2, width, height // 2))
        
        # Sun (Larger with corona)
        sun_x, sun_y = width - 150, 90
        # Corona layers
        corona_s = pygame.Surface((250, 250), pygame.SRCALPHA)
        pygame.draw.circle(corona_s, (255, 200, 100, 15), (125, 125), 120)
        pygame.draw.circle(corona_s, (255, 220, 150, 30), (125, 125), 90)
        pygame.draw.circle(corona_s, (255, 240, 180, 50), (125, 125), 70)
        surface.blit(corona_s, (sun_x - 125, sun_y - 125))
        pygame.draw.circle(surface, (255, 255, 220), (sun_x, sun_y), 50)
        # Flare highlight
        flare_s = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(flare_s, (255, 255, 255, 180), (15, 15), 15)
        surface.blit(flare_s, (sun_x - 15, sun_y - 15))
        
        # God Rays (Animated)
        ray_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        t_ray = pygame.time.get_ticks() / 1000
        for i in range(7):
            start_x = sun_x
            start_y = sun_y
            end_x = width - 400 - (i * 180) + math.sin(t_ray + i) * 25
            ray_w = 80 + i * 15
            poly = [(start_x, start_y), (end_x, height), (end_x + ray_w, height)]
            pygame.draw.polygon(ray_surface, (255, 255, 200, 15), poly)
        surface.blit(ray_surface, (0, 0))

        # 2. Far Mountains (Layered depth)
        # Layer 1 - Very far (purple-blue)
        random.seed(10)
        for i in range(0, width, 150):
            h_mount = 180 + random.randint(0, 60) + int(math.sin(i / 350) * 70)
            points = [(i - 20, height), (i + 170, height), (i + 75, height - h_mount)]
            pygame.draw.polygon(surface, (70, 65, 110), points)
            # Snow cap
            pygame.draw.polygon(surface, (180, 180, 200), [
                (i + 55, height - h_mount + 30), (i + 95, height - h_mount + 30), (i + 75, height - h_mount)
            ])
        
        # Layer 2 - Mid mountains (darker)
        random.seed(11)
        for i in range(0, width, 120):
            h_mount = 130 + random.randint(0, 50)
            points = [(i - 10, height), (i + 130, height), (i + 60, height - h_mount)]
            pygame.draw.polygon(surface, (55, 75, 95), points)

        # 3. Dense Trees (Multi-layered canopies)
        random.seed(42)
        tree_colors = [(15, 55, 18), (20, 65, 22), (25, 70, 25), (18, 60, 20)]
        for i in range(-50, width, 70):
            h_t = 170 + (i % 80)
            tc = tree_colors[i % len(tree_colors)]
            tc_light = (min(255, tc[0] + 20), min(255, tc[1] + 25), min(255, tc[2] + 20))
            
            # Trunk with bark texture
            trunk_x = i + 20
            pygame.draw.rect(surface, (50, 35, 18), (trunk_x, height - h_t, 12, h_t))
            # Bark lines
            for bark in range(0, h_t, 12):
                pygame.draw.line(surface, (35, 25, 12), (trunk_x + 2, height - h_t + bark), (trunk_x + 10, height - h_t + bark + 5), 1)
            
            # Root flares
            pygame.draw.line(surface, (45, 30, 15), (trunk_x - 5, height), (trunk_x + 3, height - 15), 3)
            pygame.draw.line(surface, (45, 30, 15), (trunk_x + 17, height), (trunk_x + 9, height - 15), 3)
            
            # Leaves (3 tiers)
            leaf_cx = trunk_x + 6
            for tier in range(3):
                tier_y = height - h_t + 30 + tier * 35
                tier_w = 30 + tier * 12
                pygame.draw.polygon(surface, tc, [
                    (leaf_cx - tier_w, tier_y + 35), (leaf_cx + tier_w, tier_y + 35), (leaf_cx, tier_y - 20)
                ])
                # Highlight edge
                pygame.draw.polygon(surface, tc_light, [
                    (leaf_cx - tier_w + 5, tier_y + 30), (leaf_cx, tier_y + 30), (leaf_cx - 2, tier_y - 10)
                ])

        # 4. GROUND (Layered)
        ground_top = height - 80
        # Dirt layer
        draw_gradient(surface, (45, 90, 35), (30, 60, 25), pygame.Rect(0, ground_top, width, 80))
        # Moss edge
        pygame.draw.rect(surface, (40, 100, 35), (0, ground_top, width, 5))
        # Edge detail
        pygame.draw.rect(surface, (55, 120, 45), (0, ground_top, width, 2))
        
        # Grass tufts
        random.seed(99)
        for i in range(0, width, 7):
            g_h = random.randint(6, 16)
            g_lean = random.randint(-4, 4)
            g_col = (40 + random.randint(0, 30), 130 + random.randint(0, 40), 40 + random.randint(0, 20))
            pygame.draw.line(surface, g_col, (i, ground_top), (i + g_lean, ground_top - g_h), 2)
        
        # Wildflowers
        random.seed(200)
        for _ in range(15):
            fx = random.randint(0, width)
            flower_colors = [(255, 80, 80), (255, 200, 50), (200, 100, 255), (255, 150, 200)]
            fc = flower_colors[random.randint(0, 3)]
            pygame.draw.circle(surface, fc, (fx, ground_top - 2), 3)
            pygame.draw.line(surface, (30, 90, 30), (fx, ground_top - 2), (fx, ground_top + 3), 1)
            
        # Falling Leaves (Animated, various colors)
        t_leaf = pygame.time.get_ticks() / 10
        leaf_colors = [(255, 190, 80), (255, 140, 50), (220, 100, 30), (180, 200, 60)]
        for i in range(25):
            lx = (i * 123 + t_leaf * 0.7) % width
            ly = (i * 57 + t_leaf * 1.5) % (height - 60)
            lc = leaf_colors[i % len(leaf_colors)]
            rot = math.sin(t_leaf / 10 + i) * 3
            pygame.draw.circle(surface, lc, (int(lx + rot), int(ly)), 3)

    elif biome == "ICE":
        # 1. SKY (Deep arctic twilight)
        draw_gradient(surface, (8, 15, 60), (40, 80, 140), pygame.Rect(0, 0, width, height // 2))
        draw_gradient(surface, (40, 80, 140), (80, 150, 200), pygame.Rect(0, height // 2, width, height // 2))
        
        # Stars (Various brightness)
        random.seed(555)
        for _ in range(80):
            sx = random.randint(0, width)
            sy = random.randint(0, int(height * 0.6))
            brightness = random.randint(150, 255)
            star_size = 1 if brightness < 200 else 2
            pygame.draw.circle(surface, (brightness, brightness, brightness), (sx, sy), star_size)

        # Moon (Detailed with craters)
        moon_x, moon_y = 100, 110
        # Moon glow
        moon_glow = pygame.Surface((250, 250), pygame.SRCALPHA)
        pygame.draw.circle(moon_glow, (200, 220, 255, 15), (125, 125), 120)
        pygame.draw.circle(moon_glow, (210, 230, 255, 30), (125, 125), 100)
        surface.blit(moon_glow, (moon_x - 125, moon_y - 125))
        
        pygame.draw.circle(surface, (220, 235, 255), (moon_x, moon_y), 85)
        # Surface detail
        pygame.draw.circle(surface, (195, 215, 240), (moon_x - 25, moon_y + 15), 22)
        pygame.draw.circle(surface, (200, 218, 242), (moon_x + 35, moon_y - 25), 12)
        pygame.draw.circle(surface, (190, 210, 238), (moon_x + 10, moon_y + 35), 15)
        pygame.draw.circle(surface, (205, 220, 245), (moon_x - 40, moon_y - 20), 8)
        
        # Aurora (3 ribbons with distinct colors)
        t_aur = pygame.time.get_ticks() / 2000
        s_aurora = pygame.Surface((width, height), pygame.SRCALPHA)
        aurora_colors = [
            (30, 255, 170, 35),   # Green
            (80, 140, 255, 25),   # Blue
            (200, 100, 255, 20),  # Magenta
        ]
        for rib in range(3):
            points = []
            for x_a in range(0, width + 20, 15):
                y_base = 80 + rib * 40
                y_off = (math.sin(x_a / 250 + t_aur * 1.5 + rib * 1.2) * 45 + 
                        math.sin(x_a / 120 + rib * 0.8) * 20 +
                        math.cos(x_a / 180 + t_aur * 0.7) * 15)
                points.append((x_a, int(y_base + y_off)))
            
            if len(points) > 1:
                # Draw ribbon as filled polygon
                poly_pts = points + [(width, 0), (0, 0)]
                pygame.draw.polygon(s_aurora, aurora_colors[rib], poly_pts)
                # Bright edge line
                edge_col = (aurora_colors[rib][0], aurora_colors[rib][1], aurora_colors[rib][2], 80)
                pygame.draw.lines(s_aurora, edge_col, False, points, 2)
        surface.blit(s_aurora, (0, 0))
        
        # 2. FROZEN SPIRES (Taller, crystalline)
        random.seed(777)
        for i in range(0, width, 75):
            h_spike = 220 + random.randint(0, 320)
            base_w = 35 + random.randint(0, 15)
            poly = [
                (i, height), (i + base_w, height), (i + base_w // 2, height - h_spike)
            ]
            # Dark ice body
            pygame.draw.polygon(surface, (35, 55, 95), poly)
            # Highlight streak (crystalline shine)
            mid_x = i + base_w // 2
            pygame.draw.line(surface, (120, 160, 220), (mid_x, height), (mid_x, height - h_spike), 2)
            pygame.draw.line(surface, (180, 210, 255), (mid_x + 2, height - 20), (mid_x + 2, height - h_spike + 30), 1)

        # Frozen Keep (Enhanced)
        k_x = width // 2 + 100
        k_y = height - 50
        # Main Tower
        pygame.draw.rect(surface, (50, 60, 100), (k_x - 45, k_y - 320, 90, 320))
        # Tower cap
        pygame.draw.polygon(surface, (55, 65, 105), [(k_x - 55, k_y - 320), (k_x + 55, k_y - 320), (k_x, k_y - 470)])
        # Crenellations
        for ci in range(-40, 41, 16):
            pygame.draw.rect(surface, (60, 70, 110), (k_x + ci - 4, k_y - 330, 8, 15))
        # Trim lines
        pygame.draw.rect(surface, (90, 110, 170), (k_x - 35, k_y - 310, 70, 310), 2)
        # Windows (Frost glow)
        for wy in range(k_y - 280, k_y - 50, 70):
            win_s = pygame.Surface((30, 50), pygame.SRCALPHA)
            glow_alpha = 150 + int(math.sin(pygame.time.get_ticks() / 500 + wy) * 50)
            pygame.draw.rect(win_s, (150, 220, 255, max(50, min(255, glow_alpha))), (5, 5, 20, 40))
            pygame.draw.rect(win_s, (100, 150, 200, 200), (5, 5, 20, 40), 2)
            surface.blit(win_s, (k_x - 15, wy))

        # 3. FROZEN GROUND (Ice with cracks)
        ground_top = height - 70
        # Ice base
        draw_gradient(surface, (140, 190, 225), (100, 160, 200), pygame.Rect(0, ground_top, width, 70))
        # Horizon line
        pygame.draw.rect(surface, (230, 240, 255), (0, ground_top, width, 3))
        
        # Ice crack network
        random.seed(888)
        for _ in range(25):
            cx = random.randint(0, width)
            cy = random.randint(ground_top + 5, height - 5)
            for seg in range(3):
                dx = random.randint(-30, 30)
                dy = random.randint(-10, 10)
                pygame.draw.line(surface, (180, 210, 240), (cx, cy), (cx + dx, cy + dy), 1)
                cx += dx
                cy += dy
        
        # Reflections (spire shapes inverted)
        s_ref = pygame.Surface((width, 70), pygame.SRCALPHA)
        random.seed(777)
        for i in range(0, width, 75):
            h_spike = 220 + random.randint(0, 320)
            base_w = 35 + random.randint(0, 15)
            ref_h = min(60, h_spike * 0.25)
            pygame.draw.polygon(s_ref, (200, 220, 255, 20), [
                (i, 0), (i + base_w, 0), (i + base_w // 2, int(ref_h))
            ])
        surface.blit(s_ref, (0, ground_top + 3))
        
        # 4. ROLLING MIST & SNOW
        t_mist = pygame.time.get_ticks() / 50
        for i in range(6):
            mx = (t_mist * (i + 1) * 18) % (width + 500) - 250
            mist_w = 350 + i * 30
            s_mist = pygame.Surface((mist_w, 45), pygame.SRCALPHA)
            pygame.draw.ellipse(s_mist, (220, 235, 255, 25), (0, 0, mist_w, 45))
            surface.blit(s_mist, (int(mx), ground_top - 25 + i * 6))
        
        # Snowflakes
        t_snow = pygame.time.get_ticks() / 15
        for i in range(35):
            sx = (i * 97 + t_snow * 0.5) % width
            sy = (i * 43 + t_snow * 1.2) % (height - 30)
            snow_size = 1 + (i % 3)
            pygame.draw.circle(surface, (240, 245, 255), (int(sx), int(sy)), snow_size)

    elif biome == "VOLCANO":
        # 1. Hellscape Sky (with orange horizon glow)
        draw_gradient(surface, (30, 2, 2), (60, 8, 0), pygame.Rect(0, 0, width, height * 2 // 3))
        draw_gradient(surface, (60, 8, 0), (100, 25, 0), pygame.Rect(0, height * 2 // 3, width, height // 3))
        
        # Ash clouds (drifting)
        s_smoke = pygame.Surface((width, height), pygame.SRCALPHA)
        t_smoke = pygame.time.get_ticks() / 1000
        for i in range(12):
            scx = int((t_smoke * 18 + i * 180) % (width + 400) - 200)
            scy = 40 + int(math.sin(t_smoke * 0.8 + i) * 25) + (i % 3) * 20
            s_size = 80 + i * 15
            pygame.draw.circle(s_smoke, (15, 10, 10, 60), (scx, scy), s_size)
            pygame.draw.circle(s_smoke, (25, 15, 10, 30), (scx + 40, scy + 10), s_size - 20)
        surface.blit(s_smoke, (0, 0))

        # Ember sky particles
        t_emb = pygame.time.get_ticks() / 20
        for i in range(15):
            ex = int((i * 137 + t_emb) % width)
            ey = int((i * 73 + t_emb * 0.5) % (height * 0.6))
            pygame.draw.circle(surface, (255, 120, 0), (ex, ey), 1)
        
        # 2. Mega Volcano (Textured)
        v_x = width // 2
        v_top_y = height - 460
        
        # Volcano body
        pygame.draw.polygon(surface, (18, 5, 3), [
            (v_x - 520, height), (v_x + 520, height), (v_x, v_top_y)
        ])
        
        # Rocky texture details
        random.seed(333)
        for _ in range(40):
            rx = v_x + random.randint(-400, 400)
            ry = random.randint(v_top_y + 50, height - 30)
            # Only draw if inside volcano shape
            y_ratio = (ry - v_top_y) / (height - v_top_y)
            max_x_off = 520 * y_ratio
            if abs(rx - v_x) < max_x_off:
                rock_w = random.randint(8, 25)
                rock_h = random.randint(5, 15)
                rock_col = (25 + random.randint(0, 15), 8 + random.randint(0, 8), 5 + random.randint(0, 5))
                pygame.draw.ellipse(surface, rock_col, (rx, ry, rock_w, rock_h))
        
        # Crater glow (pulsing orange at top)
        glow_t = pygame.time.get_ticks() / 200
        glow_intensity = 60 + int(math.sin(glow_t) * 30)
        crater_s = pygame.Surface((120, 60), pygame.SRCALPHA)
        pygame.draw.ellipse(crater_s, (255, 80, 0, max(0, min(255, glow_intensity))), (0, 0, 120, 60))
        surface.blit(crater_s, (v_x - 60, v_top_y - 15))
        
        # 3. Lava flow (Side of volcano)
        t = pygame.time.get_ticks()
        flow_offset = (t / 50) % 20
        
        lava_poly = [
            (v_x, v_top_y + 10), 
            (v_x - 110, height), 
            (v_x + 110, height)
        ]
        pygame.draw.polygon(surface, (180, 40, 0), lava_poly)
        
        # Bright veins in lava
        for i in range(12):
            ly = int(v_top_y + 10 + i * 35 + flow_offset)
            if ly < height:
                vein_w = 5 + (i % 3) * 3
                lx_off = int(math.sin(i * 0.7 + flow_offset / 10) * 15)
                pygame.draw.line(surface, (255, 130, 0), (v_x + lx_off, ly), (v_x + lx_off + vein_w, ly + 20), 3)
                pygame.draw.line(surface, (255, 200, 50), (v_x + lx_off + 1, ly + 2), (v_x + lx_off + vein_w - 1, ly + 18), 1)

        # 4. Volcanic Bombs
        for i in range(6):
            cycle_dur = 2200
            local_t = (t + i * 370) % cycle_dur
            
            if local_t < 1600:
                prog = local_t / 1600.0
                spread = (280 + i * 30) * (-1 if i % 2 == 0 else 1)
                
                curr_x = v_x + spread * prog
                arc_h = 220 * math.sin(prog * 3.14159)
                curr_y = v_top_y - arc_h + (prog * 470)
                
                # Rock (darker, larger)
                rock_r = 5 + i % 3
                pygame.draw.circle(surface, (40, 30, 30), (int(curr_x), int(curr_y)), rock_r)
                # Magma core
                pygame.draw.circle(surface, (255, 120, 0), (int(curr_x), int(curr_y)), max(1, rock_r - 2))
                # Hot center
                pygame.draw.circle(surface, (255, 220, 80), (int(curr_x) + 1, int(curr_y) - 1), max(1, rock_r - 4))
                
                # Glowing trail
                if prog < 0.85:
                    for trail_i in range(3):
                        t_off = trail_i * 0.03
                        t_prog = max(0, prog - t_off)
                        tx = v_x + spread * t_prog
                        ty = v_top_y - 220 * math.sin(t_prog * 3.14159) + (t_prog * 470)
                        trail_alpha = 150 - trail_i * 40
                        ts = pygame.Surface((8, 8), pygame.SRCALPHA)
                        pygame.draw.circle(ts, (255, 100, 0, max(0, trail_alpha)), (4, 4), 4)
                        surface.blit(ts, (int(tx) - 4, int(ty) - 4))

        # 5. Ground (Cracked obsidian with lava underneath)
        ground_top = height - 80
        pygame.draw.rect(surface, (35, 15, 10), (0, ground_top, width, 80))
        
        # Lava underneath showing through cracks
        lava_y = ground_top + 35
        lava_glow = 180 + int(math.sin(t / 150) * 40)
        pygame.draw.rect(surface, (min(255, lava_glow + 50), 50, 0), (0, lava_y, width, 35))
        
        # Surface cracks revealing lava
        random.seed(444)
        for _ in range(20):
            cx = random.randint(0, width)
            cy = random.randint(ground_top + 2, ground_top + 30)
            crack_len = random.randint(15, 50)
            crack_dir = random.uniform(-0.5, 0.5)
            ex = cx + int(crack_len * math.cos(crack_dir))
            ey = cy + int(crack_len * math.sin(crack_dir))
            # Crack (dark)
            pygame.draw.line(surface, (15, 5, 0), (cx, cy), (ex, ey), 2)
            # Lava glow in crack
            pygame.draw.line(surface, (255, 80, 0), (cx + 1, cy + 1), (ex + 1, ey + 1), 1)
        
        # Lava bubbles & hot spots
        random.seed(int(t / 100))
        for _ in range(12):
            bx = random.randint(0, width)
            by = lava_y + random.randint(2, 30)
            bubble_r = random.randint(2, 5)
            pygame.draw.circle(surface, (255, 200, 50), (bx, by), bubble_r)
            pygame.draw.circle(surface, (255, 255, 150), (bx - 1, by - 1), max(1, bubble_r - 2))
        
        # Rising heat sparks
        for i in range(8):
            sx = random.randint(0, width)
            sy = int(ground_top - (t / 5 + i * 50) % 60)
            pygame.draw.circle(surface, (255, 150, 50), (sx, sy), 1)

def draw_health_bar(surface, x, y, current_hp, max_hp):
    """Draws a health bar with numbers as requested."""
    bar_width = 200
    bar_height = 25
    
    # Background
    pygame.draw.rect(surface, (50, 50, 50), (x, y, bar_width, bar_height), border_radius=5)
    
    # Fill
    health_pct = max(0, current_hp / max_hp)
    fill_width = int(bar_width * health_pct)
    
    # Color based on health
    color = (0, 255, 0)
    if health_pct < 0.6: color = (255, 255, 0)
    if health_pct < 0.3: color = (255, 0, 0)
    
    if fill_width > 0:
        pygame.draw.rect(surface, color, (x, y, fill_width, bar_height), border_radius=5)
    
    # Border
    pygame.draw.rect(surface, WHITE, (x, y, bar_width, bar_height), 2, border_radius=5)
    
    # Text
    font = pygame.font.SysFont("Arial", 18, bold=True)
    text = font.render(f"{current_hp}/{max_hp}", True, WHITE)
    text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
    surface.blit(text, text_rect)

def draw_lightning_bolt(surface, start_pos, end_pos):
    """Draws a CINEMATIC plasma lightning bolt with multi-layer glow, branches, and impact effects."""
    
    t = pygame.time.get_ticks()
    
    # Create alpha surface for proper glow blending
    bolt_s = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    
    # 1. Main Bolt Logic (Enhanced recursion)
    def recursive_bolt(surf, start, end, depth, displace, width_scale, is_branch=False):
        if depth == 0:
            s_x, s_y = int(start[0]), int(start[1])
            e_x, e_y = int(end[0]), int(end[1])
            
            # Outer plasma glow (wide, purple-blue)
            for w in range(width_scale + 6, width_scale + 1, -1):
                alpha = 30 + (width_scale + 6 - w) * 10
                col = (100, 80, 255, min(255, alpha))
                pygame.draw.line(surf, col, (s_x, s_y), (e_x, e_y), w)
            
            # Mid glow (electric blue)
            pygame.draw.line(surf, (150, 180, 255, 200), (s_x, s_y), (e_x, e_y), max(1, width_scale))
            
            # Core (bright white with slight cyan)
            if not is_branch:
                pygame.draw.line(surf, (220, 240, 255), (s_x, s_y), (e_x, e_y), max(1, width_scale - 1))
                pygame.draw.line(surf, (255, 255, 255), (s_x, s_y), (e_x, e_y), max(1, width_scale - 3))
            else:
                pygame.draw.line(surf, (180, 200, 255), (s_x, s_y), (e_x, e_y), max(1, width_scale - 2))
            return

        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        
        # Perpendicular vector
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        px, py = -dy, dx
        L = math.hypot(px, py)
        if L > 0: px /= L; py /= L
            
        # Increased jitter for more dramatic shape
        offset = (random.random() - 0.5) * displace
        mid = (mid_x + px * offset, mid_y + py * offset)
        
        recursive_bolt(surf, start, mid, depth - 1, displace * 0.55, width_scale, is_branch)
        recursive_bolt(surf, mid, end, depth - 1, displace * 0.55, width_scale, is_branch)
        
        # Branches (more frequent, more dramatic)
        if depth > 2 and random.random() < 0.4:
            # Branch direction biased towards the main bolt direction
            base_angle = math.atan2(dy, dx)
            branch_angle = base_angle + random.uniform(-1.2, 1.2)
            length = displace * 0.65
            bx = mid[0] + math.cos(branch_angle) * length
            by = mid[1] + math.sin(branch_angle) * length
            recursive_bolt(surf, mid, (bx, by), depth - 2, displace * 0.4, max(1, width_scale - 2), True)
    
    # Draw main bolt (deeper recursion for smoother look)
    recursive_bolt(bolt_s, start_pos, end_pos, 7, 90, 6)
    
    # Flicker effect (slight randomization per frame)
    if random.random() < 0.3:
        recursive_bolt(bolt_s, start_pos, end_pos, 5, 60, 3)
    
    surface.blit(bolt_s, (0, 0))
    
    # 2. Enhanced Impact Effect at end_pos
    impact_s = pygame.Surface((200, 200), pygame.SRCALPHA)
    icx, icy = 100, 100
    
    # Multi-layer impact glow
    pygame.draw.circle(impact_s, (80, 80, 255, 30), (icx, icy), 80)
    pygame.draw.circle(impact_s, (120, 120, 255, 60), (icx, icy), 50)
    pygame.draw.circle(impact_s, (180, 200, 255, 120), (icx, icy), 25)
    pygame.draw.circle(impact_s, (255, 255, 255, 220), (icx, icy), 10)
    pygame.draw.circle(impact_s, (255, 255, 255), (icx, icy), 4)
    surface.blit(impact_s, (int(end_pos[0]) - 100, int(end_pos[1]) - 100))
    
    # Expanding shock ring at impact
    ring_phase = (t % 300) / 300.0
    ring_r = int(10 + ring_phase * 40)
    ring_alpha = int(200 * (1.0 - ring_phase))
    ring_s = pygame.Surface((ring_r * 2 + 10, ring_r * 2 + 10), pygame.SRCALPHA)
    pygame.draw.circle(ring_s, (200, 200, 255, max(0, ring_alpha)), (ring_r + 5, ring_r + 5), ring_r, 2)
    surface.blit(ring_s, (int(end_pos[0]) - ring_r - 5, int(end_pos[1]) - ring_r - 5))
    
    # Spark particles radiating from impact
    for _ in range(15):
        spark_angle = random.uniform(0, 6.2832)
        spark_len = random.randint(10, 40)
        ix = int(end_pos[0]) + int(math.cos(spark_angle) * spark_len)
        iy = int(end_pos[1]) + int(math.sin(spark_angle) * spark_len)
        
        # Gradient spark line
        pygame.draw.line(surface, (200, 220, 255), (int(end_pos[0]), int(end_pos[1])), (ix, iy), 2)
        pygame.draw.circle(surface, (255, 255, 255), (ix, iy), 2)
    
    # 3. Origin point glow (at caster)
    origin_s = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.circle(origin_s, (150, 150, 255, 80), (30, 30), 25)
    pygame.draw.circle(origin_s, (200, 200, 255, 150), (30, 30), 12)
    pygame.draw.circle(origin_s, (255, 255, 255), (30, 30), 4)
    surface.blit(origin_s, (int(start_pos[0]) - 30, int(start_pos[1]) - 30))
    
    # 4. Screen flash (dramatic effect)
    if random.random() < 0.25:
        s_flash = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        flash_intensity = random.randint(20, 50)
        s_flash.fill((180, 200, 255, flash_intensity))
        surface.blit(s_flash, (0, 0))

def draw_tornado_effect(surface, x, y, life_counter):
    """Draws a CINEMATIC volumetric tornado with swirling debris, wind streaks, and ground effects."""
    
    t = pygame.time.get_ticks() / 120  # Smooth rotation speed
    
    # Tornado Parameters
    height = 300
    top_width = 180
    base_width = 18
    
    # 1. GROUND DUST CLOUD (Realistic spreading dust)
    for layer in range(3):
        for i in range(8):
            angle = (t * 2.5 + i * 0.78 + layer * 0.3)
            dist = 15 + i * 6 + layer * 8
            dx = x + math.cos(angle) * dist
            dy = y - 5 + math.sin(angle * 0.5) * 4 + layer * 3
            
            dust_w = 30 + layer * 15
            dust_h = 14 + layer * 4
            s_dust = pygame.Surface((dust_w, dust_h), pygame.SRCALPHA)
            dust_alpha = 80 - layer * 20
            pygame.draw.ellipse(s_dust, (120, 110, 90, max(0, dust_alpha)), (0, 0, dust_w, dust_h))
            surface.blit(s_dust, (dx - dust_w//2, dy - dust_h//2))
    
    # 2. FUNNEL BODY (Volumetric stacked rings with depth)
    segments = 50
    for i in range(segments):
        prog = i / segments  # 0 (bottom) to 1 (top)
        
        # Non-linear width curve (exponential opening)
        current_w = base_width + (top_width - base_width) * (prog ** 1.4)
        
        # Multi-frequency wobble for organic wind feel
        wobble_x = (math.sin(t * 1.2 + i * 0.15) * (12 * prog) + 
                    math.sin(t * 0.7 + i * 0.3) * (5 * prog))
        
        rect_x = x - current_w // 2 + wobble_x
        rect_y = y - (prog * height) - 15
        
        # Color Gradient: Dark Earth (Base) -> Storm Grey -> Cloudy White (Top)
        if prog < 0.3:
            # Brown-grey earth
            r_c = int(70 + prog * 200)
            g_c = int(60 + prog * 180)
            b_c = int(50 + prog * 200)
        elif prog < 0.7:
            # Storm grey
            mid_prog = (prog - 0.3) / 0.4
            r_c = int(130 + mid_prog * 60)
            g_c = int(120 + mid_prog * 60)
            b_c = int(110 + mid_prog * 80)
        else:
            # Light cloud top
            top_prog = (prog - 0.7) / 0.3
            r_c = int(190 + top_prog * 40)
            g_c = int(180 + top_prog * 40)
            b_c = int(190 + top_prog * 40)
        
        # Ring thickness varies with height
        ring_h = int(6 + prog * 8)
        
        # Back ring (darker shadow)
        s_ring = pygame.Surface((int(current_w) + 20, ring_h + 8), pygame.SRCALPHA)
        shadow_col = (max(0, r_c - 30), max(0, g_c - 30), max(0, b_c - 30), 130)
        pygame.draw.ellipse(s_ring, shadow_col, (8, 2, int(current_w), ring_h))
        surface.blit(s_ring, (rect_x - 8, rect_y))
        
        # Front ring (brighter)
        s_front = pygame.Surface((int(current_w) + 20, ring_h + 4), pygame.SRCALPHA)
        front_col = (min(255, r_c + 10), min(255, g_c + 10), min(255, b_c + 10), 160)
        pygame.draw.ellipse(s_front, front_col, (10, 0, int(current_w) - 4, ring_h - 2))
        surface.blit(s_front, (rect_x - 6, rect_y + 1))
        
        # Helix wind streaks (orbiting highlights)
        for helix in range(2):
            orbit_ang = t * (4.5 - prog * 1.5) + i * 0.4 + helix * 3.14
            ox = math.cos(orbit_ang) * (current_w * 0.42)
            oy_depth = math.sin(orbit_ang)  # -1 to 1 for depth
            
            # Only draw on front side (z-sorting simulation)
            if oy_depth > -0.2:
                streak_alpha = int(120 + oy_depth * 80)
                streak_len = int(8 + prog * 6)
                sx = x + wobble_x + ox
                sy = rect_y + ring_h // 2
                
                streak_s = pygame.Surface((streak_len + 4, 4), pygame.SRCALPHA)
                pygame.draw.line(streak_s, (255, 255, 255, min(255, max(0, streak_alpha))), 
                               (0, 2), (streak_len, 2), 2)
                surface.blit(streak_s, (sx - streak_len // 2, sy - 2))

    # 3. DEBRIS (Multi-type: rocks, wood, leaves)
    for i in range(18):
        d_prog = ((t * 0.18 + i * 0.055) % 1.0)
        d_h = d_prog * height
        d_w = base_width + (top_width - base_width) * (d_prog ** 1.4)
        
        d_angle = t * 5.5 + i * 19.7
        d_x = x + math.cos(d_angle) * (d_w * 0.55)
        d_y = y - d_h - 15
        
        is_front = math.sin(d_angle) > 0
        
        # Different debris types
        debris_type = i % 3
        if debris_type == 0:
            # Rock
            size = 5 + (i % 4)
            col = (80, 70, 60) if is_front else (50, 40, 30)
        elif debris_type == 1:
            # Wood splinter
            size = 4 + (i % 3)
            col = (120, 80, 40) if is_front else (80, 50, 25)
        else:
            # Leaf
            size = 3 + (i % 3)
            col = (60, 120, 30) if is_front else (40, 80, 20)
        
        if is_front:
            # Spinning rotation for debris
            rot_ang = t * 8 + i * 5
            s_deb = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pts = []
            for corner in range(4):
                ca = rot_ang + corner * 1.57
                pts.append((size + int(math.cos(ca) * size * 0.7), 
                           size + int(math.sin(ca) * size * 0.7)))
            if len(pts) >= 3:
                pygame.draw.polygon(s_deb, col, pts)
                pygame.draw.polygon(s_deb, (0, 0, 0), pts, 1)
            surface.blit(s_deb, (d_x - size, d_y - size))
        else:
            # Behind (dimmer, smaller)
            alpha_d = 100
            s_deb = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.rect(s_deb, (*col, alpha_d), (0, 0, size, size))
            surface.blit(s_deb, (d_x, d_y))
    
    # 4. Wind speed lines (radiating from base)
    for i in range(6):
        wind_ang = t * 3 + i * 1.05
        wind_dist = 30 + math.sin(t + i) * 15
        wx = x + math.cos(wind_ang) * wind_dist
        wy = y - 5
        wex = wx + math.cos(wind_ang) * 25
        wey = wy - 3
        
        wind_s = pygame.Surface((60, 10), pygame.SRCALPHA)
        pygame.draw.line(wind_s, (200, 200, 200, 80), (0, 5), (50, 5), 1)
        surface.blit(wind_s, (min(wx, wex) - 5, wy - 5))
    
    # 5. Vortex glow at core (subtle inner light)
    vortex_s = pygame.Surface((60, int(height * 0.4)), pygame.SRCALPHA)
    vortex_alpha = 20 + int(math.sin(t * 2) * 10)
    pygame.draw.ellipse(vortex_s, (200, 220, 255, max(0, vortex_alpha)), (0, 0, 60, int(height * 0.4)))
    surface.blit(vortex_s, (x - 30, y - int(height * 0.5)))

def draw_dragon_effect(surface, x, y, life_counter):
    """CINEMATIC Dragon with detailed head, layered fire breath, and atmospheric effects."""
    
    t = pygame.time.get_ticks()
    
    # 1. Screen Darken with vignette
    shake_x = random.randint(-4, 4)
    shake_y = random.randint(-4, 4)
    
    # Dark overlay with vignette gradient
    s_dark = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    s_dark.fill((0, 0, 0, 140))
    surface.blit(s_dark, (0, 0))
    
    # Red atmospheric tint (heat)
    s_heat = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    s_heat.fill((40, 0, 0, 40))
    surface.blit(s_heat, (0, 0))
    
    # 2. DRAGON HEAD (Detailed with scales, horns, and features)
    head_y = 55 + math.sin(t / 250) * 15 + shake_y
    head_x = x + shake_x
    
    # A. Head base silhouette (dark crimson with depth layers)
    # Back layer (darker, slightly larger for depth)
    pygame.draw.polygon(surface, (15, 0, 0), [
        (head_x - 110, head_y - 155),
        (head_x + 110, head_y - 155),
        (head_x + 185, head_y - 260),
        (head_x + 130, head_y - 55),
        (head_x + 65, head_y + 55),
        (head_x, head_y + 85),
        (head_x - 65, head_y + 55),
        (head_x - 130, head_y - 55),
        (head_x - 185, head_y - 260),
    ])
    
    # Main head
    pygame.draw.polygon(surface, (35, 5, 5), [
        (head_x - 100, head_y - 150),
        (head_x + 100, head_y - 150),
        (head_x + 180, head_y - 250),
        (head_x + 120, head_y - 50),
        (head_x + 60, head_y + 50),
        (head_x, head_y + 80),
        (head_x - 60, head_y + 50),
        (head_x - 120, head_y - 50),
        (head_x - 180, head_y - 250),
    ])
    
    # B. Scale texture (subtle lighter patches)
    for sx in range(-80, 80, 25):
        for sy in range(-130, 40, 20):
            scale_alpha = random.randint(10, 30)
            ss = pygame.Surface((12, 8), pygame.SRCALPHA)
            pygame.draw.ellipse(ss, (60, 10, 10, scale_alpha), (0, 0, 12, 8))
            surface.blit(ss, (head_x + sx, head_y + sy))
    
    # C. Horn ridges (detailed)
    for horn_side in [-1, 1]:
        horn_base_x = head_x + horn_side * 130
        horn_base_y = head_y - 150
        horn_tip_x = head_x + horn_side * 180
        horn_tip_y = head_y - 255
        
        # Horn body
        pygame.draw.line(surface, (60, 40, 20), (horn_base_x, horn_base_y), (horn_tip_x, horn_tip_y), 8)
        # Horn highlight
        pygame.draw.line(surface, (100, 70, 40), (horn_base_x + horn_side * 2, horn_base_y), 
                        (horn_tip_x + horn_side * 2, horn_tip_y), 3)
        # Horn ridges
        for ridge in range(4):
            rp = ridge / 4.0
            rx = int(horn_base_x + (horn_tip_x - horn_base_x) * rp)
            ry = int(horn_base_y + (horn_tip_y - horn_base_y) * rp)
            pygame.draw.line(surface, (80, 50, 30), (rx - 4 * horn_side, ry - 2), (rx + 4 * horn_side, ry + 2), 2)
    
    # D. Snout / Nose bridge
    pygame.draw.polygon(surface, (45, 8, 8), [
        (head_x - 30, head_y + 20),
        (head_x + 30, head_y + 20),
        (head_x + 20, head_y + 60),
        (head_x, head_y + 75),
        (head_x - 20, head_y + 60),
    ])
    # Nostrils
    for ns in [-1, 1]:
        pygame.draw.ellipse(surface, (0, 0, 0), (head_x + ns * 12 - 5, head_y + 55, 10, 6))
        # Nostril ember glow
        ember_alpha = 150 + int(math.sin(t / 100 + ns) * 50)
        ns_s = pygame.Surface((14, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(ns_s, (255, 80, 0, max(0, min(255, ember_alpha))), (0, 0, 14, 10))
        surface.blit(ns_s, (head_x + ns * 12 - 7, head_y + 52))
    
    # E. Eyes (Fierce with iris detail)
    for eye_side in [-1, 1]:
        eye_cx = head_x + eye_side * 50
        eye_cy = head_y - 30
        
        # Eye socket shadow
        pygame.draw.ellipse(surface, (10, 0, 0), (eye_cx - 25, eye_cy - 22, 50, 44))
        
        # Eye glow halo
        eye_glow = pygame.Surface((70, 60), pygame.SRCALPHA)
        pygame.draw.ellipse(eye_glow, (255, 50, 0, 60), (0, 0, 70, 60))
        surface.blit(eye_glow, (eye_cx - 35, eye_cy - 30))
        
        # Iris (fiery orange-red)
        pygame.draw.ellipse(surface, (255, 80, 0), (eye_cx - 18, eye_cy - 18, 36, 36))
        # Inner iris ring
        pygame.draw.ellipse(surface, (255, 150, 0), (eye_cx - 12, eye_cy - 12, 24, 24))
        
        # Vertical slit pupil
        pygame.draw.rect(surface, (0, 0, 0), (eye_cx - 4, eye_cy - 16, 8, 32))
        # Pupil highlight
        pygame.draw.circle(surface, (255, 255, 200), (eye_cx - 6, eye_cy - 8), 3)
    
    # F. Teeth / Fangs
    for tooth in range(-3, 4):
        tx = head_x + tooth * 12
        ty_top = head_y + 65
        tooth_len = 8 + abs(tooth) * 3
        pygame.draw.polygon(surface, (220, 220, 200), [
            (tx - 3, ty_top), (tx + 3, ty_top), (tx, ty_top + tooth_len)
        ])
    
    # 3. FIRE BREATH (Multi-jet volumetric)
    fire_start_y = head_y + 70
    
    # Three interleaved fire jets for volumetric look
    for jet in range(3):
        jet_offset_x = (jet - 1) * 15
        jet_phase = jet * 0.5
        
        for i in range(120):
            prog = i / 120.0
            
            # Turbulent wiggle
            wiggle = (math.sin(t / 45 + i / 8 + jet_phase) * (40 * prog) +
                     math.sin(t / 25 + i / 5 + jet_phase) * (20 * prog))
            
            stream_x = head_x + jet_offset_x + wiggle
            stream_y = fire_start_y + i * 6
            
            if stream_y > SCREEN_HEIGHT + 20:
                break
            
            # Expanding width
            width = 30 + (prog * 500)
            
            # Multiple particles per row for density
            num_particles = 2 + int(prog * 4)
            for p_idx in range(num_particles):
                px = stream_x + random.randint(int(-width / 2), int(width / 2))
                
                # 8-step color gradient: White -> Yellow-white -> Yellow -> Orange -> Deep orange -> Red -> Dark red -> Smoke
                if prog < 0.05:
                    col = (255, 255, 255)
                elif prog < 0.12:
                    col = (255, 255, 180)
                elif prog < 0.2:
                    col = (255, 255, 80)
                elif prog < 0.3:
                    col = (255, 200, 0)
                elif prog < 0.45:
                    col = (255, 130, 0)
                elif prog < 0.6:
                    col = (230, 60, 0)
                elif prog < 0.8:
                    col = (150, 30, 0)
                else:
                    col = (60, 20, 10)
                
                # Alpha decreases at edges
                alpha = random.randint(80, 200) - int(prog * 80)
                alpha = max(20, min(255, alpha))
                
                # Size grows with distance
                size = int(8 + prog * 60)
                
                s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*col, alpha), (size, size), size)
                surface.blit(s, (px - size, stream_y - size))
    
    # 4. Embers floating upward (with velocity trails)
    for i in range(30):
        ember_seed = (t // 30 + i * 17) % 1000
        random.seed(ember_seed)
        
        ex = random.randint(int(head_x - 300), int(head_x + 300))
        ey_base = random.randint(0, SCREEN_HEIGHT)
        # Float upward based on time
        ey = int(ey_base - (t / 10 + i * 20) % SCREEN_HEIGHT)
        if ey < 0:
            ey += SCREEN_HEIGHT
        
        ember_size = random.randint(2, 5)
        ember_s = pygame.Surface((ember_size * 2 + 4, ember_size * 2 + 4), pygame.SRCALPHA)
        
        # Ember glow
        pygame.draw.circle(ember_s, (255, 200, 50, 100), (ember_size + 2, ember_size + 2), ember_size + 2)
        pygame.draw.circle(ember_s, (255, 255, 100, 220), (ember_size + 2, ember_size + 2), ember_size)
        
        # Trail line
        trail_len = random.randint(5, 15)
        pygame.draw.line(ember_s, (255, 150, 0, 80), (ember_size + 2, ember_size + 2), 
                        (ember_size + 2, ember_size + 2 + trail_len), 1)
        
        surface.blit(ember_s, (ex - ember_size - 2, ey - ember_size - 2))
    
    # Reset random seed
    random.seed()
    
    # 5. Heat wave distortion overlay
    heat_s = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for hy in range(0, SCREEN_HEIGHT, 40):
        wave_x = int(math.sin(t / 100 + hy / 50) * 3)
        heat_alpha = 8 + int(math.sin(t / 150 + hy / 30) * 5)
        pygame.draw.line(heat_s, (255, 100, 0, max(0, min(255, heat_alpha))), 
                        (wave_x, hy), (SCREEN_WIDTH + wave_x, hy), 2)
    surface.blit(heat_s, (0, 0))


def draw_dragon_boss(surface, x, y, facing_right, scale=1.0, tick=0, is_attacking=False, attack_phase=0.0):
    """Draws a massive, animated Dragon Boss entity."""
    
    direction = 1 if facing_right else -1
    
    # Canvas setup
    w, h = int(500 * scale), int(500 * scale)
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w//2, h//2
    
    # Animation Parameters
    hover_y = math.sin(tick / 250) * (20 * scale)
    wing_phase = math.sin(tick / 150)
    breath_pulse = (math.sin(tick / 100) + 1.5) * 0.5 # 0.5 to 1.25
    
    # Position adjustments
    body_x = cx
    body_y = cy + hover_y
    
    # 1. WINGS (Behind Body)
    wing_span = 180 * scale
    wing_h = (100 + wing_phase * 40) * scale
    wing_root_y = body_y - 40 * scale
    
    wing_col_outer = (50, 10, 10)
    wing_col_inner = (80, 30, 10)
    
    # Draw far wing first
    far_side = -direction
    wx_far = body_x + (far_side * 20 * scale)
    wt_x_far = wx_far + (far_side * wing_span)
    wt_y_far = wing_root_y - wing_h
    
    # Wing polygon points
    wing_pts_far = [
        (wx_far, wing_root_y),
        (wt_x_far, wt_y_far),
        (wt_x_far - (far_side * 40 * scale), wt_y_far + 120 * scale),
        (wx_far, wing_root_y + 60 * scale)
    ]
    pygame.draw.polygon(s, wing_col_outer, wing_pts_far)
    pygame.draw.polygon(s, wing_col_inner, [wing_pts_far[0], wing_pts_far[1], wing_pts_far[2]]) # Membrane
    
    # 2. TAIL
    tail_pts = []
    for i in range(12):
        tx = body_x - (i * 15 * direction * scale) - (math.sin(tick/200 + i*0.4) * 10 * scale)
        ty = body_y + (i * 8 * scale) + (math.cos(tick/200 + i*0.4) * 5 * scale)
        size = (40 - i * 3) * scale
        pygame.draw.circle(s, (70, 20, 20), (int(tx), int(ty)), int(size))
        
    # 3. BODY (Main Mass)
    body_rect = pygame.Rect(0, 0, 100 * scale, 140 * scale)
    body_rect.center = (body_x, body_y)
    pygame.draw.ellipse(s, (90, 20, 20), body_rect)
    
    # Scales on belly
    pygame.draw.ellipse(s, (110, 40, 20), (body_rect.centerx - 30*scale, body_rect.top + 20*scale, 60*scale, 100*scale))

    # 4. NEAR WING
    near_side = direction
    wx_near = body_x + (near_side * 10 * scale)
    wt_x_near = wx_near + (near_side * wing_span)
    wt_y_near = wing_root_y - wing_h
    
    wing_pts_near = [
        (wx_near, wing_root_y),
        (wt_x_near, wt_y_near),
        (wt_x_near - (near_side * 40 * scale), wt_y_near + 120 * scale),
        (wx_near, wing_root_y + 60 * scale)
    ]
    pygame.draw.polygon(s, wing_col_outer, wing_pts_near)
    pygame.draw.polygon(s, wing_col_inner, [wing_pts_near[0], wing_pts_near[1], wing_pts_near[2]])

    # 5. NECK & HEAD
    neck_len = 70 * scale
    head_pos_x = body_x + (50 * direction * scale)
    head_pos_y = body_y - neck_len
    
    # Neck curve
    pygame.draw.line(s, (90, 20, 20), (body_x, body_y - 40*scale), (head_pos_x, head_pos_y), int(40*scale))
    
    # Head Shape
    head_size = 50 * scale
    pygame.draw.circle(s, (100, 30, 30), (int(head_pos_x), int(head_pos_y)), int(head_size))
    
    # Snout
    snout_len = 60 * scale
    snout_x = head_pos_x + (direction * snout_len)
    snout_y = head_pos_y + (10 * scale)
    
    pygame.draw.polygon(s, (100, 30, 30), [
        (head_pos_x, head_pos_y - 20*scale),
        (head_pos_x, head_pos_y + 20*scale),
        (snout_x, snout_y + 15*scale),
        (snout_x, snout_y - 15*scale)
    ])
    
    # Eye
    eye_x = head_pos_x + (15 * direction * scale)
    eye_y = head_pos_y - 10 * scale
    pygame.draw.circle(s, (255, 200, 0), (int(eye_x), int(eye_y)), int(8*scale))
    # Pupil (Cat eye slit)
    pygame.draw.rect(s, (0,0,0), (int(eye_x)-1, int(eye_y)-5, 2, 10))
    
    # Horns
    horn_base_x = head_pos_x - (10 * direction * scale)
    horn_base_y = head_pos_y - 25 * scale
    horn_tip_x = horn_base_x - (40 * direction * scale)
    horn_tip_y = horn_base_y - (50 * scale)
    pygame.draw.line(s, (200, 200, 180), (horn_base_x, horn_base_y), (horn_tip_x, horn_tip_y), int(6*scale))
    
    # ATTACK EFFECT (Fire Breath Charging/Releasing)
    if is_attacking:
        # Glow in throat
        pygame.draw.circle(s, (255, 100, 0, 150), (int(head_pos_x + 20*direction*scale), int(head_pos_y)), int(20*scale*breath_pulse))
        
        if attack_phase > 0.3: # Release Phase
            # Flamethrower
            fire_len = 250 * scale
            fx = snout_x
            fy = snout_y
            
            # Draw multiple transparent flame layers
            for i in range(5):
                alpha = 200 - i * 40
                width = 20 + i * 15
                col = (255, 100 + i*30, 0)
                
                # End point with spread
                end_x = fx + (fire_len * direction)
                end_y = fy + (i * 10 * scale)
                
                pygame.draw.line(s, (*col, alpha), (fx, fy), (end_x, end_y), int(width*scale))
                
                # Particles at end
                pygame.draw.circle(s, (*col, alpha), (int(end_x), int(end_y)), int(width*scale))


    surface.blit(s, s.get_rect(center=(x, y)))

def draw_dragon_cinematic_entrance(surface, progress):
    """
    Renders an EPIC intro sequence for the Dragon Boss.
    progress goes from 0.0 (start) to 1.0 (ready to fight).
    """
    w, h = surface.get_size()
    cx, cy = w//2, h//2
    t = pygame.time.get_ticks()
    
    # 1. Darken Sky (Weather Change)
    darkness = int(min(200, progress * 200)) # Fade to dark storm
    s_dark = pygame.Surface((w, h), pygame.SRCALPHA)
    s_dark.fill((20, 10, 30, darkness))
    surface.blit(s_dark, (0,0))
    
    # 2. Lightning Flashes (Dramatic Strobe)
    if 0.3 < progress < 0.8:
        if random.random() < 0.1: # Flash
            s_flash = pygame.Surface((w, h), pygame.SRCALPHA)
            s_flash.fill((200, 220, 255, random.randint(50, 150)))
            surface.blit(s_flash, (0,0))
            
    # 3. Dragon Descent
    # Starts high up (y = -300) and descends to fight pos (cy - 100)
    start_y = -400
    end_y = cy - 200
    
    # Non-linear ease out
    eased_prog = 1 - (1 - progress) ** 3  # Cubic ease out
    dragon_y = start_y + (end_y - start_y) * eased_prog
    
    # Scale grows as he gets closer (simulating flight down)
    current_scale = 0.5 + 0.5 * eased_prog # 0.5 -> 1.0
    
    # Draw Dragon
    draw_dragon_boss(surface, cx, dragon_y, facing_right=False, scale=current_scale * 1.8, tick=t, is_attacking=False)

    # 4. Roar Shockwave (at end of entrance)
    if progress > 0.8:
        wave_prog = (progress - 0.8) / 0.2
        wave_r = int(wave_prog * 800)
        pygame.draw.circle(surface, (255, 255, 255), (cx, int(dragon_y)), wave_r, 10)
        
    # Text
    if progress > 0.5:
        # Large menacing text
        font_big = pygame.font.SysFont("Verdana", 80, bold=True)
        txt = font_big.render("THE ANCIENT DRAGON", True, (255, 50, 0))
        rect = txt.get_rect(center=(cx, h - 150))
        surface.blit(txt, rect)
