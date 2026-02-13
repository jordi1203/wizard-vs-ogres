
import pygame
import sys
import random
import math
from src.config import *
from src.assets import *
from src.entities import Wizard, Enemy, Projectile, EnemyProjectile

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wizard vs Ogres: Ultimate Edition")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 36, bold=True)
small_font = pygame.font.SysFont("Arial", 24)
card_font = pygame.font.SysFont("Arial", 20, bold=True)
shop_font = pygame.font.SysFont("Arial", 28, bold=True)

# Game State
# MENU, PLAYING, SHOP, CARD_SELECT, GAME_OVER, VICTORY
game_state = "MENU"
current_biome = "FOREST"
current_wave = 1
enemies_killed_in_wave = 0
total_enemies_spawned_in_wave = 0
score = 0

# Entity Groups
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()

# Player
wizard = Wizard(100, SCREEN_HEIGHT - 50)
all_sprites.add(wizard)

# Particles & Effects
particles = []
active_effects = [] # For Tornado, Dragon visuals

# Global Store for resetting logic
# We persist coins across runs? No, usually roguelike resets. 
# But user said "Menu inicial... tienda... monedas".
# Maybe consistent progression or just within the run?
# Let's assume persistent for this session, but reset on full restart?
# Actually "Menu inicial" implies a main menu before starting.
# Let's make coins persist in memory (session) but skills reset?
# Or roguelite style: coins are collected in run, then shop is accessible?
# User phrasing: "menu inicial, donde haya un menu para la tienda".
# So: Main Menu -> Shop (buy perma upgrades?) -> Play.
# Or: Play -> Get Coins -> Die/Win -> Main Menu -> Shop.
# Let's go with: Coins are persistent globally. Skills bought are permanent for the user profile.

TOTAL_COINS = 999999
UNLOCKED_ABILITIES = { 
    "LIGHTNING": False, "TORNADO": False, "DRAGON": False,
    "ARCANE_VOLLEY": False, "VOID_LANCE": False, "FIRE_RING": False
}
SHOP_UPGRADES_STATE = {} # Key: ID, Value: Level
shop_scroll_y = 0
shop_return_target = "MENU" # Tracks where to go after closing shop
gray = (100, 100, 100) # Defined gray here used in draw_shop

def save_data():
    pass # In real app, save to file

def load_data():
    pass

# --- VISUAL EFFECTS ---
# (Effects are now imported from src.assets)

def cast_lightning():
    # Chain Lightning: Zap closest, then zap from that to next closest
    if not enemies: return
    
    # Find up to 3 targets
    targets = []
    
    # 1. Closest to Wizard
    sorted_enemies = sorted(enemies, key=lambda e: math.hypot(e.rect.centerx - wizard.rect.centerx, e.rect.centery - wizard.rect.centery))
    if sorted_enemies:
        t1 = sorted_enemies[0]
        if math.hypot(t1.rect.centerx - wizard.rect.centerx, t1.rect.centery - wizard.rect.centery) < 700:
            targets.append(t1)
            
            # 2. Closest to T1 (excluding T1)
            others = [e for e in enemies if e != t1]
            if others:
                t2 = min(others, key=lambda e: math.hypot(e.rect.centerx - t1.rect.centerx, e.rect.centery - t1.rect.centery))
                if math.hypot(t2.rect.centerx - t1.rect.centerx, t2.rect.centery - t1.rect.centery) < 400:
                    targets.append(t2)
                    
                    # 3. Closest to T2
                    others2 = [e for e in others if e != t2]
                    if others2:
                        t3 = min(others2, key=lambda e: math.hypot(e.rect.centerx - t2.rect.centerx, t2.rect.centery - t2.rect.centery))
                        if math.hypot(t3.rect.centerx - t2.rect.centerx, t3.rect.centery - t2.rect.centery) < 400:
                            targets.append(t3)

    # Apply Damage & Visuals
    prev_pos = wizard.rect.center
    for t in targets:
        t.health -= 5 # High damage
        
        # Visual Bolt from prev to current
        active_effects.append({
            "type": "LIGHTNING", 
            "start": prev_pos, 
            "end": t.rect.center, 
            "life": 15
        })
        prev_pos = t.rect.center
        
        if t.health <= 0:
            kill_enemy(t)

def cast_tornado():
    # Spawn 2 localized tornado objects that move outward
    # We need to track them in active_effects and handle collision logic THERE,
    # because they need to move over time.
    
    # Left Tornado
    active_effects.append({
        "type": "TORNADO_MOVING", 
        "x": wizard.rect.centerx - 50, 
        "y": wizard.rect.centery, 
        "life": 100, 
        "dir": -1
    })
    # Right Tornado
    active_effects.append({
        "type": "TORNADO_MOVING", 
        "x": wizard.rect.centerx + 50, 
        "y": wizard.rect.centery, 
        "life": 100, 
        "dir": 1
    })

