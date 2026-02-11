
// Configuration Constants
const CONFIG = {
    SCREEN_WIDTH: 1280,
    SCREEN_HEIGHT: 720,
    PHYSICS: {
        GRAVITY: 0.5,
        JUMP_STRENGTH: -14,
        PLAYER_SPEED: 6,
        PROJECTILE_SPEED: 12,
        OGRE_SPEED: 3
    },
    STATS: {
        PLAYER_MAX_HEALTH: 100,
        OGRE_HEALTH_BASE: 2,
        OGRE_BOSS_HEALTH: 50,
        WAND_DAMAGE: 2
    },
    COLORS: {
        WHITE: '#FFFFFF', RED: '#FF3232', GREEN: '#32FF32', BLUE: '#3232FF',
        GOLD: '#FFD700', MAGENTA: '#FF00FF', CYAN: '#00FFFF',
        WAND_LEVELS: ['#FFFFFF', '#00BFFF', '#32CD32', '#FF0000']
    }
};

// Graphics Helpers
function drawCircle(ctx, x, y, r, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
}

function drawRect(ctx, x, y, w, h, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
}

function drawPolygon(ctx, points, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(points[0][0], points[0][1]);
    for (let i = 1; i < points.length; i++) ctx.lineTo(points[i][0], points[i][1]);
    ctx.closePath();
    ctx.fill();
}

// --- PORTED ASSETS ---

function drawWizard(ctx, x, y, facingRight, isCasting, wandLevel) {
    const direction = facingRight ? 1 : -1;
    const playerSize = 60;

    // Robe
    ctx.fillStyle = '#0000B4'; // Base Blue
    // Round rect for body
    ctx.beginPath();
    ctx.roundRect(x - playerSize / 2, y - playerSize, playerSize, playerSize, 10);
    ctx.fill();

    // Robe Highlight
    ctx.fillStyle = '#3232DC';
    const hX = x - playerSize / 2 + (facingRight ? 5 : 0);
    ctx.beginPath();
    ctx.roundRect(hX, y - playerSize, playerSize - 10, playerSize - 5, 8);
    ctx.fill();

    // Head
    const headRadius = playerSize / 3;
    const headY = y - playerSize - 2;
    drawCircle(ctx, x, headY, headRadius, '#FFDCB4'); // Skin

    // Beard
    ctx.fillStyle = '#F0F0FF';
    ctx.beginPath();
    ctx.moveTo(x - headRadius + 2, headY + 5);
    ctx.lineTo(x + headRadius - 2, headY + 5);
    ctx.lineTo(x + (10 * direction), headY + 25);
    ctx.lineTo(x, headY + 20);
    ctx.closePath();
    ctx.fill();

    // Hat
    const hatBaseY = headY - headRadius + 5;
    ctx.fillStyle = '#2828A0';
    // Brim
    ctx.beginPath();
    ctx.ellipse(x, hatBaseY, headRadius + 8, 5, 0, 0, Math.PI * 2);
    ctx.fill();
    // Cone
    const hatTipX = x - (10 * direction);
    const hatTipY = hatBaseY - 45;
    ctx.beginPath();
    ctx.moveTo(x - headRadius, hatBaseY);
    ctx.lineTo(x + headRadius, hatBaseY);
    ctx.lineTo(hatTipX, hatTipY);
    ctx.closePath();
    ctx.fill();

    // Eyes
    const eyeX = x + (8 * direction);
    drawCircle(ctx, eyeX, headY - 2, 3, '#000');
    drawCircle(ctx, eyeX + 1, headY - 3, 1, '#FFF');

    // Staff
    const staffX = x + (25 * direction);
    const staffY = y - playerSize / 2 + 5;

    ctx.strokeStyle = '#654321';
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(staffX, staffY + 35);
    ctx.lineTo(staffX + (5 * direction), staffY - 35);
    ctx.stroke();

    // Crystal
    const crystalPos = { x: staffX + (5 * direction), y: staffY - 35 };
    const wandColor = CONFIG.COLORS.WAND_LEVELS[Math.min(wandLevel, 3)];

    drawCircle(ctx, crystalPos.x, crystalPos.y, 8, wandColor);
    if (isCasting) {
        ctx.strokeStyle = '#E0FFFF';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(crystalPos.x, crystalPos.y, 12, 0, Math.PI * 2);
        ctx.stroke();
    }

    // Return emission point (Waist/Staff center)
    return { x: staffX, y: staffY };
}

