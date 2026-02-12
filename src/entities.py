
import pygame
import random
from src.config import *
from src.assets import *

class Wizard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0)) # Transparent
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.vel_y = 0
        self.vel_x = 0
        self.facing_right = True
        self.jumping = False
        self.is_casting = False
        self.cast_cooldown = 0
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.wand_level = 0 # 0 to 3 visual level
        self.attack_speed_boost = 0
        self.damage_multiplier = 1.0
        self.multishot = 1
        self.piercing = 0
        self.coins = 0
        # Tracks how many times each stat has been upgraded (Max 3)
        self.upgrade_levels = {
            "SPEED": 0,
            "DAMAGE": 0,
            "MULTISHOT": 0,
            "PIERCING": 0,
            "HEALTH": 0 # Unlimited
        }
        self.abilities = {
            "LIGHTNING": False,
            "TORNADO": False,
            "DRAGON": False
        }

    def update(self, keys, platforms):
        # Movement
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True

        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and not self.jumping:
            self.vel_y = JUMP_STRENGTH
            self.jumping = True

        # Gravity
        self.vel_y += GRAVITY
        
        # Apply Movement Y
        self.rect.y += self.vel_y
        
        # Collision Y
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0: # Falling
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.jumping = False
                elif self.vel_y < 0: # Jumping up into ceiling
                    self.rect.top = platform.bottom
                    self.vel_y = 0
                    
        # Apply Movement X
        self.rect.x += self.vel_x
        
        # Collision X
        for platform in platforms:
             if self.rect.colliderect(platform):
                 if self.vel_x > 0: # Moving right
                     self.rect.right = platform.left
                 elif self.vel_x < 0: # Moving left
                     self.rect.left = platform.right

        # Screen Bounds
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT - 50: # Ground Floor
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.vel_y = 0
            self.jumping = False

        # Cooldown
        if self.cast_cooldown > 0:
            self.cast_cooldown -= 1
            if self.cast_cooldown < 10: # Reset animation state quickly
                self.is_casting = False

    def draw(self, surface):
        color = WAND_COLORS[min(self.wand_level, len(WAND_COLORS)-1)]
        draw_wizard(surface, self.rect.centerx, self.rect.bottom, self.facing_right, self.is_casting, color)

    def shoot(self):
        if self.cast_cooldown == 0:
            self.is_casting = True
            base_cooldown = 20
            self.cast_cooldown = max(5, base_cooldown - self.attack_speed_boost)
            
            # Match visual staff tip from assets.py
            # staff_x = x + (25 * direction)
            # staff_y = y - PLAYER_SIZE // 2 + 5
            
            # Get tip position from draw helper logic or approximate
            # We updated draw_wizard to return tip, but here we need to calculate it or just guess for now
            # Best is to approximate based on the updated draw logic
            
            
            offset_x = 30 if self.facing_right else -30
            offset_y = -40
            
            start_x = self.rect.centerx + offset_x
            
            projectiles = []
            damage = BASE_WAND_DAMAGE * self.damage_multiplier
            color = WAND_COLORS[min(self.wand_level, len(WAND_COLORS)-1)]
            
            # Single Shot Logic (Scaled by Multishot Upgrades)
            start_y_base = self.rect.bottom + offset_y
            
            # Instead of multiple projectiles, we scale ONE projectile
            # Scale factor based on multishot level (1, 2, 3...)
            # Nerfed Scaling: +0.3 size per level instead of 0.5
            scale_factor = 1.0 + (self.multishot - 1) * 0.3
            
            p = Projectile(start_x, start_y_base, self.facing_right, color)
            
            # Increase Damage based on "multishot" level (which is now just Power Up)
            # Nerfed Damage: +40% damage per level instead of +100%
            multishot_dmg_mult = 1.0 + (self.multishot - 1) * 0.4
            p.damage = damage * multishot_dmg_mult
            
            # Increase Size visually
            p.scale = scale_factor
            
            # Pass scale to projectile so it draws bigger
            
            p.piercing = self.piercing
            projectiles.append(p)
            
            return projectiles
        return None

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="OGRE"):
        super().__init__()
        self.enemy_type = enemy_type
        
        # Stats based on type
        if self.enemy_type == "GOBLIN":
            size = 50
            self.speed = OGRE_SPEED * 1.5
            self.health = OGRE_HEALTH_BASE * 0.5
        elif self.enemy_type == "TROLL":
            size = 90
            self.speed = OGRE_SPEED * 0.7
            self.health = OGRE_HEALTH_BASE * 2.0
        else: # OGRE
            size = OGRE_SIZE
            self.speed = OGRE_SPEED
            self.health = OGRE_HEALTH_BASE

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.vel_y = 0
        self.direction = -1 
        
    def update(self, player_x):
        # Tracking AI
        if self.rect.centerx > player_x:
            self.direction = -1
        else:
            self.direction = 1
            
        self.rect.x += self.speed * self.direction
        
        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        if self.rect.bottom > SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.vel_y = 0

    def draw(self, surface):
        t = pygame.time.get_ticks()
        if self.enemy_type == "GOBLIN":
            draw_goblin(surface, self.rect.centerx, self.rect.bottom, self.direction > 0, tick=t)
        elif self.enemy_type == "TROLL":
             draw_troll(surface, self.rect.centerx, self.rect.bottom, self.direction > 0, tick=t)
        else:
            draw_ogre(surface, self.rect.centerx, self.rect.bottom, self.direction > 0, tick=t)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right, color=WHITE):
        super().__init__()
        self.color = color
        self.damage = BASE_WAND_DAMAGE
        self.piercing = 0
        self.hit_list = [] 
        self.scale = 1.0 # Default scale
        
        # Fireball sizing
        self.image = pygame.Surface((PROJECTILE_RADIUS*3, PROJECTILE_RADIUS*3), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = PROJECTILE_SPEED if facing_right else -PROJECTILE_SPEED
        self.vel_y = 0 
        
        self.life = 100
        
        # Particle System for Trail
        # Each particle: [x, y, vx, vy, life, max_life, size, color_type]
        self.particles = []
        
    def update_rect(self):
        # Update rect size based on scale if not already done
        # We'll do this on the fly or after init if scale is changed externally
        # But rect center needs to persist.
        c = self.rect.center
        
        # Base Size * Scale
        size = int(PROJECTILE_RADIUS * 3 * self.scale)
        if self.image.get_width() != size:
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.center = c
            
    def update(self):
        # Ensure rect matches scale (lazy update or just check)
        # For performance, maybe just trust it was set right.
        # But we set .scale AFTER init in Wizard.shoot. So we need to apply it once.
        # Let's just blindly re-calc rect size if it seems small compared to scale?
        # Actually, let's just use the draw function radius logic.
        # But collision depends on self.rect.
        
        # Hacky fix: Check if rect width matches expected
        expected_size = int(PROJECTILE_RADIUS * 3 * self.scale)
        if self.rect.width != expected_size:
            c = self.rect.center
            self.image = pygame.Surface((expected_size, expected_size), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.center = c
            
        self.rect.x += self.vel_x
        self.life -= 1
        
        # --- Spawn Trail Particles ---
        # Spawn more particles if bigger
        count = 3 + int(self.scale * 2)
        
        for _ in range(count):
            # Random offset from center (scaled)
            spread = 5 * self.scale
            off_x = random.uniform(-spread, spread)
            off_y = random.uniform(-spread, spread)
            
            px = self.rect.centerx + off_x
            py = self.rect.centery + off_y
            
            # Velocity
            vx = -self.vel_x * 0.3 + random.uniform(-1, 1)
            vy = random.uniform(-2, 2) 
            
            life = random.randint(15, 30)
            size = random.randint(4, 10) * self.scale # Scale particles too
            
            # Store particle
            self.particles.append([px, py, vx, vy, life, life, size])

        # --- Update Particles ---
        for p in self.particles:
            p[0] += p[2] # x move
            p[1] += p[3] # y move
            p[4] -= 1    # life drain
            p[6] *= 0.95 # shrink
            
        # Remove dead particles
        self.particles = [p for p in self.particles if p[4] > 0 and p[6] > 1] 

        return self.life > 0

    def draw(self, surface):
        draw_projectile(surface, self.rect.centerx, self.rect.centery, self.color, self.particles, self.scale)

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.vel_x = random.uniform(-2, 2)
        self.vel_y = random.uniform(-2, 2)
        self.life = 30
        self.max_life = 30
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1
        return self.life > 0