def cast_dragon():
    # Kill all enemies on screen
    for e in enemies:
        e.health = 0
        kill_enemy(e)
    
    # Visual
    active_effects.append({"type": "DRAGON", "x": SCREEN_WIDTH//2, "y": SCREEN_HEIGHT//2, "life": 120})

def kill_enemy(enemy):
    global score, enemies_killed_in_wave, TOTAL_COINS
    if not enemy.alive(): return # Already dead
    
    enemy.kill()
    enemies_killed_in_wave += 1
    score += 10 * current_wave
    
    # Coins
    is_boss = enemy.rect.width > 100
    coin_val = BOSS_COIN_VALUE if is_boss else COIN_VALUE
    TOTAL_COINS += coin_val
    
    # Particles
    for _ in range(15):
        particles.append({
            'x': enemy.rect.centerx + random.randint(-15, 15),
            'y': enemy.rect.centery + random.randint(-15, 15),
            'life': 30, 'max_life': 30, 'size': random.randint(3, 8), 'color': (0, 255, 0)
        })

# --- UI STATES ---

def draw_menu(surface):
    # 1. Background & Atmosphere
    # Fill specific sky color first to prevent black voids if assets fail
    surface.fill((20, 10, 30))
    draw_background_scenery(surface, "FOREST", SCREEN_WIDTH, SCREEN_HEIGHT)
    
    ground_y = SCREEN_HEIGHT - 80
    
    # Subtle Overlay (just to unify colors, not hide them)
    s_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    s_overlay.fill((10, 20, 30, 80)) # Blue-ish tint, low alpha
    surface.blit(s_overlay, (0,0))

    cx = SCREEN_WIDTH // 2
    cy = SCREEN_HEIGHT // 2
    
    # 2. Hero Character (The Wizard) - LEFT SIDE
    # Position him at ~25% width
    wiz_x = int(SCREEN_WIDTH * 0.3)
    wiz_y = ground_y - 20
    draw_scaled_wizard(surface, wiz_x, wiz_y, scale=3.0)
    
    # Magical Particles around Wizard
    t = pygame.time.get_ticks()
    random.seed(t // 50) 
    for _ in range(8):
        sx = wiz_x + random.randint(-100, 100)
        sy = wiz_y - 200 - random.randint(0, 300)
        alpha = random.randint(150, 255)
        radius = random.randint(2, 4)
        if random.random() < 0.2: radius += 2 # Occasional big spark
        
        s_part = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s_part, (255, 230, 150, alpha), (radius, radius), radius)
        surface.blit(s_part, (sx, sy))
    
    # 3. UI Section - RIGHT SIDE
    ui_center_x = int(SCREEN_WIDTH * 0.7)
    
    # Epic Title
    title_text = "WIZARD vs OGRES"
    # Use a nice bold font
    title_font = pygame.font.SysFont("Verdana", 60, bold=True)
    
    # Shadow
    shad = title_font.render(title_text, True, (0, 0, 0))
    shad_rect = shad.get_rect(center=(ui_center_x + 4, 104))
    surface.blit(shad, shad_rect)
    
    # Main Title
    tit = title_font.render(title_text, True, (255, 200, 50)) 
    tit_rect = tit.get_rect(center=(ui_center_x, 100))
    surface.blit(tit, tit_rect)
    
    sub_font = pygame.font.SysFont("Arial", 24, italic=True)
    sub = sub_font.render("- ENCHANTED FOREST EDITION -", True, (150, 220, 255))
    surface.blit(sub, sub.get_rect(center=(ui_center_x, 150)))

    # 4. Menu Options (Right Side)
    mouse_pos = pygame.mouse.get_pos()
    menu_opts = [
        {"text": "PLAY GAME", "key": "ENTER", "action": "START"},
        {"text": "ITEM SHOP", "key": "S", "action": "SHOP"},
        {"text": "EXIT", "key": "Q", "action": "QUIT"}
    ]
    
    start_y = 250
    btn_w, btn_h = 280, 55
    spacing = 15
    
    for i, opt in enumerate(menu_opts):
        btn_y = start_y + i * (btn_h + spacing)
        rect = pygame.Rect(ui_center_x - btn_w//2, btn_y, btn_w, btn_h)
        
        is_hover = rect.collidepoint(mouse_pos)
        
        # Style
        # Glass morphism style
        bg_col = (10, 10, 20, 180) if not is_hover else (50, 50, 90, 220)
        border_col = (100, 100, 150) if not is_hover else (255, 220, 100)
        
        # Draw Button Box
        s_btn = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        pygame.draw.rect(s_btn, bg_col, (0,0,btn_w,btn_h), border_radius=12)
        pygame.draw.rect(s_btn, border_col, (0,0,btn_w,btn_h), 2, border_radius=12)
        surface.blit(s_btn, rect)
        
        # Text
        txt_col = (220, 220, 220) if not is_hover else (255, 255, 255)
        mtxt = shop_font.render(opt["text"], True, txt_col)
        surface.blit(mtxt, mtxt.get_rect(center=rect.center))
        
        hint = small_font.render(f"[{opt['key']}]", True, (120, 120, 120))
        surface.blit(hint, (rect.right + 10, rect.centery - 10))

    # 5. Bottom Stats Bar
    bar_y = SCREEN_HEIGHT - 40
    pygame.draw.rect(surface, (0,0,0,150), (0, bar_y, SCREEN_WIDTH, 40))
    
    c_txt = small_font.render(f"GOLD: {TOTAL_COINS}", True, GOLD)
    surface.blit(c_txt, (20, bar_y + 8))
    
    ver = small_font.render("v2.2 (Forest)", True, GRAY)
    surface.blit(ver, (SCREEN_WIDTH - 120, bar_y + 8))

def draw_shop(surface):
    global TOTAL_COINS
    surface.fill((20, 20, 30))
    
    title = font.render("MAGIC SHOP", True, MAGENTA)
    coins_txt = font.render(f"Your Coins: {TOTAL_COINS}", True, GOLD)
    
    exit_label = "Press [ESC] to Return"
    if shop_return_target == "PLAYING":
        exit_label = "Press [ENTER] to Start Next Wave"
    
    exit_txt = small_font.render(exit_label, True, WHITE)
    
    # Header Overlay (to cover scrolled items)
    pygame.draw.rect(surface, (20, 20, 30), (0, 0, SCREEN_WIDTH, 130))
    surface.blit(title, (50, 50))
    surface.blit(coins_txt, (50, 100))
    surface.blit(exit_txt, (50, SCREEN_HEIGHT - 50))
    
    items = [
        {"id": "LIGHTNING", "name": "Lightning Strike (Auto)", "cost": COST_LIGHTNING, "desc": "Zaps closest enemy periodically."},
        {"id": "TORNADO", "name": "Wind Blast (Key: T)", "cost": COST_TORNADO, "desc": "Push enemies back with 'T'."},
        {"id": "DRAGON", "name": "Dragon Summon (Key: R)", "cost": COST_DRAGON, "desc": "Summon Dragon to clear screen."},
        {"id": "ARCANE_VOLLEY", "name": "Arcane Volley (Key: 2)", "cost": COST_ARCANE_VOLLEY, "desc": "Fires 5 unstable magic orbs."},
        {"id": "VOID_LANCE", "name": "Void Lance (Key: 3)", "cost": COST_VOID_LANCE, "desc": "Piercing beam of dark energy."},
        {"id": "FIRE_RING", "name": "Inferno Ring (Key: 4)", "cost": COST_FIRE_RING, "desc": "Massive ring of fire destruction."}
    ]
    
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    
    start_y = 200
    for i, item in enumerate(items):
        y = start_y + i * 120 + shop_scroll_y
        rect = pygame.Rect(50, y, 800, 100)
        
        is_owned = UNLOCKED_ABILITIES[item["id"]]
        color = (50, 50, 50)
        if is_owned: 
            color = (30, 80, 30) # Owned
        elif rect.collidepoint(mouse_pos) and (y > 100 and y < SCREEN_HEIGHT - 60):
             if TOTAL_COINS >= item["cost"]:
                color = (80, 80, 80) # Affordable Highlight
                if click:
                    TOTAL_COINS -= item["cost"]
                    UNLOCKED_ABILITIES[item["id"]] = True
                    # Immediate unlock if playing
                    if item["id"] in ["ARCANE_VOLLEY", "VOID_LANCE", "FIRE_RING"] and item["id"] not in wizard.unlocked_weapons:
                        wizard.unlocked_weapons.append(item["id"])
                    pygame.time.wait(200)
        
        pygame.draw.rect(surface, color, rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, rect, 2, border_radius=10)
        
        name_s = shop_font.render(f"{item['name']}", True, CYAN if is_owned else WHITE)
        cost_s = shop_font.render("OWNED" if is_owned else f"{item['cost']} G", True, GOLD)
        desc_s = small_font.render(item['desc'], True, GRAY)
        
        surface.blit(name_s, (70, y + 20))
        surface.blit(cost_s, (700, y + 35))
        surface.blit(desc_s, (70, y + 60))
        
    # --- Permanent Upgrades Section ---
    section_y_base = start_y + len(items) * 120 + 20
    sect_title = shop_font.render("PERMANENT UPGRADES", True, ORANGE)
    surface.blit(sect_title, (50, section_y_base + shop_scroll_y))
    
    start_y_upg = section_y_base + 50
    for i, item in enumerate(SHOP_UPGRADES_LIST):
        y = start_y_upg + i * 120 + shop_scroll_y
        rect = pygame.Rect(50, y, 800, 100)
        
        lvl = SHOP_UPGRADES_STATE.get(item["id"], 0)
        cost = item["cost"] * (lvl + 1)
        
        color = (50, 50, 60)
        if rect.collidepoint(mouse_pos) and (y > 100 and y < SCREEN_HEIGHT - 60):
             if TOTAL_COINS >= cost:
                color = (70, 70, 90) # Affordable
                if click:
                    TOTAL_COINS -= cost
                    SHOP_UPGRADES_STATE[item["id"]] = lvl + 1
                    pygame.time.wait(200)
    
        pygame.draw.rect(surface, color, rect, border_radius=10)
        pygame.draw.rect(surface, (100, 100, 255), rect, 2, border_radius=10)
        
        name_s = shop_font.render(f"{item['name']} (Lvl {lvl})", True, WHITE)
        cost_s = shop_font.render(f"{cost} G", True, GOLD)
        desc_s = small_font.render(item['desc'], True, GRAY)
        
        surface.blit(name_s, (70, y + 20))
        surface.blit(cost_s, (700, y + 35))
        surface.blit(desc_s, (70, y + 60))
        
    # Scrollbar indicator (simple)
    total_h = section_y_base + 50 + len(SHOP_UPGRADES_LIST) * 120
    if total_h > SCREEN_HEIGHT:
        bar_h = (SCREEN_HEIGHT / total_h) * SCREEN_HEIGHT
        bar_y = (-shop_scroll_y / total_h) * SCREEN_HEIGHT
        pygame.draw.rect(surface, (100, 100, 100), (SCREEN_WIDTH - 10, bar_y, 10, bar_h))

    # Header Overlay (to cover scrolled items)
    pygame.draw.rect(surface, (20, 20, 30), (0, 0, SCREEN_WIDTH, 130))
    surface.blit(title, (50, 50))
    surface.blit(coins_txt, (50, 100))
    # surface.blit(exit_txt, (50, SCREEN_HEIGHT - 50)) # Draw exit text on top of everything? No, footer better.
    
    # Footer Overlay
    pygame.draw.rect(surface, (20, 20, 30), (0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60))
    surface.blit(exit_txt, (50, SCREEN_HEIGHT - 50))

# --- GAME LOGIC HELPERS ---

def reset_run():
    global score, current_wave, enemies_killed_in_wave, total_enemies_spawned_in_wave
    global current_biome, game_state, particles
    global enemies, projectiles, enemy_projectiles, active_effects, spawn_timer
    
    score = 0
    current_wave = 1
    enemies_killed_in_wave = 0
    total_enemies_spawned_in_wave = 0
    current_biome = "FOREST"
    
    enemies.empty()
    projectiles.empty()
    enemy_projectiles.empty()
    all_sprites.empty()
    particles.clear()
    active_effects.clear()
    spawn_timer = 0
    
    wizard.__init__(100, SCREEN_HEIGHT - 50) # Reset hp/stats
    # Reset upgrade levels
    wizard.upgrade_levels = {
            "SPEED": 0,
            "DAMAGE": 0,
            "MULTISHOT": 0,
            "PIERCING": 0,
            "HEALTH": 0
    }
    
    # Apply bought upgrades (Abilities)
    wizard.abilities = UNLOCKED_ABILITIES.copy()
    
    # Populate unlocked weapons
    wizard.unlocked_weapons = ["DEFAULT"]
    if UNLOCKED_ABILITIES["ARCANE_VOLLEY"]: wizard.unlocked_weapons.append("ARCANE_VOLLEY")
    if UNLOCKED_ABILITIES["VOID_LANCE"]: wizard.unlocked_weapons.append("VOID_LANCE")
    if UNLOCKED_ABILITIES["FIRE_RING"]: wizard.unlocked_weapons.append("FIRE_RING")
    
    # Apply Permanent Stats from Shop
    # {"id": "PERMA_DMG", "val": 0.1, "stat": "damage_multiplier"}
    for upg in SHOP_UPGRADES_LIST:
        lvl = SHOP_UPGRADES_STATE.get(upg["id"], 0)
        if lvl > 0:
            if upg["stat"] == "damage_multiplier":
                wizard.damage_multiplier += (upg["val"] * lvl)
            elif upg["stat"] == "max_health":
                wizard.max_health += (upg["val"] * lvl)
                wizard.health = wizard.max_health
            elif upg["stat"] == "attack_speed_boost":
                wizard.attack_speed_boost += (upg["val"] * lvl)
    
    all_sprites.add(wizard)
    game_state = "PLAYING"

def spawn_enemy_logic():
    global enemies, particles, projectiles, enemy_projectiles, active_effects, score, current_wave, spawn_timer, wizard, enemies_killed_in_wave
    
    # BOSS WAVE LOGIC
    if current_wave % 10 == 0:
        # Spawn Boss ONCE per wave
        # We need a flag to check if boss spawned.
        # Simplest way: Check if we have spawned it yet.
        # But spawn_enemy_logic is called repeatedly.
        # We can check if `enemies_killed_in_wave == 0` and len(enemies) == 0.
        # Or better: Just spawn boss and regular minions?
        # Let's say Boss Wave = ONLY Boss + occasional minions?
        
        # Check if Boss exists
        boss_exists = False
        for e in enemies:
            if e.enemy_type == "OGRE_KING": 
                boss_exists = True
                break
        
        if not boss_exists and enemies_killed_in_wave == 0:
            # Spawn BOSS
            side = random.choice([-100, SCREEN_WIDTH + 100])
            e = Enemy(side, SCREEN_HEIGHT - 50, "OGRE_KING")
            enemies.add(e)
            all_sprites.add(e)
            return # Spawned boss
            
        # If boss is dead (enemies_killed > 0), maybe spawn nothing or small guys?
        # If boss is alive, maybe spawn small helpers?
        if boss_exists and len(enemies) < 3:
             # Spawn minion
             pass
    
    # Regular Spawn Logic
    if len(enemies) < 5 + current_wave: # Cap enemies
        side = random.choice([-50, SCREEN_WIDTH + 50])
        
        # Probabilities
        roll = random.random()
        etype = "OGRE"
        
        # New Diverse Spawn Logic:
        # Check rarest first? Or just probability buckets.
        
        if current_wave > 5 and roll < 0.15: # 15% Troll (Wave 6+)
             etype = "TROLL"
        elif current_wave > 2 and roll < 0.45: # 30% Archer (Wave 3+) (0.15 to 0.45) if Troll fails
             etype = "SKELETON_ARCHER"
        elif current_wave > 1 and roll < 0.75: # 30% Goblin (Wave 2+) (0.45 to 0.75 or 0.0 to 0.75 depending)
             etype = "GOBLIN"
        
        # Default is OGRE (remaining probability)
        # Wave 1: 100% Ogre
        # Wave 2: ~75% Goblin, 25% Ogre (since roll < 0.75 catches most)
        # Wave 3: ~30% Archer, ~30% Goblin, ~40% Ogre
        
        e = Enemy(side, SCREEN_HEIGHT - 50, etype)
        enemies.add(e)
        all_sprites.add(e)

# Cards Logic (Same as before)
cards = []
def generate_upgrades():
    options = [
        {"type": "HEALTH", "name": "Vitality Boost", "desc": "+50 HP (Max & Heal)", "color": GREEN},
        {"type": "SPEED", "name": "Swift Caster", "desc": "+Attack Speed", "color": YELLOW},
        {"type": "DAMAGE", "name": "Arcane Power", "desc": "+25% Damage", "color": MAGENTA},
        {"type": "MULTISHOT", "name": "Fire Mastery", "desc": "Power Up! +Size +Damage", "color": CYAN},
        {"type": "PIERCING", "name": "Spectral Bolt", "desc": "Pierce +1 Enemy", "color": WHITE},
        {"type": "COINS", "name": "Treasure Hunter", "desc": "+500 Instant Coins", "color": GOLD},
    ]
    
    # Filter based on max level (3)
    valid_options = []
    for opt in options:
        t = opt["type"]
        # Unlimited upgrades: Health, Coins
        if t in ["HEALTH", "COINS"]:
            valid_options.append(opt)
        elif t in wizard.upgrade_levels:
            lvl_current = wizard.upgrade_levels[t]
            if lvl_current < 3:
                # Add level info. 
                # If current is 0, next is 1. Text: (1/3)
                # If current is 1, next is 2. Text: (2/3)
                # If current is 2, next is 3. Text: (MAX)
                next_lvl = lvl_current + 1
                tag = f"({next_lvl}/3)" if next_lvl < 3 else "(MAX)"
                
                opt_copy = opt.copy()
                opt_copy["name"] += f" {tag}"
                valid_options.append(opt_copy)
            # If maxed (3), do not append to valid_options
    
    # Be safe if we ran out of options (shouldn't happen with Health/Coins)
    if len(valid_options) < 3:
        # Pad with coins/health
        while len(valid_options) < 3:
            valid_options.append({"type": "COINS", "name": "Bonus Coins", "desc": "+200 Coins", "color": GOLD})
            
    selection = random.sample(valid_options, 3)
    return selection

def apply_card(card):
    global score
    t = card["type"]
    
    if t == "HEALTH":
        wizard.max_health += 50 
        wizard.health = wizard.max_health
    elif t == "COINS":
        global TOTAL_COINS
        TOTAL_COINS += 500
    else:
        # Stat upgrades
        if t in wizard.upgrade_levels and wizard.upgrade_levels[t] < 3:
            wizard.upgrade_levels[t] += 1
            
            if t == "SPEED":
                wizard.attack_speed_boost += 3 # Nerfed from 5
            elif t == "DAMAGE":
                wizard.damage_multiplier += 0.15 # Nerfed from 0.25
            elif t == "MULTISHOT":
                wizard.multishot += 1
            elif t == "PIERCING":
                wizard.piercing += 1

def draw_cards_ui(surface, events):
    global current_wave, enemies_killed_in_wave, total_enemies_spawned_in_wave, current_biome, game_state, cards
    
    # Overlay
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 200))
    surface.blit(s, (0,0))
    
    title = font.render(f"WAVE {current_wave} CLEARED!", True, WHITE)
    surface.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 80)))
    
    global cards
    if not cards: cards = generate_upgrades()
    
    mouse_pos = pygame.mouse.get_pos()
    
    clicked = False
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            clicked = True
    
    start_x = (SCREEN_WIDTH - (3 * 250 + 40)) // 2
    
    for i, c in enumerate(cards):
        rect = pygame.Rect(start_x + i * 270, 150, 250, 350)
        col = (40, 40, 40)
        if rect.collidepoint(mouse_pos):
            col = (60, 60, 60)
            if clicked:
                apply_card(c)
                cards = []
                global shop_return_target, game_state
                global spawn_timer, enemies_killed_in_wave
                # Next wave
                current_wave += 1
                enemies_killed_in_wave = 0
                total_enemies_spawned_in_wave = 0
                if current_wave > 2: current_biome = "ICE"
                if current_wave > 4: current_biome = "VOLCANO"
                
                game_state = "PLAYING"
                
                pygame.time.wait(200)
                return
        
        pygame.draw.rect(surface, col, rect, border_radius=10)
        pygame.draw.rect(surface, c["color"], rect, 4, border_radius=10)
        
        name = card_font.render(c["name"], True, c["color"])
        desc = small_font.render(c["desc"], True, WHITE)
        
        surface.blit(name, name.get_rect(center=rect.center))
        surface.blit(desc, desc.get_rect(midtop=(rect.centerx, rect.centery + 30)))

    # Draw Shop Hint
    shop_hint = shop_font.render("Press [S] to Open Shop", True, GOLD)
    surface.blit(shop_hint, shop_hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)))