function drawOgre(ctx, x, y, facingRight, scale, isBoss) {
    const direction = facingRight ? 1 : -1;
    const ogreSize = isBoss ? 150 : 70;

    // Scaling context
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(scale, scale);
    // Draw relative to (0,0) as bottom center

    // Pants
    ctx.fillStyle = '#8B4513';
    ctx.fillRect(-20, -25, 15, 25);
    ctx.fillRect(5, -25, 15, 25);

    // Torso
    ctx.fillStyle = '#556B2F';
    ctx.beginPath();
    ctx.roundRect(-25, -65, 50, 45, 10);
    ctx.fill();

    // Abs shading
    ctx.strokeStyle = '#32461E';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(0, -60); ctx.lineTo(0, -30); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-15, -45); ctx.lineTo(15, -45); ctx.stroke();

    // Head
    const headY = -75;
    drawCircle(ctx, 0, headY, 18, '#556B2F');

    // Face
    const eyeX = 8 * direction;
    drawCircle(ctx, eyeX, headY - 5, 4, '#FF0000');
    // Brow
    ctx.beginPath(); ctx.moveTo(eyeX - 5, headY - 10); ctx.lineTo(eyeX + 5, headY - 8); ctx.stroke();
    // Mouth
    ctx.strokeStyle = '#000';
    ctx.beginPath(); ctx.moveTo(0, headY + 8); ctx.lineTo(10 * direction, headY + 8); ctx.stroke();
    // Tooth
    ctx.fillStyle = '#FFF';
    ctx.beginPath();
    ctx.moveTo(5 * direction, headY + 8);
    ctx.lineTo(8 * direction, headY + 3);
    ctx.lineTo(11 * direction, headY + 8);
    ctx.fill();

    // Club
    const handX = 25 * direction;
    const handY = -45;
    // Arm
    ctx.strokeStyle = '#556B2F';
    ctx.lineWidth = 10;
    ctx.beginPath(); ctx.moveTo(15 * direction, -55); ctx.lineTo(handX, handY); ctx.stroke();
    // Club Stick
    ctx.strokeStyle = '#64503C';
    ctx.lineWidth = 12;
    const clubEndX = handX + (10 * direction);
    const clubEndY = handY - 30;
    ctx.beginPath(); ctx.moveTo(handX, handY); ctx.lineTo(clubEndX, clubEndY); ctx.stroke();
    drawCircle(ctx, clubEndX, clubEndY, 15, '#64503C');

    ctx.restore();
}

function drawBackground(ctx, biome, width, height) {
    if (biome === "FOREST") {
        // Sky
        const grad = ctx.createLinearGradient(0, 0, 0, height);
        grad.addColorStop(0, '#87CEEB');
        grad.addColorStop(1, '#E0F7FA');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, width, height);

        // Mountains
        ctx.fillStyle = '#6495ED';
        ctx.beginPath(); ctx.moveTo(0, height); ctx.lineTo(200, height - 200); ctx.lineTo(400, height); ctx.fill();
        ctx.fillStyle = '#4682B4';
        ctx.beginPath(); ctx.moveTo(300, height); ctx.lineTo(600, height - 250); ctx.lineTo(900, height); ctx.fill();

        // Ground
        ctx.fillStyle = '#228B22';
        ctx.fillRect(0, height - 50, width, 50);

    } else if (biome === "ICE") {
        ctx.fillStyle = '#C8E6FF';
        ctx.fillRect(0, 0, width, height);
        // Ice mountains
        ctx.fillStyle = '#E6F0FF';
        ctx.beginPath(); ctx.moveTo(100, height); ctx.lineTo(400, height - 300); ctx.lineTo(700, height); ctx.fill();

        ctx.fillStyle = '#F0F8FF';
        ctx.fillRect(0, height - 50, width, 50);

    } else if (biome === "VOLCANO") {
        ctx.fillStyle = '#280000';
        ctx.fillRect(0, 0, width, height);
        // Volcano
        ctx.fillStyle = '#140000';
        ctx.beginPath(); ctx.moveTo(200, height); ctx.lineTo(500, height - 300); ctx.lineTo(800, height); ctx.fill();
        // Lava
        ctx.fillStyle = '#FF4500';
        ctx.beginPath(); ctx.moveTo(480, height - 300); ctx.lineTo(500, height - 50); ctx.lineTo(520, height - 300); ctx.fill();

        ctx.fillStyle = '#461414';
        ctx.fillRect(0, height - 50, width, 50);
        ctx.fillStyle = '#FF4500';
        ctx.fillRect(0, height - 15, width, 15);
    }
}

