
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
    """Draws a Green Ogre."""
    _draw_monster_base(surface, x, y, facing_right, scale, 
                       skin_color=(100, 140, 60), 
                       outfit_color=(139, 69, 19), 
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
    """Draws a Skeleton Archer with a Bow."""
    direction = 1 if facing_right else -1
    
    # Canvas
    w, h = 300, 300 
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w//2, h - 10
    
    # Animation
    walk_speed = tick / 150
    if is_attacking:
        walk_speed = 0
        leg_l_off = 0
        leg_r_off = 0
        # Draw Bow Draw animation
    else:
        stride = 10
        leg_l_off = math.sin(walk_speed) * stride
        leg_r_off = math.sin(walk_speed + math.pi) * stride

    # Colors
    BONE = (220, 220, 220)
    DARK_BONE = (180, 180, 180)
    
    # Legs (Bones)
    leg_w = 6
    leg_h = 40
    # Left
    pygame.draw.rect(s, BONE, (cx - 10 + leg_l_off*direction, cy - leg_h, leg_w, leg_h))
    # Right
    pygame.draw.rect(s, BONE, (cx + 10 + leg_r_off*direction, cy - leg_h, leg_w, leg_h))
    
    # Pelvis
    pygame.draw.rect(s, BONE, (cx - 15, cy - leg_h - 10, 30, 10))
    
    # Spine (Line)
    spine_bot = cy - leg_h - 10
    spine_top = spine_bot - 35
    pygame.draw.line(s, BONE, (cx, spine_bot), (cx, spine_top), 4)
    
    # Ribs
    for i in range(3):
        ry = spine_top + 10 + (i * 8)
        pygame.draw.line(s, BONE, (cx - 12, ry), (cx + 12, ry), 3)
        
    # Head (Skull)
    head_y = spine_top - 20
    pygame.draw.circle(s, BONE, (cx, head_y), 14) # Skull
    pygame.draw.rect(s, BONE, (cx - 8, head_y + 8, 16, 10)) # Jaw
    # Eyes
    pygame.draw.circle(s, (0, 0, 0), (cx + 5*direction, head_y), 3)
    
    # Arms (Holding Bow)
    # Shoulder
    shoulder_y = spine_top + 5
    
    # Bow Arm (Front)
    arm_len = 30
    hand_x = cx + arm_len * direction
    hand_y = shoulder_y
    
    pygame.draw.line(s, BONE, (cx, shoulder_y), (hand_x, hand_y), 4)
    
    # Bow Logic
    # Vertical Arc
    bow_top = (hand_x, hand_y - 30)
    bow_bot = (hand_x, hand_y + 30)
    # Draw arc (simple lines)
    curve_x = hand_x + 10 * direction
    pygame.draw.lines(s, (139, 69, 19), False, [bow_top, (curve_x, hand_y), bow_bot], 3)
    # String
    draw_pct = 0.0
    if is_attacking:
        # Pull back string based on phase
        # Phase 0 -> 0.5 (Pull), 0.5 -> 1.0 (Release/Hold)
        if attack_phase < 0.5:
             draw_pct = attack_phase * 2.0
        else:
             draw_pct = 0.0 # Released
             
    string_x = hand_x - (draw_pct * 20 * direction)
    pygame.draw.line(s, (200, 200, 200), bow_top, (string_x, hand_y), 1)
    pygame.draw.line(s, (200, 200, 200), bow_bot, (string_x, hand_y), 1)
    
    # Arrow
    if is_attacking and attack_phase < 0.5:
        arrow_end = (string_x, hand_y)
        arrow_tip = (hand_x + 10 * direction, hand_y)
        pygame.draw.line(s, (255, 0, 0), arrow_end, arrow_tip, 2)

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
    # Head bobs slightly less than body for stability focus
    head_y = body_y_top - head_size + 10 
    head_x = cx
    
    # Thick Neck
    pygame.draw.rect(s, skin_shadow, (cx - 12, body_y_top - 5, 24, 15))
    
    # Face Shape (Square Jaw)
    pygame.draw.circle(s, skin_color, (head_x, head_y), head_size)
    pygame.draw.rect(s, skin_color, (head_x - head_size + 2, head_y, head_size*2 - 4, head_size), border_radius=5)
    
    # Shading under chin
    pygame.draw.rect(s, skin_shadow, (head_x - head_size + 5, head_y + head_size - 4, head_size*2 - 10, 4))

    # Facial Features
    eye_y = head_y - 2
    eye_off = 9
    
    # Brows (Angry V)
    pygame.draw.line(s, (30, 20, 10), (head_x - 15, eye_y - 6), (head_x, eye_y), 3)
    pygame.draw.line(s, (30, 20, 10), (head_x + 15, eye_y - 6), (head_x, eye_y), 3)
    
    # Glowing Eyes
    pygame.draw.circle(s, (255, 0, 0), (head_x + eye_off * direction, eye_y), 4) # Main Eye
    pygame.draw.circle(s, (255, 200, 100), (head_x + eye_off * direction, eye_y), 1) # Pupil glare
    
    # Tusks (Protruding Up)
    if not is_goblin:
        tusk_color = (240, 240, 220)
        # Left
        pygame.draw.polygon(s, tusk_color, [(head_x-10, head_y+15), (head_x-10, head_y+5), (head_x-14, head_y+8)])
        # Right
        pygame.draw.polygon(s, tusk_color, [(head_x+10, head_y+15), (head_x+10, head_y+5), (head_x+14, head_y+8)])
    
    # Ears (Pointed)
    ear_y = head_y - 5
    pygame.draw.polygon(s, skin_shadow, [(head_x-head_size, ear_y), (head_x-head_size-15, ear_y-10), (head_x-head_size, ear_y+5)])
    pygame.draw.polygon(s, skin_shadow, [(head_x+head_size, ear_y), (head_x+head_size+15, ear_y-10), (head_x+head_size, ear_y+5)])

    # 6. Arms & Shoulders
    
    # Spiked Shoulder Pads
    if not is_goblin:
        pad_size = 20
        # Draw Left Pad
        pygame.draw.circle(s, (50, 50, 60), (cx - shoulder_w//2, body_y_top + 5), pad_size)
        pygame.draw.line(s, (200, 200, 200), (cx - shoulder_w//2, body_y_top), (cx - shoulder_w//2 - 10, body_y_top - 15), 4) # Spike
        # Draw Right Pad
        pygame.draw.circle(s, (50, 50, 60), (cx + shoulder_w//2, body_y_top + 5), pad_size)
        pygame.draw.line(s, (200, 200, 200), (cx + shoulder_w//2, body_y_top), (cx + shoulder_w//2 + 10, body_y_top - 15), 4) # Spike

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
    """Draws different projectile visualization based on type."""
    
    t = pygame.time.get_ticks()
    
    # --- PARTICLE TRAIL (Universalish) ---
    if particles:
        for p in particles:
             px, py, vx, vy, life, max_life, size = p
             alpha = int((life / max_life) * 200)
             if alpha <= 0: continue
             
             # Color based on type can be refined
             col = color
             if p_type == "FIRE_RING": col = (255, 100, 0)
             elif p_type == "VOID_LANCE": col = (100, 0, 200)
             elif p_type == "ARCANE_VOLLEY": col = (150, 50, 255)
             else: # Default fireball particles
                progress = 1.0 - (life / max_life)
                if progress < 0.2:
                    col = (255, 255, 100) # Bright Yellow start
                elif progress < 0.5:
                    col = (255, 140, 0)   # Orange Mid
                elif progress < 0.8:
                    col = (200, 50, 50)   # Red fade
                else:
                    col = (100, 100, 100) # Grey smoke
             
             s = pygame.Surface((int(size)*2, int(size)*2), pygame.SRCALPHA)
             if len(col) == 3: col = (*col, alpha)
             else: col = (col[0], col[1], col[2], alpha)
             
             pygame.draw.circle(s, col, (int(size), int(size)), int(size))
             surface.blit(s, (px - size, py - size))

    if p_type == "FIRE_RING":
        # --- SIMPLE COMPACT FIRE RING ---
        # User requested: Smaller, simple circle with fire around, mini trail.
        
        # 1. Size Setup
        # Much smaller than before.
        ring_radius = 20 * scale 
        s_size = int(ring_radius * 2.8) 
        s_ring = pygame.Surface((s_size, s_size), pygame.SRCALPHA)
        cx, cy = s_size//2, s_size//2
        
        # Rotation for the fire texture on the ring
        rot_offset = t / 50.0

        # 2. Draw The Ring (Donut)
        # Main Body - Orange/Red
        pygame.draw.circle(s_ring, (255, 100, 0), (cx, cy), int(ring_radius), 4) # Thick ring
        pygame.draw.circle(s_ring, (255, 200, 50), (cx, cy), int(ring_radius - 2), 2) # Inner brightness
        
        # 3. Fire Effects ON the ring (Circumference)
        # Draw small flames along the ring edge
        num_flames = 8
        for i in range(num_flames):
            angle = (i / num_flames) * 6.28 + rot_offset
            
            # Flame position on ring edge
            fx = cx + math.cos(angle) * ring_radius
            fy = cy + math.sin(angle) * ring_radius
            
            # Flame Size (oscillating)
            f_size = 4 * scale + math.sin(t/100 + i)*2
            
            # Draw flame puff
            pygame.draw.circle(s_ring, (255, 150, 0, 150), (int(fx), int(fy)), int(f_size))
            pygame.draw.circle(s_ring, (255, 255, 100, 200), (int(fx), int(fy)), int(f_size*0.6))

        # 4. Center Hole (Ensure it looks like a ring)
        # (Already achieved by drawing ring with thickness, but let's be sure)
        
        # Blit
        surface.blit(s_ring, (x - s_size//2, y - s_size//2))
            
    elif p_type == "VOID_LANCE":
        # Long, thin, dark beam
        # Since it moves fast, maybe draw a trail line?
        # Just simple shape for now
        # Ellipse stretched
        w, h = 40 * scale, 10 * scale
        # Ideally rotated by velocity, but we only have facing direction via velocity normally...
        # We'll just draw a generic "bolt" shape
        pygame.draw.ellipse(surface, (50, 0, 100), (x - w//2, y - h//2, w, h))
        pygame.draw.ellipse(surface, (200, 100, 255), (x - w//2 + 5, y - h//4, w - 10, h//2)) # Core
        
    elif p_type == "ARCANE_VOLLEY":
        # Small unstable orbs
        pulse = math.sin(t/50) * 2
        r = 6 * scale + pulse
        pygame.draw.circle(surface, (150, 50, 255), (x, y), int(r))
        pygame.draw.circle(surface, (200, 200, 255), (x, y), int(r*0.6))
        
    else:
        # DEFAULT FIREBALL (Original Logic)
        # 2. Draw Fireball Core (The actual projectile)
        base_radius = 16 * scale
        
        # Pulsing size for "burning" effect
        pulse = math.sin(t / 50) * (3 * scale)
        
        # Outer Glow (Red/Orange Halo)
        radius_outer = base_radius + pulse
        s_glow = pygame.Surface((int(radius_outer*3), int(radius_outer*3)), pygame.SRCALPHA)
        pygame.draw.circle(s_glow, (255, 69, 0, 80), (int(radius_outer*1.5), int(radius_outer*1.5)), int(radius_outer))
        surface.blit(s_glow, (x - radius_outer*1.5, y - radius_outer*1.5))
        
        # Inner Fire (Orange/Yellow)
        radius_mid = (10 * scale) + pulse * 0.5
        pygame.draw.circle(surface, (255, 160, 0), (x, y), int(radius_mid))
        
        # Core (White hot center)
        radius_core = 6 * scale
        pygame.draw.circle(surface, (255, 255, 220), (x, y), int(radius_core))
        
        # 3. Extra "Sparks" orbiting/jittering
        random.seed(int(t/20))
        for _ in range(int(3 * scale)):
            range_s = 15 * scale
            sx = x + random.uniform(-range_s, range_s)
            sy = y + random.uniform(-range_s, range_s)
            pygame.draw.circle(surface, (255, 255, 100), (sx, sy), int(2*scale))

def draw_background_scenery(surface, biome, width, height, scroll_x=0):
    """Draws a HIGH QUALITY background with parallax-like depth and details."""
    
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
        # 1. Sky & Sun (Static)
        draw_gradient(surface, (30, 100, 180), (160, 220, 255), pygame.Rect(0, 0, width, height))
        
        # Sun & God Rays
        sun_x, sun_y = width - 150, 100
        pygame.draw.circle(surface, (255, 255, 200), (sun_x, sun_y), 60) 
        
        # God Rays (Animated Transparency)
        # These move slightly, which is allowed (light effect), but trees/mountains must be static.
        ray_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        t_ray = pygame.time.get_ticks() / 1000
        for i in range(5):
            start_x = sun_x
            start_y = sun_y
            end_x = width - 300 - (i * 200) + math.sin(t_ray + i)*20
            poly = [(start_x, start_y), (end_x, height), (end_x + 100, height)]
            pygame.draw.polygon(ray_surface, (255, 255, 220, 20), poly)
        surface.blit(ray_surface, (0,0))

        # 2. Far Mountains (Static)
        random.seed(10) # Seed 1
        for i in range(0, width, 120):
            h_mount = 200 + random.randint(0, 50) + int(math.sin(i/300)*80)
            color = (80, 90, 130)
            points = [(i, height), (i+150, height), (i+90, height-h_mount)]
            pygame.draw.polygon(surface, color, points)

        # 3. Dense Trees (Static)
        random.seed(42) # Seed 2 (Strictly separate)
        tree_color = (20, 60, 20)
        # Use a list to store tree props if needed, but deterministic gen is fine
        for i in range(-50, width, 80):
            # Deterministic jitter based on 'i'
            h_t = 180 + (i % 70) 
            
            # Trunk
            pygame.draw.rect(surface, (40, 30, 20), (i+20, height-h_t, 10, h_t))
            # Leaves (multiple layers)
            pygame.draw.polygon(surface, tree_color, [
                (i, height-h_t+50), (i+50, height-h_t+50), (i+25, height-h_t-50)
            ])
            pygame.draw.polygon(surface, tree_color, [
                (i-10, height-h_t+100), (i+60, height-h_t+100), (i+25, height-h_t)
            ])

        # 4. GROUND (Static)
        ground_top = height - 80
        pygame.draw.rect(surface, (30, 80, 30), (0, ground_top, width, 80))
        pygame.draw.rect(surface, (20, 60, 20), (0, ground_top, width, 10))
        
        # Grass (Static)
        random.seed(99) # Seed 3
        for i in range(0, width, 8):
            g_h = random.randint(5, 15)
            pygame.draw.line(surface, (50, 150, 50), (i, ground_top), (i-3, ground_top-g_h), 2)
            
        # Falling Leaves (Animated)
        t_leaf = pygame.time.get_ticks() / 10
        for i in range(20):
            lx = (i * 123 + t_leaf) % width
            ly = (i * 57 + t_leaf * 2) % (height-50) # Stop before ground roughly
            pygame.draw.circle(surface, (255, 200, 100), (lx, ly), 3)

    elif biome == "ICE":
        # 1. SKY (Twilight/Bright Arctic Night)
        # Much lighter than before to see details
        draw_gradient(surface, (10, 30, 80), (100, 180, 255), pygame.Rect(0, 0, width, height))
        
        # Stars (Subtle now)
        random.seed(555)
        for _ in range(50):
            sx = random.randint(0, width)
            sy = random.randint(0, int(height // 1.5)) # helper cast
            pygame.draw.circle(surface, (255, 255, 255), (sx, sy), 1)

        # Giant Frozen Moon (Left side, huge)
        moon_x = 100
        moon_y = 120
        pygame.draw.circle(surface, (230, 240, 255), (moon_x, moon_y), 90) # Base
        # Craters
        pygame.draw.circle(surface, (200, 220, 255), (moon_x-20, moon_y+10), 20)
        pygame.draw.circle(surface, (200, 220, 255), (moon_x+30, moon_y-30), 10)
        
        # Aurora (Bright & Visible)
        t_aur = pygame.time.get_ticks() / 2000
        s_aurora = pygame.Surface((width, height), pygame.SRCALPHA)
        for rib in range(3):
            points = []
            for x_a in range(0, width+20, 20):
                y_base = 100 + rib * 30
                y_off = math.sin(x_a/300 + t_aur + rib) * 50 + math.sin(x_a/100)*20
                points.append((x_a, y_base + y_off))
            
            if len(points) > 1:
                poly_pts = points + [(width, 0), (0, 0)]
                col = (50, 255, 200, 30) if rib == 0 else (150, 150, 255, 20)
                pygame.draw.polygon(s_aurora, col, poly_pts)
        surface.blit(s_aurora, (0,0))
        
        # 2. FROZEN SPIRES & CASTLE (Static)
        random.seed(777)
        # Background massive spikes (Lighter Blue/Purple)
        for i in range(0, width, 80):
            h_spike = 200 + random.randint(0, 300)
            poly = [
                (i, height),
                (i+40, height),
                (i+20, height - h_spike)
            ]
            pygame.draw.polygon(surface, (40, 60, 100), poly) # Lighter navy
            pygame.draw.line(surface, (150, 180, 255), (i+20, height), (i+20, height-h_spike), 1)

        # The Frozen Keep (Center) - More Visible
        k_x = width // 2 + 100
        k_y = height - 50
        # Main Tower
        pygame.draw.rect(surface, (60, 70, 110), (k_x-40, k_y-300, 80, 300))
        pygame.draw.polygon(surface, (60, 70, 110), [(k_x-50, k_y-300), (k_x+50, k_y-300), (k_x, k_y-450)])
        # Trim
        pygame.draw.rect(surface, (100, 120, 180), (k_x-30, k_y-300, 60, 300), 2)
        # Windows (Lit)
        if (pygame.time.get_ticks() // 500) % 2 == 0: # Blink
            pygame.draw.rect(surface, (200, 255, 255), (k_x-10, k_y-250, 20, 40))

        # 3. FROZEN LAKE GROUND (Reflective & Shiny)
        ground_top = height - 70
        pygame.draw.rect(surface, (150, 200, 230), (0, ground_top, width, 70)) # Base Ice
        pygame.draw.rect(surface, (255, 255, 255), (0, ground_top, width, 2)) # Horizon
        
        # Reflections of Spires
        s_ref = pygame.Surface((width, 70), pygame.SRCALPHA)
        random.seed(777) # Match spires
        for i in range(0, width, 80):
            h_spike = 200 + random.randint(0, 300)
            # Reflection is upside down, faded
            ref_h = h_spike * 0.3
            pygame.draw.polygon(s_ref, (255, 255, 255, 30), [
                (i, 0), (i+40, 0), (i+20, ref_h)
            ])
        surface.blit(s_ref, (0, ground_top))
        
        # 4. GLIMMERING SNOW & MIST
        # Rolling Mist (Low moving rects)
        t_mist = pygame.time.get_ticks() / 50
        for i in range(5):
             mx = (t_mist * (i+1) * 20) % (width + 400) - 200
             s_mist = pygame.Surface((300, 40), pygame.SRCALPHA)
             pygame.draw.ellipse(s_mist, (255, 255, 255, 30), (0,0,300,40))
             surface.blit(s_mist, (mx, ground_top - 20 + i*5))

        # Sparkles on ground
        t_spark = pygame.time.get_ticks() / 50
        random.seed(int(t_spark // 10)) # Twinkle every few frames
        for _ in range(10):
            sx = random.randint(0, width)
            sy = random.randint(ground_top, height)
            pygame.draw.rect(surface, (255, 255, 255), (sx, sy, 2, 2))

    elif biome == "VOLCANO":
        # 1. Hellscape Sky
        draw_gradient(surface, (40, 0, 0), (80, 10, 0), pygame.Rect(0, 0, width, height))
        
        # Dark Smoke Overlay
        s_smoke = pygame.Surface((width, height), pygame.SRCALPHA)
        t_smoke = pygame.time.get_ticks() / 1000
        for i in range(10):
            cx = (t_smoke * 20 + i * 200) % (width+300) - 150
            cy = 50 + math.sin(t_smoke + i) * 30
            pygame.draw.circle(s_smoke, (20, 20, 20, 80), (cx, cy), 100)
        surface.blit(s_smoke, (0,0))

        
        # 2. Mega Volcano (Static Base)
        v_x = width // 2
        v_top_y = height - 450
        pygame.draw.polygon(surface, (20, 5, 5), [
            (v_x - 500, height), (v_x + 500, height), (v_x, v_top_y)
        ])
        
        # 3. Active Lava Eruption logic
        t = pygame.time.get_ticks()
        
        # Lava down the side (Animated Texture)
        # We simulate flow by shifting a pattern
        flow_offset = (t / 50) % 20
        # Draw a triangle strip for lava
        lava_poly = [
            (v_x, v_top_y), 
            (v_x - 100, height), 
            (v_x + 100, height)
        ]
        pygame.draw.polygon(surface, (200, 50, 0), lava_poly)
        # Add flowing "veins"
        for i in range(10):
            ly = v_top_y + i * 40 + flow_offset
            if ly < height:
                pygame.draw.line(surface, (255, 100, 0), (v_x, v_top_y), (v_x + (i%2*20-10), ly), 3)

        # 4. VOLCANIC BOMBS (Rocks shooting out)
        # Spawning mechanism based on time
        # We track 5 "rocks" looping phases
        for i in range(5):
            # Each rock has a cycle of, say, 2000ms. Staggered by i.
            cycle_dur = 2000
            local_t = (t + i * 400) % cycle_dur
            
            if local_t < 1500: # Active flight duration
                # Progress 0.0 to 1.0
                prog = local_t / 1500.0
                
                # Parabolic arc
                # Start: v_x, v_top_y
                # End: random ground spot? Let's make them fly left/right
                spread = 300 * (-1 if i % 2 == 0 else 1)
                
                curr_x = v_x + spread * prog
                # Height: Arc up then down. h = -4 * (x - 0.5)^2 + 1  (normalized)
                # Simple gravity: y = start_y + vy * t + 0.5 * g * t^2
                # Let's use simple math
                arc_h = 200 * math.sin(prog * 3.14159) # Peak at 0.5
                curr_y = v_top_y - arc_h + (prog * 450) # Net drop down to ground
                
                # Draw Rock
                pygame.draw.circle(surface, (50, 40, 40), (int(curr_x), int(curr_y)), 6)
                pygame.draw.circle(surface, (255, 100, 0), (int(curr_x)+2, int(curr_y)+2), 2) # Magma core
                
                # Trail
                if prog < 0.8:
                    pygame.draw.circle(surface, (100, 50, 50), (int(curr_x), int(curr_y)+10), 4)

        # 5. Ground (Cracked)
        ground_top = height - 80
        pygame.draw.rect(surface, (40, 20, 20), (0, ground_top, width, 80))
        
        # Lava River in Foreground
        lava_y = ground_top + 40
        pygame.draw.rect(surface, (255, 60, 0), (0, lava_y, width, 30))
        
        # Bubbles & Heat
        for _ in range(15):
            bx = random.randint(0, width)
            pygame.draw.circle(surface, (255, 220, 0), (bx, lava_y + random.randint(0, 30)), 3)

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
    """Draws a GOD-TIER fractal lightning bolt with core, glow, and impact."""
    
    # 1. Main Bolt Logic
    def recursive_bolt(start, end, depth, displace, width_scale):
        if depth == 0:
            # Draw GLOW (Thick, colored, low alpha)
            # Since we can't do direct alpha lines easily on main surf, we iterate
            for w in range(width_scale + 4, width_scale, -1):
                col = (100, 100, 255) # Blue-ish
                pygame.draw.line(surface, col, start, end, w)
            
            # Draw CORE (Thin, White)
            pygame.draw.line(surface, (255, 255, 255), start, end, max(1, width_scale-2))
            return

        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        
        # Perpendicular vector
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        px, py = -dy, dx
        L = math.hypot(px, py)
        if L > 0: px/=L; py/=L
            
        offset = (random.random() - 0.5) * displace
        mid = (mid_x + px*offset, mid_y + py*offset)
        
        recursive_bolt(start, mid, depth-1, displace/2, width_scale)
        recursive_bolt(mid, end, depth-1, displace/2, width_scale)
        
        # Branches
        if depth > 2 and random.random() < 0.3:
             angle = random.uniform(0, 6.28)
             length = displace * 0.7
             bx = mid[0] + math.cos(angle) * length
             by = mid[1] + math.sin(angle) * length
             # Draw branch (thinner)
             recursive_bolt(mid, (bx, by), depth-1, displace/2, max(1, width_scale-2))

    # Draw Main Bolt
    recursive_bolt(start_pos, end_pos, 6, 80, 5)
    
    # 2. Impact Effect at end_pos
    # "Sparks"
    for _ in range(10):
        ix = end_pos[0] + random.randint(-20, 20)
        iy = end_pos[1] + random.randint(-20, 20)
        pygame.draw.line(surface, (200, 200, 255), end_pos, (ix, iy), 2)
    
    # Impact Flash circle
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(s, (200, 200, 255, 100), (50, 50), 30)
    pygame.draw.circle(s, (255, 255, 255, 200), (50, 50), 10)
    surface.blit(s, (end_pos[0]-50, end_pos[1]-50))
    
    # Global Flash
    if random.random() < 0.2:
        s_flash = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        s_flash.fill((200, 200, 255, 40))
        surface.blit(s_flash, (0,0))

def draw_tornado_effect(surface, x, y, life_counter):
    """Draws a PROFESSIONAL, 3D-Volumetric Tornado with helix particles and debris."""
    
    t = pygame.time.get_ticks() / 150 # Slower, more majestic speed
    
    # Tornado Parameters
    height = 280
    top_width = 160
    base_width = 20
    
    # 1. DUST CLOUD BASE
    # Draw spinning dust puff balls at the bottom
    for i in range(10):
        angle = (t * 2 + i * 0.6) 
        dx = x + math.cos(angle) * (i * 4 + 10)
        dy = y - 10 + math.sin(angle) * 5
        s_dust = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(s_dust, (100, 90, 80, 100), (0,0,40,20))
        surface.blit(s_dust, (dx-20, dy-10))

    # 2. FUNNEL BODY (Stacked animated rings + vertical fade)
    # We use many thin ellipses to create a smooth 3D cone
    segments = 40
    for i in range(segments):
        prog = i / segments # 0 (bottom) to 1 (top)
        
        # Calculate width at this height (non-linear for curve)
        current_w = base_width + (top_width - base_width) * (prog**1.5)
        
        # Sine wave wobble for "wind" feel
        wobble_x = math.sin(t + i*0.2) * (10 * prog) 
        
        rect_x = x - current_w//2 + wobble_x
        rect_y = y - (prog * height) - 20
        
        # Color Gradient: Dark Brown (Base) -> Light Grey/White (Top)
        # RGB interpolation
        c_bot = (80, 70, 60)
        c_top = (220, 220, 230)
        r = int(c_bot[0] + (c_top[0]-c_bot[0])*prog)
        g = int(c_bot[1] + (c_top[1]-c_bot[1])*prog)
        b = int(c_bot[2] + (c_top[2]-c_bot[2])*prog)
        
        # Alpha is higher at edges to simulate volume? 
        # Actually simpler: Solid-ish core, transparent edges.
        # Let's draw composed ellipses.
        
        # Back Ring (darker)
        s_ring = pygame.Surface((int(current_w)+20, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(s_ring, (r-20, g-20, b-20, 150), (10, 0, current_w, 8+prog*10))
        surface.blit(s_ring, (rect_x-10, rect_y))
        
        # Front Helix Streak (A particle orbiting)
        # Orbit phase
        orbit_ang = t * (5 - prog*2) + i * 0.5 # Faster at bottom?
        ox = math.cos(orbit_ang) * (current_w * 0.4)
        
        # Draw "wind streak"
        if math.sin(orbit_ang) > 0: # Front side only?
             pygame.draw.line(surface, (255, 255, 255, 180), (x + wobble_x + ox, rect_y+5), (x + wobble_x + ox - 10, rect_y+7), 2)

    # 3. DEBRIS (Flying chunks)
    random.seed(int(t)) # Jittery debris? or consistent?
    # Actually let's use consistent orbits based on time
    for i in range(12):
        # Each piece has a height and orbit radius
        d_prog = ((t*0.2 + i*0.1) % 1.0) # Moves up continuously
        d_h = d_prog * height
        d_w = base_width + (top_width - base_width) * (d_prog**1.5)
        
        d_angle = t * 6 + i * 20
        d_x = x + math.cos(d_angle) * (d_w * 0.6)
        d_y = y - d_h - 20
        
        # Z-sorting-ish: if behind, draw darker/smaller
        is_front = math.sin(d_angle) > 0
        
        if is_front:
             pygame.draw.rect(surface, (60, 50, 40), (d_x, d_y, 6, 6))
             pygame.draw.rect(surface, (0, 0, 0), (d_x, d_y, 6, 6), 1)
        else:
             # Behind (dimmer)
             s_deb = pygame.Surface((6,6), pygame.SRCALPHA)
             pygame.draw.rect(s_deb, (40, 30, 20, 150), (0,0,6,6))
             surface.blit(s_deb, (d_x, d_y))

def draw_dragon_effect(surface, x, y, life_counter):
    """EPIC HYPER-REALISTIC DRAGON BREATH."""
    
    t = pygame.time.get_ticks()
    
    # 1. Screen Shake & Darken
    shake_x = random.randint(-5, 5)
    shake_y = random.randint(-5, 5)
    
    s_dark = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    s_dark.fill((0, 0, 0, 150)) # Darker
    surface.blit(s_dark, (0,0))
    
    # 2. Dragon Head (Massive, jagged)
    head_y = 60 + math.sin(t/200)*20 + shake_y
    head_x = x + shake_x
    
    # Silhouette (Spiky)
    pygame.draw.polygon(surface, (30, 0, 0), [
        (head_x - 100, head_y - 150),
        (head_x + 100, head_y - 150),
        (head_x + 180, head_y - 250), # Horn R
        (head_x + 120, head_y - 50),
        (head_x + 60, head_y + 50), # Jaw R
        (head_x, head_y + 80), # Chin
        (head_x - 60, head_y + 50), # Jaw L
        (head_x - 120, head_y - 50),
        (head_x - 180, head_y - 250), # Horn L
    ])
    
    # Eyes (Fierce Glowing)
    pygame.draw.ellipse(surface, (255, 50, 0), (head_x - 70, head_y - 50, 40, 60))
    pygame.draw.ellipse(surface, (255, 50, 0), (head_x + 30, head_y - 50, 40, 60))
    # Vertical pupil
    pygame.draw.rect(surface, (0,0,0), (head_x - 55, head_y - 45, 10, 50))
    pygame.draw.rect(surface, (0,0,0), (head_x + 45, head_y - 45, 10, 50))
    
    # 3. FIRE STREAM (Volumetric Particles)
    # We spawn MANY circles with additive blending-ish feel
    fire_start_y = head_y + 60
    
    # Stream Logic:
    # Multiple "jets" of fire
    for i in range(150):
        # Progress down screen
        prog = i / 150.0
        
        # Sine wave wiggles
        wiggle = math.sin(t/50 + i/10) * (50 * prog)
        stream_x = head_x + wiggle + random.randint(-20, 20)
        stream_y = fire_start_y + i * 8
        
        if stream_y > SCREEN_HEIGHT: break
        
        # Width expands
        width = 40 + (prog * 600)
        
        # Random pos within width
        px = stream_x + random.randint(-int(width/2), int(width/2))
        
        # Color Gradient: White (hot) -> Yellow -> Orange -> Red -> Black (smoke)
        if prog < 0.1: col = (255, 255, 255)
        elif prog < 0.3: col = (255, 255, 0)
        elif prog < 0.6: col = (255, 100, 0)
        else: col = (150, 50, 0)
        
        # Vary alpha
        alpha = random.randint(50, 150)
        
        # Size grows
        size = int(10 + prog * 80)
        
        # Draw particle
        s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*col, alpha), (size, size), size)
        surface.blit(s, (px - size, stream_y - size))
        
    # 4. Embers / Sparks floating up
    for _ in range(20):
        ex = random.randint(0, SCREEN_WIDTH)
        ey = random.randint(0, SCREEN_HEIGHT)
        pygame.draw.rect(surface, (255, 200, 100), (ex, ey, 3, 3))

