
import pygame
import sys
import random
import math
from src.config import *
from src.assets import *
from src.entities import Wizard, Enemy, Projectile

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

TOTAL_COINS = 0
UNLOCKED_ABILITIES = { "LIGHTNING": False, "TORNADO": False, "DRAGON": False}
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
                        t3 = min(others2, key=lambda e: math.hypot(e.rect.centerx - t2.rect.centerx, e.rect.centery - t2.rect.centery))
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
    surface.fill(BLACK)
    
    title = font.render(f"WIZARD vs OGRES", True, CYAN)
    start_txt = shop_font.render("Press [ENTER] to Start Game", True, WHITE)
    shop_txt = shop_font.render("Press [S] to Open Shop", True, GOLD)
    quit_txt = shop_font.render("Press [Q] to Quit", True, RED)
    
    coins_txt = small_font.render(f"Coins: {TOTAL_COINS}", True, GOLD)

    cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    
    surface.blit(title, title.get_rect(center=(cx, cy - 100)))
    surface.blit(start_txt, start_txt.get_rect(center=(cx, cy)))
    surface.blit(shop_txt, shop_txt.get_rect(center=(cx, cy + 50)))
    surface.blit(quit_txt, quit_txt.get_rect(center=(cx, cy + 100)))
    surface.blit(coins_txt, (20, 20))

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
        {"id": "DRAGON", "name": "Dragon Summon (Key: R)", "cost": COST_DRAGON, "desc": "Summon Dragon to clear screen."}
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
    
    score = 0
    current_wave = 1
    enemies_killed_in_wave = 0
    total_enemies_spawned_in_wave = 0
    current_biome = "FOREST"
    
    enemies.empty()
    projectiles.empty()
    all_sprites.empty()
    particles.clear()
    
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
    global total_enemies_spawned_in_wave
    
    # Calculate Enemies Per Wave: Harder scaling
    # Was (wave-1)//2. Now just wave count (linear increase)
    enemies_this_wave = ENEMIES_PER_WAVE_BASE + int(current_wave * 2.0)
    
    if total_enemies_spawned_in_wave >= enemies_this_wave: return

    side = random.choice([-1, 1])
    x = -100 if side == -1 else SCREEN_WIDTH + 100
    
    # Calculate Mix of Weak vs Strong
    # Round 1: 5 weak (0 strong).
    # Round 5: 5 weak, 2 strong.
    # Pattern: Weak stays around 5 (or grows slowly), Strong grows.
    
    # Let's say Strong count = (current_wave - 1) // 2
    strong_count = (current_wave - 1) // 2
    # Ensure at least some weak enemies for satisfaction
    weak_count = enemies_this_wave - strong_count
    
    # Determine type for this specific spawn
    # If we haven't spawned all strongs yet... random chance based on remaining?
    # Simplified: Spawn strongs with probability
    prob_strong = strong_count / enemies_this_wave if enemies_this_wave > 0 else 0
    
    is_strong = random.random() < prob_strong
    
    # Determine Health Thresholds based on player power
    player_dmg = BASE_WAND_DAMAGE * wizard.damage_multiplier
    
    # Difficulty Spike Multiplier (Requested: +20% at 10, +30% at 20)
    # Let's interpret as cumulative multipliers
    diff_mult = 1.0
    if current_wave >= 10:
        diff_mult *= 1.2
    if current_wave >= 20:
        diff_mult *= 1.3 # Cumulative with previous? "En la 20 un 30%".
                         # If it means 30% ON TOP of 20%, it's 1.2 * 1.3 = 1.56
                         # If it means total 30% boost from base, it's 1.3.
                         # "Suba un 20... y luego un 30" -> Usually cumulative steps.
    
    # Also scale with wave count generally
    diff_mult += (current_wave * 0.05) 
    
    if is_strong:
         # Strong enemy health (Harder)
         health = (player_dmg * 4.0) * diff_mult # Signficantly buffed from 2.2
         enemy_type = "GOBLIN" if current_wave % 3 == 0 else "OGRE"
         if current_wave > 5 and random.random() < 0.4: enemy_type = "TROLL"
    else:
         # Weak enemy health (Harder)
         health = (player_dmg * 2.0) * diff_mult # Buffed from 1.2

         enemy_type = "GOBLIN" if random.random() < 0.5 else "OGRE"

    # Create Enemy
    enemy = Enemy(x, SCREEN_HEIGHT - 50, enemy_type)
    enemy.health = health
    
    # Speed Scaling
    enemy.speed += (current_wave * 0.05)
    if current_wave > 20: enemy.speed *= 1.2

    enemies.add(enemy)
    all_sprites.add(enemy)
    total_enemies_spawned_in_wave += 1

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
                # Next wave
                current_wave += 1
                enemies_killed_in_wave = 0
                total_enemies_spawned_in_wave = 0
                if current_wave > 2: current_biome = "ICE"
                if current_wave > 4: current_biome = "VOLCANO"
                
                # Go to Shop instead of Playing immediately
                shop_return_target = "PLAYING"
                game_state = "SHOP"
                
                pygame.time.wait(200)
                return
        
        pygame.draw.rect(surface, col, rect, border_radius=10)
        pygame.draw.rect(surface, c["color"], rect, 4, border_radius=10)
        
        name = card_font.render(c["name"], True, c["color"])
        desc = small_font.render(c["desc"], True, WHITE)
        
        surface.blit(name, name.get_rect(center=rect.center))
        surface.blit(desc, desc.get_rect(midtop=(rect.centerx, rect.centery + 30)))

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
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            reset_run()
        if keys[pygame.K_s]:
            shop_return_target = "MENU"
            game_state = "SHOP"
        if keys[pygame.K_q]:
            running = False
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

        # Projectiles
        projectiles.update()
        for p in projectiles:
            if p.rect.left > SCREEN_WIDTH or p.rect.right < 0: p.kill()
            

        # Spawning
        if spawn_timer <= 0:
            spawn_enemy_logic()
            # Slower waves:
            # Base 120 (2 sec) minus wave scaling (but not too fast)
            spawn_timer = 120 - (current_wave * 10)
            if spawn_timer < 40: spawn_timer = 40
        spawn_timer -= 1
        
        # Enemies
        hits = pygame.sprite.groupcollide(enemies, projectiles, False, False)
        for enemy, projs in hits.items():
            for p in projs:
                if not hasattr(p, 'hit_list'): p.hit_list = [] # Safety
                
                if enemy not in p.hit_list:
                    enemy.health -= p.damage
                    p.hit_list.append(enemy)
                    
                    particles.append({'x': enemy.rect.centerx, 'y': enemy.rect.centery, 'life': 8, 'max_life': 8, 'size': 3, 'color': p.color})
                    
                    if p.piercing <= 0:
                        p.kill()
                    else:
                        p.piercing -= 1
                        
            if enemy.health <= 0:
                kill_enemy(enemy)
        
        # Player Collisions
        for e in enemies:
            e.update(wizard.rect.centerx)
            if e.rect.colliderect(wizard.rect):
                wizard.health -= 1
                if wizard.health <= 0:
                    game_state = "GAME_OVER"
        
        # Wave Check
        enemies_this_wave = ENEMIES_PER_WAVE_BASE + (current_wave - 1) // 2
        if enemies_killed_in_wave >= enemies_this_wave:
             game_state = "CARD_SELECT"
             # No victory condition for infinite waves, unless we want a boss every X waves
             # maybe wave 10, 20 etc.

        # 2. Drawing
        draw_background_scenery(screen, current_biome, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Draw Entities
        for e in enemies:
            scale = 1.0
            if e.rect.width > 90: scale = 1.5 # Boss scale
            
            # Use internal draw method which delegates
            e.draw(screen)
            
        wizard.draw(screen)
        for p in projectiles:
            p.draw(screen)
            
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

    elif game_state == "CARD_SELECT":
        draw_cards_ui(screen, events)
        
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