// --- ENGINE ---

class InputManager {
    constructor() {
        this.keys = {};
        this.touch = { left: false, right: false, jump: false, shoot: false, tornado: false, dragon: false };
        this.joystick = { dx: 0, dy: 0, active: false };

        window.addEventListener('keydown', (e) => this.keys[e.code] = true);
        window.addEventListener('keyup', (e) => this.keys[e.code] = false);
        this.setupTouch();
    }

    setupTouch() {
        const joystickArea = document.getElementById('joystick-area');
        const knob = document.getElementById('joystick-knob');
        let startX;

        joystickArea.addEventListener('touchstart', (e) => {
            e.preventDefault();
            const touch = e.touches[0];
            startX = touch.clientX;
            this.joystick.active = true;
        }, { passive: false });

        joystickArea.addEventListener('touchmove', (e) => {
            if (!this.joystick.active) return;
            e.preventDefault();
            const touch = e.touches[0];
            const dx = touch.clientX - startX;
            const maxDist = 50;
            const clampedX = Math.max(-maxDist, Math.min(maxDist, dx));
            knob.style.transform = `translateX(${clampedX}px)`;

            this.touch.right = clampedX > 10;
            this.touch.left = clampedX < -10;
        }, { passive: false });

        joystickArea.addEventListener('touchend', (e) => {
            this.joystick.active = false;
            knob.style.transform = 'translate(0,0)';
            this.touch.left = false;
            this.touch.right = false;
        });

        const btnJump = document.getElementById('btn-jump');
        btnJump.addEventListener('touchstart', (e) => { e.preventDefault(); this.touch.jump = true; });
        btnJump.addEventListener('touchend', (e) => { this.touch.jump = false; });

        const btnShoot = document.getElementById('btn-shoot');
        btnShoot.addEventListener('touchstart', (e) => { e.preventDefault(); this.touch.shoot = true; });
        btnShoot.addEventListener('touchend', (e) => { this.touch.shoot = false; });

        document.getElementById('btn-skill-tornado').addEventListener('touchstart', () => this.touch.tornado = true);
        document.getElementById('btn-skill-dragon').addEventListener('touchstart', () => this.touch.dragon = true);
    }
}

class Wizard {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 60;
        this.height = 60;
        this.velX = 0;
        this.velY = 0;
        this.facingRight = true;
        this.jumping = false;

        this.health = 1000; // God mode mostly
        this.maxHealth = 1000;
        this.wandLevel = 3; // Maxed for fun
        this.coins = 999999;
        this.abilities = { LIGHTNING: true, TORNADO: true, DRAGON: true };