# --- MAIN LOOPS ---
spawn_timer = 0
lightning_timer = 0 # For auto lightning
tornado_cooldown = 0
dragon_cooldown = 0

running = True
while running:
    # Global Input
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT: running = False
    
    # State Machine
    if game_state == "MENU":
        draw_menu(screen)
        
        # Logic for buttons (must match draw_menu rects)
        ui_center_x = int(SCREEN_WIDTH * 0.7)
        start_y = 250
        btn_w, btn_h = 280, 55
        spacing = 15
        
        # Check clicks
        mouse_pos = pygame.mouse.get_pos()
        click = False
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                click = True
        
        # Reconstruct rects to check collisions
        # 0: PLAY
        rect_play = pygame.Rect(ui_center_x - btn_w//2, start_y, btn_w, btn_h)
        if rect_play.collidepoint(mouse_pos) and click:
            reset_run()
            
        # 1: SHOP
        rect_shop = pygame.Rect(ui_center_x - btn_w//2, start_y + (btn_h + spacing), btn_w, btn_h)
        if rect_shop.collidepoint(mouse_pos) and click:
            shop_return_target = "MENU"
            game_state = "SHOP"
            
        # 2: EXIT
        rect_exit = pygame.Rect(ui_center_x - btn_w//2, start_y + 2*(btn_h + spacing), btn_w, btn_h)
        if rect_exit.collidepoint(mouse_pos) and click:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            reset_run()
        if keys[pygame.K_s]:
            shop_return_target = "MENU"
            game_state = "SHOP"
        if keys[pygame.K_q]:
            running = False
    elif game_state == "SHOP":
        # Handle Scroll
        for e in events:
            if e.type == pygame.MOUSEWHEEL:
                shop_scroll_y += e.y * 30
                # Clamp scroll_y
                # Calculate max scroll down (total height of content - screen height)
                total_content_height = 200 + len(UNLOCKED_ABILITIES) * 120 + 20 + 50 + len(SHOP_UPGRADES_LIST) * 120
                max_scroll_down = -(total_content_height - SCREEN_HEIGHT + 130 + 60) # Header + Footer height
                if max_scroll_down > 0: max_scroll_down = 0 # If content is smaller than screen, no scroll
                
                if shop_scroll_y > 0: shop_scroll_y = 0
                if shop_scroll_y < max_scroll_down: shop_scroll_y = max_scroll_down
                
        draw_shop(screen)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or (keys[pygame.K_RETURN] and shop_return_target == "PLAYING"):
            game_state = shop_return_target
            shop_scroll_y = 0 # Reset scroll
         
         # Arrow key scroll
        if keys[pygame.K_UP]: shop_scroll_y += 10
        if keys[pygame.K_DOWN]: shop_scroll_y -= 10
        
        # Clamp scroll_y for arrow keys too
        total_content_height = 200 + len(UNLOCKED_ABILITIES) * 120 + 20 + 50 + len(SHOP_UPGRADES_LIST) * 120
        max_scroll_down = -(total_content_height - SCREEN_HEIGHT + 130 + 60)
        if max_scroll_down > 0: max_scroll_down = 0
        
        if shop_scroll_y > 0: shop_scroll_y = 0
        if shop_scroll_y < max_scroll_down: shop_scroll_y = max_scroll_down
            
    elif game_state == "PLAYING":
        # 1. Update Logic
        keys = pygame.key.get_pressed()
        wizard.update(keys, [])
        
        # Shooting
        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            projs = wizard.shoot() # Now returns list
            if projs: 
                projectiles.add(projs)
                all_sprites.add(projs)

        # Ability Inputs
        if UNLOCKED_ABILITIES["TORNADO"] and keys[pygame.K_t] and tornado_cooldown == 0:
            cast_tornado()
            tornado_cooldown = 300 # 5 sec
            
        if UNLOCKED_ABILITIES["DRAGON"] and keys[pygame.K_r] and dragon_cooldown == 0:
            cast_dragon()
            dragon_cooldown = 1800 # 30 sec
        
        if tornado_cooldown > 0: tornado_cooldown -= 1
        if dragon_cooldown > 0: dragon_cooldown -= 1
        
        # Auto Lightning
        if UNLOCKED_ABILITIES["LIGHTNING"]:
            if lightning_timer <= 0:
                cast_lightning()
                lightning_timer = 120 # 2 sec
            lightning_timer -= 1
            
        # Weapon Switching
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1: wizard.select_weapon(1)
                if e.key == pygame.K_2: wizard.select_weapon(2)
                if e.key == pygame.K_3: wizard.select_weapon(3)
                if e.key == pygame.K_4: wizard.select_weapon(4)
                    


        # Projectiles
        # Spawning
        if spawn_timer <= 0:
            spawn_enemy_logic()
            # Slower waves:
            # Base 120 (2 sec) minus wave scaling (but not too fast)
            spawn_timer = 120 - (current_wave * 2) 
            if spawn_timer < 40: spawn_timer = 40
            
            # If Boss alive, slow down spawn a lot
            is_boss_alive = False
            for e in enemies:
                if e.enemy_type == "OGRE_KING":
                    is_boss_alive = True
                    break
            
            if is_boss_alive:
                spawn_timer = 300 # 5 sec
                
        spawn_timer -= 1

        # Projectiles
        projectiles.update(enemies) 
        enemy_projectiles.update() # Ranged enemy shots
        
        for p in projectiles:
            if p.rect.left > SCREEN_WIDTH or p.rect.right < 0 or p.rect.bottom < 0 or p.rect.top > SCREEN_HEIGHT:
                 p.kill()

        # Enemy Projectile Collisions
        hits = pygame.sprite.spritecollide(wizard, enemy_projectiles, True)
        for hit in hits:
             wizard.health -= hit.damage
             # Feedback
             for _ in range(5):
                    particles.append({'x': wizard.rect.centerx, 'y': wizard.rect.centery, 'life': 10, 'max_life': 10, 'size': 4, 'color': (200, 50, 255)})
             if wizard.health <= 0:
                 game_state = "GAME_OVER"

        # Enemies Logic (+ Shooting)
        # Player Collisions & Enemy Attacks
        boss_active = None
        
        for e in enemies:
            # 1. Update Enemy (Pass Player Rect for aiming)
            new_proj = e.update(wizard.rect)
            if new_proj:
                enemy_projectiles.add(new_proj)
                all_sprites.add(new_proj)
            
            # Track Boss for UI
            if e.enemy_type == "OGRE_KING":
                boss_active = e
            
            # 2. Attack Damage (Direct Hit / Melee)
            # EXPLICITLY IGNORE ARCHERS here. They damage via projectiles only.
            if e.enemy_type != "SKELETON_ARCHER":
                if e.did_attack and e.damage > 0:
                    # Melee Hit Logic
                    # Check distance to be fair (don't hit from across screen if player dash away)
                    dist_to_p = math.hypot(e.rect.centerx - wizard.rect.centerx, e.rect.centery - wizard.rect.centery)
                    if dist_to_p < 150: # Melee Range allowance (was 150)
                        wizard.health -= e.damage
                        if wizard.health < 0: wizard.health = 0
                        
                        # Hit feedback
                        for _ in range(10):
                            particles.append({'x': wizard.rect.centerx, 'y': wizard.rect.centery, 'life': 15, 'max_life': 15, 'size': 5, 'color': RED})
                        
                        s_flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                        s_flash.fill((255, 0, 0, 50))
                        screen.blit(s_flash, (0,0))
                        
                        if wizard.health <= 0:
                            game_state = "GAME_OVER"

            # 2. Contact Damage (If they get too close despite range)
            if e.rect.colliderect(wizard.rect):
                wizard.health -= 1 # Contact is just chip damage now
                if wizard.health < 0: wizard.health = 0 # Clamp
                
                # Push player away
                if e.rect.centerx < wizard.rect.centerx:
                    wizard.rect.x += 5
                else:
                    wizard.rect.x -= 5
                    
                if wizard.health <= 0:
                    game_state = "GAME_OVER"
        
        # 3. Enemy Projectiles
        # 3. Enemy Projectiles Collisions
        # We need to update them somewhere? They are updated with projectiles.update(enemies)? 
        # No, projectiles group is Player projectiles.
        # enemy_projectiles is separate.
        
        for p in enemy_projectiles:
            p.update() # Update position
            if p.rect.colliderect(wizard.rect):
                wizard.health -= p.damage
                p.kill()
                # Feedback
                for _ in range(5):
                     particles.append({'x': wizard.rect.centerx, 'y': wizard.rect.centery, 'life': 15, 'max_life': 15, 'size': 5, 'color': RED})
                
                # Flash screen
                s_flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s_flash.fill((255, 0, 0, 30))
                screen.blit(s_flash, (0,0))

                if wizard.health <= 0: game_state = "GAME_OVER"
            
            # Remove if off screen
            if p.rect.right < 0 or p.rect.left > SCREEN_WIDTH or p.rect.bottom < 0 or p.rect.top > SCREEN_HEIGHT:
                 p.kill()
        
        # Wave Check
        enemies_this_wave = ENEMIES_PER_WAVE_BASE + (current_wave - 1) // 2
        # If Boss wave, we need to kill boss?
        if current_wave % 10 == 0:
            # Check if boss dead
            # If enemies_killed_in_wave >= 1 (assuming boss is the 1)
            # But minions might be killed.
            # Only win wave if Boss is NOT in enemies group AND we killed at least 1 big guy?
            # Better: If Boss spawned and is now dead.
            # We can just check `not any(e.enemy_type == "OGRE_KING" for e in enemies)` BUT we need to ensure he spawned.
            # Simplified: Boss wave ends when enemies_killed > enemies_this_wave AND no boss.
            pass # Use standard count for now, but Boss is worth more points/kills?
            
        if enemies_killed_in_wave >= enemies_this_wave:
             game_state = "CARD_SELECT"
             # Clear projectiles
        # 4. Player Projectile Collisions (Damage Enemies)
        # Using groupcollide to check all projectiles against all enemies
        hits = pygame.sprite.groupcollide(enemies, projectiles, False, False)
        for enemy, projs in hits.items():
            for p in projs:
                if not hasattr(p, 'hit_list'): p.hit_list = [] # Safety
                
                # Check if this projectile already hit this enemy (for piercing)
                if enemy not in p.hit_list:
                    enemy.health -= p.damage
                    p.hit_list.append(enemy)
                    
                    # Particle Feedback
                    col = p.color
                    for _ in range(3):
                        particles.append({'x': enemy.rect.centerx, 'y': enemy.rect.centery, 'life': 8, 'max_life': 8, 'size': 3, 'color': col})
                    
                    # Piercing Logic
                    if p.piercing <= 0:
                        p.kill()
                    else:
                        p.piercing -= 1
                        
            if enemy.health <= 0:
                kill_enemy(enemy)

        enemy_projectiles.empty()

        # 2. Drawing
        draw_background_scenery(screen, current_biome, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Draw Entities
        # Draw Entities
        for e in enemies:
            scale = 1.0
            # Boss scale handled in draw()
            # if e.rect.width > 90: scale = 1.5 
            
            # Use internal draw method which delegates
            e.draw(screen)
            
        for ep in enemy_projectiles:
            screen.blit(ep.image, ep.rect)
            
        wizard.draw(screen)
        for p in projectiles:
            p.draw(screen)
            
        for p in enemy_projectiles:
            pygame.draw.circle(screen, (255, 0, 0), p.rect.center, p.rect.width//2)
            pygame.draw.circle(screen, (255, 255, 255), p.rect.center, p.rect.width//2 - 2)
            
        # Draw Particles
        for p in particles[:]:
            p['life'] -= 1
            p['x'] += random.uniform(-1, 1)
            p['y'] += random.uniform(-1, 1)
            if p['life'] <= 0: particles.remove(p); continue
            
            s = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
            col = p['color']
            alpha = int((p['life']/p['max_life'])*255)
            if len(col)==3: col = (*col, alpha)
            else: col = (col[0], col[1], col[2], alpha)
            pygame.draw.circle(s, col, (p['size'], p['size']), p['size'])
            screen.blit(s, (p['x']-p['size'], p['y']-p['size']))

        # Draw Active Effects (Lightning, Dragon)
        for eff in active_effects[:]:
            eff["life"] -= 1
            if eff["life"] <= 0: active_effects.remove(eff); continue
            
            if eff["type"] == "LIGHTNING":
                draw_lightning_bolt(screen, eff["start"], eff["end"])
            elif eff["type"] == "TORNADO_MOVING":
                # Moving Logic for Tornado inside Draw Loop (simplest way without defining new class)
                eff["x"] += 5 * eff["dir"] # Move 5px/frame
                
                # Draw
                draw_tornado_effect(screen, eff["x"], eff["y"], eff["life"])
                
                # Collision with enemies
                t_rect = pygame.Rect(eff["x"] - 40, eff["y"] - 150, 80, 150)
                for e in enemies:
                    if t_rect.colliderect(e.rect):
                        # Push Back
                        e.rect.x += 10 * eff["dir"]
                        # Damage (only every f few frames? No, tornados hurt fast)
                        if eff["life"] % 5 == 0:
                            e.health -= 1
                            if e.health <= 0: kill_enemy(e)
                            
            elif eff["type"] == "DRAGON":
                draw_dragon_effect(screen, eff["x"], eff["y"], eff["life"])

        # UI
        

        draw_health_bar(screen, 20, 20, wizard.health, wizard.max_health)
        
        if boss_active:
             # BOSS BAR at Top Center
             bw = 400
             bh = 30
             bx = SCREEN_WIDTH//2 - bw//2
             by = 20
             # Draw Boss Bar
             pygame.draw.rect(screen, (50, 0, 0), (bx, by, bw, bh))
             pct = max(0, boss_active.health / (OGRE_HEALTH_BASE * 15.0))
             pygame.draw.rect(screen, (200, 0, 0), (bx, by, int(bw*pct), bh))
             pygame.draw.rect(screen, WHITE, (bx, by, bw, bh), 2)
             
             bn = font.render(f"OGRE KING (Wave {current_wave})", True, WHITE)
             screen.blit(bn, (SCREEN_WIDTH//2 - bn.get_width()//2, by - 25))
        
        info = small_font.render(f"Wave: {current_wave}", True, WHITE)
        coins_ui = small_font.render(f"Coins: {TOTAL_COINS}", True, GOLD) # Show persistent coins
        
        screen.blit(info, (SCREEN_WIDTH - 120, 20))
        screen.blit(coins_ui, (SCREEN_WIDTH - 150, 60))
        
        # Cooldowns HUD
        if UNLOCKED_ABILITIES["TORNADO"]:
            col = GREEN if tornado_cooldown == 0 else RED
            txt = small_font.render("Tornado [T]", True, col)
            screen.blit(txt, (20, SCREEN_HEIGHT - 60))
        if UNLOCKED_ABILITIES["DRAGON"]:
            col = GREEN if dragon_cooldown == 0 else RED
            txt = small_font.render("Dragon [R]", True, col)
            screen.blit(txt, (20, SCREEN_HEIGHT - 30))

        # UI: Draw Weapon Hotbar (Moved here to draw ON TOP)
        hotbar_x = 20
        hotbar_y = 120
        slot_size = 50
        padding = 10
        
        # Weapon Metadata for Display
        hotbar_slots = [
            {"key": "1", "id": "DEFAULT", "color": (255, 200, 50)},    # Gold/Yellow
            {"key": "2", "id": "ARCANE_VOLLEY", "color": (200, 100, 255)}, # Purple
            {"key": "3", "id": "VOID_LANCE", "color": (50, 0, 100)},   # Dark Purple
            {"key": "4", "id": "FIRE_RING", "color": (255, 69, 0)}     # Orange Red
        ]
        
        for i, slot in enumerate(hotbar_slots):
            # Status
            is_unlocked = slot["id"] == "DEFAULT" or slot["id"] in wizard.unlocked_weapons
            is_active = wizard.current_weapon == slot["id"]
            
            # Position
            rx = hotbar_x + i * (slot_size + padding)
            ry = hotbar_y
            rect = pygame.Rect(rx, ry, slot_size, slot_size)
            
            # Background Color
            if is_active:
                bg_col = (50, 50, 70) # Highlight active bg
                border_col = (255, 255, 255) # Bright border
                width = 3
            elif is_unlocked:
                bg_col = (30, 30, 30) # Unlocked but inactive
                border_col = (100, 100, 100)
                width = 1
            else:
                bg_col = (10, 10, 10) # Locked
                border_col = (50, 50, 50)
                width = 1
                
            pygame.draw.rect(screen, bg_col, rect, border_radius=5)
            pygame.draw.rect(screen, border_col, rect, width, border_radius=5)
            
            # Weapon Icon (Detailed Representation)
            if is_unlocked:
                center = rect.center
                cx, cy = center
                
                # Base Color (Dimmed if inactive)
                icon_col = slot["color"]
                if not is_active:
                    icon_col = (icon_col[0]//3, icon_col[1]//3, icon_col[2]//3)
                
                if slot["id"] == "DEFAULT":
                    # Simple Spark Orb
                    pygame.draw.circle(screen, icon_col, center, 8)
                    if is_active:
                        pygame.draw.circle(screen, (255, 255, 200), center, 4) # Inner glow
                        
                elif slot["id"] == "ARCANE_VOLLEY":
                    # Three small orbs in local spread
                    #  o
                    # o o
                    offsets = [(0, -6), (-6, 4), (6, 4)]
                    for ox, oy in offsets:
                        pygame.draw.circle(screen, icon_col, (cx + ox, cy + oy), 4)
                        
                elif slot["id"] == "VOID_LANCE":
                    # A diagonal beam/line
                    #  /
                    pygame.draw.line(screen, icon_col, (cx - 10, cy + 10), (cx + 10, cy - 10), 4)
                    if is_active:
                        pygame.draw.line(screen, (200, 100, 255), (cx - 10, cy + 10), (cx + 10, cy - 10), 1)
                        
                elif slot["id"] == "FIRE_RING":
                    # A Ring (Hollow Circle)
                    pygame.draw.circle(screen, icon_col, center, 12, 3)
                    if is_active:
                         # Flames on ring?
                         pass

                # Key Number
                key_txt = small_font.render(slot["key"], True, (200, 200, 200) if is_active else (80, 80, 80))
                screen.blit(key_txt, (rect.right - 15, rect.bottom - 20))
            else:
                # Draw Lock? Or just empty dark slot
                key_txt = small_font.render(slot["key"], True, (40, 40, 40))
                screen.blit(key_txt, (rect.right - 15, rect.bottom - 20))

    elif game_state == "CARD_SELECT":
        draw_cards_ui(screen, events)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
             shop_return_target = "CARD_SELECT"
             game_state = "SHOP"
        
    elif game_state in ["GAME_OVER", "VICTORY"]:
        screen.fill(BLACK)
        txt = "VICTORY!" if game_state == "VICTORY" else "GAME OVER"
        col = GREEN if game_state == "VICTORY" else RED
        
        t = font.render(txt, True, col)
        s = small_font.render(f"Final Score: {score} - Coins Earned: {TOTAL_COINS}", True, WHITE)
        r = small_font.render("Press [ESC] to Return Menu", True, GRAY)
        
        cx, cy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
        screen.blit(t, t.get_rect(center=(cx, cy - 40)))
        screen.blit(s, s.get_rect(center=(cx, cy)))
        screen.blit(r, r.get_rect(center=(cx, cy + 50)))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = "MENU"

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
