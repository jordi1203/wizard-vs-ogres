
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

def draw_ogre(surface, x, y, facing_right, scale=1.0):
    """Draws a Green Ogre."""
    _draw_monster_base(surface, x, y, facing_right, scale, 
                       skin_color=(100, 140, 60), 
                       outfit_color=(139, 69, 19), 
                       weapon="CLUB")

def draw_goblin(surface, x, y, facing_right, scale=0.8):
    """Draws a small, fast Goblin."""
    _draw_monster_base(surface, x, y, facing_right, scale, 
                       skin_color=(150, 200, 50), 
                       outfit_color=(100, 50, 50), 
                       weapon="DAGGER",
                       is_goblin=True)

def draw_troll(surface, x, y, facing_right, scale=1.3):
    """Draws a large, regenerating Troll."""
    _draw_monster_base(surface, x, y, facing_right, scale, 
                       skin_color=(100, 100, 120), 
                       outfit_color=(50, 50, 50), 
                       weapon="ROCK")

def _draw_monster_base(surface, x, y, facing_right, scale, skin_color, outfit_color, weapon, is_goblin=False):
    direction = 1 if facing_right else -1
    
    # Virtual Surface
    w, h = 140, 140
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    
    cx, cy = w//2, h
    
    # --- Body ---
    # Legs (Thicker for Ogres)
    leg_w = 15 if not is_goblin else 12
    pygame.draw.rect(s, outfit_color, (cx - 15, cy - 35, leg_w, 35))
    pygame.draw.rect(s, outfit_color, (cx + 5, cy - 35, leg_w, 35))
    
    # Torso (Muscular)
    body_h = 50 if not is_goblin else 30
    body_w = 50 if not is_goblin else 40
    pygame.draw.rect(s, skin_color, (cx - 25, cy - 35 - body_h, body_w, body_h), border_radius=8)
    
    # Armor/Vest (Jagged)
    pygame.draw.polygon(s, outfit_color, [
        (cx - 25, cy - 35 - body_h), 
        (cx + 25, cy - 35 - body_h), 
        (cx + 15, cy - 35 - body_h + 20),
        (cx, cy - 35 - body_h + 30),
        (cx - 15, cy - 35 - body_h + 20)
    ])
    
    # Shoulder Pads (Ogre Only)
    if not is_goblin:
        pygame.draw.circle(s, (80, 80, 80), (cx - 25, cy - 35 - body_h + 5), 12)
        pygame.draw.circle(s, (80, 80, 80), (cx + 25, cy - 35 - body_h + 5), 12)
        # Spikes on shoulder
        pygame.draw.line(s, (200, 200, 200), (cx - 25, cy - 35 - body_h), (cx - 35, cy - 35 - body_h - 10), 3)
        pygame.draw.line(s, (200, 200, 200), (cx + 25, cy - 35 - body_h), (cx + 35, cy - 35 - body_h - 10), 3)
    
    # Head
    head_y = cy - 35 - body_h - 18
    head_r = 20 if not is_goblin else 14
    pygame.draw.circle(s, skin_color, (cx, head_y), head_r)
    
    # Details Ogre/Troll
    if not is_goblin:
        # War Paint (Red markings)
        pygame.draw.line(s, (150, 0, 0), (cx-10, head_y-10), (cx-5, head_y+5), 3)
        pygame.draw.line(s, (150, 0, 0), (cx+10, head_y-10), (cx+5, head_y+5), 3)
        
        # Jaw/Teeth (Underbit)
        pygame.draw.rect(s, (255, 255, 200), (cx - 8, head_y + 10, 4, 8)) # Left Tusk
        pygame.draw.rect(s, (255, 255, 200), (cx + 4, head_y + 10, 4, 8)) # Right Tusk

    # Ears (Pointy & Large)
    ear_len = 15
    ear_l = [(cx - head_r + 5, head_y), (cx - head_r - ear_len, head_y - 10), (cx - head_r, head_y - 10)]
    ear_r = [(cx + head_r - 5, head_y), (cx + head_r + ear_len, head_y - 10), (cx + head_r, head_y - 10)]
    pygame.draw.polygon(s, skin_color, ear_l)
    pygame.draw.polygon(s, skin_color, ear_r)
    
    # Face
    eye_x = cx + (8 * direction)
    # Glowing Eyes
    pygame.draw.circle(s, (255, 50, 0), (eye_x, head_y - 5), 4)
    pygame.draw.circle(s, (255, 200, 0), (eye_x, head_y - 5), 1) # Pupil
    
    # Mouth (Angry line)
    pygame.draw.line(s, (20, 0, 0), (cx - 5, head_y + 8), (cx + 5 + 5*direction, head_y + 8), 3)
    
    # --- Weapon ---
    hand_x = cx + (30 * direction)
    hand_y = cy - 60
    # Arm (Thick muscular)
    pygame.draw.line(s, skin_color, (cx + 20*direction, cy - 60), (hand_x, hand_y), 8)
    
    if weapon == "CLUB":
        # Massive Spiked Club
        end_x = hand_x + (20 * direction)
        end_y = hand_y - 50
        # Handle
        pygame.draw.line(s, (100, 80, 60), (hand_x, hand_y), (end_x, end_y), 6)
        # Head (Big blobb)
        pygame.draw.circle(s, (80, 60, 40), (end_x, end_y), 18)
        # Spikes
        pygame.draw.line(s, (200, 200, 200), (end_x-10, end_y), (end_x-18, end_y), 2)
        pygame.draw.line(s, (200, 200, 200), (end_x+10, end_y), (end_x+18, end_y), 2)
        pygame.draw.line(s, (200, 200, 200), (end_x, end_y-10), (end_x, end_y-18), 2)
        
    elif weapon == "DAGGER":
        end_x = hand_x + (15 * direction) 
        end_y = hand_y - 15
        pygame.draw.line(s, (150, 150, 150), (hand_x, hand_y), (end_x, end_y), 4) # Blade
        pygame.draw.line(s, (100, 50, 0), (hand_x, hand_y), (hand_x+5*direction, hand_y+5), 2) # Hilt
        
    elif weapon == "ROCK":
        pygame.draw.circle(s, (80, 80, 80), (hand_x, hand_y - 10), 18)
        pygame.draw.circle(s, (60, 60, 60), (hand_x-5, hand_y - 12), 5) # Texture

    # Scale & Blit
    if scale != 1.0:
        s = pygame.transform.scale(s, (int(w*scale), int(h*scale)))
    
    surface.blit(s, s.get_rect(midbottom=(x, y)))

def draw_projectile(surface, x, y, color=WHITE, is_multishot=False):
    """Draws a glowing orb with a magical trail if upgraded."""
    
    # Trail Effect
    if is_multishot: # If multishot is active (or just always for style)
        for i in range(5):
            tx = x - (i*5) # Simple trail behind
            ty = y + random.randint(-2, 2)
            alpha = 150 - (i*30)
            if alpha > 0:
                s = pygame.Surface((10, 10), pygame.SRCALPHA)
                pygame.draw.circle(s, (*color[:3], alpha), (5, 5), 3)
                surface.blit(s, (tx, ty))

    # Core Glow
    r, g, b = color[:3]
    for radius, alpha in [(12, 100), (8, 200), (4, 255)]:
        s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (r, g, b, alpha), (radius, radius), radius)
        surface.blit(s, (x - radius, y - radius))
        
    # Bright center
    pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), 2)

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