        this.cooldown = 0;
    }

    update(input) {
        this.velX = 0;
        if (input.keys['ArrowLeft'] || input.touch.left) { this.velX = -CONFIG.PHYSICS.PLAYER_SPEED; this.facingRight = false; }
        if (input.keys['ArrowRight'] || input.touch.right) { this.velX = CONFIG.PHYSICS.PLAYER_SPEED; this.facingRight = true; }

        if ((input.keys['Space'] || input.touch.jump) && !this.jumping) {
            this.velY = CONFIG.PHYSICS.JUMP_STRENGTH;
            this.jumping = true;
        }

        this.velY += CONFIG.PHYSICS.GRAVITY;
        this.y += this.velY;
        this.x += this.velX;

        if (this.y + this.height > CONFIG.SCREEN_HEIGHT - 50) {
            this.y = CONFIG.SCREEN_HEIGHT - 50 - this.height;
            this.velY = 0;
            this.jumping = false;
        }

        if (this.x < 0) this.x = 0;
        if (this.x + this.width > CONFIG.SCREEN_WIDTH) this.x = CONFIG.SCREEN_WIDTH - this.width;

        if (this.cooldown > 0) this.cooldown--;
    }

    draw(ctx) {
        return drawWizard(ctx, this.x + this.width / 2, this.y + this.height, this.facingRight, this.cooldown > 10, this.wandLevel);
    }
}

class Projectile {
    constructor(x, y, right, color) {
        this.x = x;
        this.y = y;
        this.radius = 10;
        this.velX = right ? CONFIG.PHYSICS.PROJECTILE_SPEED : -CONFIG.PHYSICS.PROJECTILE_SPEED;
        this.color = color;
        this.active = true;
    }

    update() {
        this.x += this.velX;
        if (this.x < 0 || this.x > CONFIG.SCREEN_WIDTH) this.active = false;
    }

    draw(ctx) {
        // Glow
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
        drawCircle(ctx, this.x, this.y, this.radius, this.color);
        ctx.shadowBlur = 0;
        drawCircle(ctx, this.x, this.y, 6, '#FFF');
    }
}

class Ogre {
    constructor(x, y, wave, isBoss) {
        this.x = x;
        this.y = y;
        this.width = isBoss ? 150 : 70;
        this.height = isBoss ? 150 : 70;
        this.isBoss = isBoss;
        this.health = isBoss ? CONFIG.STATS.OGRE_BOSS_HEALTH : CONFIG.STATS.OGRE_HEALTH_BASE + (wave - 1) * 2;
        this.speed = isBoss ? 2 : CONFIG.PHYSICS.OGRE_SPEED + (wave * 0.5);
        this.active = true;
        this.wave = wave;
    }

    update(targetX) {
        const dx = targetX - (this.x + this.width / 2);
        const dir = dx > 0 ? 1 : -1;
        this.x += dir * this.speed;
        if (this.y + this.height > CONFIG.SCREEN_HEIGHT - 50) {
            this.y = CONFIG.SCREEN_HEIGHT - 50 - this.height;
        }
    }

    draw(ctx) {
        const scale = this.isBoss ? 2.0 : 1.0;
        const centerX = this.x + this.width / 2;
        const bottomY = this.y + this.height;
        // Direction check
        // Simplified: always face player? No, store facing.
        // For now assume facing left if x > player
        // Let's passed FacingRight to draw
        // Hack for demo:
        drawOgre(ctx, centerX, bottomY, true, scale, this.isBoss);
    }
}

// System
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const input = new InputManager();

let wizard = new Wizard(100, 300);
let projectiles = [];
let enemies = [];
let particles = [];
let wave = 1;
let enemiesSpawned = 0;
let enemiesKilled = 0;
let gameState = "MENU";
let currentBiome = "FOREST";

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    CONFIG.SCREEN_WIDTH = canvas.width;
    CONFIG.SCREEN_HEIGHT = canvas.height;
}
window.addEventListener('resize', resize);
resize();

// MAIN LOOP
function gameLoop() {
    // Biome Logic
    if (wave > 2) currentBiome = "ICE";
    if (wave > 4) currentBiome = "VOLCANO";

    drawBackground(ctx, currentBiome, canvas.width, canvas.height);

    if (gameState === "MENU") {
        ctx.fillStyle = "rgba(0,0,0,0.7)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#00FFFF";
        ctx.font = "bold 60px Arial";
        ctx.textAlign = "center";
        ctx.fillText("WIZARD vs OGRES", canvas.width / 2, canvas.height / 2 - 50);

        ctx.fillStyle = "#FFF";
        ctx.font = "30px Arial";
        ctx.fillText("Tap to Start", canvas.width / 2, canvas.height / 2 + 50);

        if (input.touch.jump || input.touch.shoot || Object.values(input.keys).some(k => k)) {
            gameState = "PLAYING";
            // Fullscreen request
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen();
            }
        }
        requestAnimationFrame(gameLoop);
        return;
    }

    // Update
    wizard.update(input);

    if ((input.keys['KeyZ'] || input.touch.shoot) && wizard.cooldown <= 0) {
        const tip = wizard.draw(ctx); // Use draw to calc tip? No, separate render logic
        // We do render in draw loop. 
        // Just calc position here logic:
        const facing = wizard.facingRight;
        const sx = facing ? wizard.x + 50 : wizard.x - 10;
        const sy = wizard.y + 30;
        const col = CONFIG.COLORS.WAND_LEVELS[3]; // Max level

        projectiles.push(new Projectile(sx, sy, facing, col));
        wizard.cooldown = 15;
    }

    // Skills
    if (input.touch.tornado) {
        enemies.forEach(e => { e.x += 300 * (e.x > wizard.x ? 1 : -1); e.health -= 5; });
        input.touch.tornado = false;
    }
    if (input.touch.dragon) {
        enemies.forEach(e => e.health = 0);

        // Visual
        ctx.fillStyle = "rgba(255, 0, 0, 0.5)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        input.touch.dragon = false;
    }

    // Entities Update
    projectiles.forEach(p => p.update());
    enemies.forEach(e => e.update(wizard.x + wizard.width / 2));

    projectiles = projectiles.filter(p => p.active);
    enemies = enemies.filter(e => e.active);

    // Collisions
    projectiles.forEach(p => {
        enemies.forEach(e => {
            if (p.active && e.active &&
                p.x > e.x && p.x < e.x + e.width &&
                p.y > e.y && p.y < e.y + e.height) {

                p.active = false;
                e.health -= CONFIG.STATS.WAND_DAMAGE;

                // Particles
                particles.push({ x: e.x + e.width / 2, y: e.y + e.height / 2, life: 10, color: p.color });

                if (e.health <= 0) {
                    e.active = false;
                    enemiesKilled++;
                }
            }
        });
    });

    // Spawning
    // Simple spawning logic
    if (enemies.length < 5 && enemiesSpawned < 10) {
        if (Math.random() < 0.05) {
            const side = Math.random() > 0.5 ? 1 : -1;
            const x = side === 1 ? CONFIG.SCREEN_WIDTH + 50 : -100;
            const isBoss = (wave === 5 && enemiesSpawned === 9);
            enemies.push(new Ogre(x, CONFIG.SCREEN_HEIGHT - 100, wave, isBoss));
            enemiesSpawned++;
        }
    }

    if (enemiesKilled >= 10) {
        wave++;
        enemiesSpawned = 0;
        enemiesKilled = 0;
    }

    // Drawing
    wizard.draw(ctx);
    enemies.forEach(e => e.draw(ctx));
    projectiles.forEach(p => p.draw(ctx));

    // Particles
    for (let i = particles.length - 1; i >= 0; i--) {
        let p = particles[i];
        p.life--;
        drawCircle(ctx, p.x + (Math.random() - 0.5) * 10, p.y + (Math.random() - 0.5) * 10, 5, p.color);
        if (p.life <= 0) particles.splice(i, 1);
    }

    // UI
    ctx.fillStyle = "#FFF";
    ctx.font = "bold 24px Arial";
    ctx.textAlign = "left";
    ctx.fillText(`Coins: ∞`, 20, 40);
    ctx.fillText(`Wave: ${wave}`, 20, 70);

    if (input.touch.dragon) {
        ctx.fillStyle = "RED";
        ctx.font = "50px Arial";
        ctx.fillText("DRAGON!", canvas.width / 2 - 100, canvas.height / 2);
    }

    requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);
wizard.abilities.TORNADO = true;
wizard.abilities.DRAGON = true;
document.getElementById('btn-skill-tornado').style.display = 'block';
document.getElementById('btn-skill-dragon').style.display = 'block';
