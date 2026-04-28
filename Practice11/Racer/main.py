import pygame
import random

pygame.init()

width, height = 500, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racer")

white  = (255, 255, 255)
black  = (0, 0, 0)
red    = (200, 0, 0)
gray   = (100, 100, 100)
yellow = (255, 220, 0)
green  = (0, 140, 0)
blue   = (0, 100, 255)
orange = (255, 165, 0)
silver = (192, 192, 192)
gold   = (255, 215, 0)

clock = pygame.time.Clock()
font  = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 16)

player = pygame.Rect(225, 580, 50, 80)
player_speed = 5

COIN_TYPES = [
    {"name": "bronze", "color": orange, "points": 1, "weight": 60},
    {"name": "silver", "color": silver, "points": 3, "weight": 30},
    {"name": "gold",   "color": gold,   "points": 5, "weight": 10},
]

def random_coin_type():
    total = sum(c["weight"] for c in COIN_TYPES)
    r = random.randint(1, total)
    cumulative = 0
    for coin_type in COIN_TYPES:
        cumulative += coin_type["weight"]
        if r <= cumulative:
            return coin_type
    return COIN_TYPES[0]

def create_coin(y_offset):
    coin_type = random_coin_type()
    rect = pygame.Rect(random.choice([80, 180, 280, 380]), y_offset, 20, 20)
    return {"rect": rect, "type": coin_type}

coins = [create_coin(-200 - i * 200) for i in range(3)]

enemies = []
for i in range(4):
    enemy = pygame.Rect(random.choice([80, 180, 280, 380]), -100 - i * 150, 50, 80)
    enemies.append(enemy)

enemy_speeds = [random.randint(3, 6) for _ in enemies]

road_y     = 0
score      = 0
collected  = 0
coin_score = 0

SPEED_UP_EVERY = 5
speed_level = 0

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]  and player.x > 65:  player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < 385: player.x += player_speed

    for index, enemy in enumerate(enemies):
        enemy.y += enemy_speeds[index]
        if enemy.y > height:
            enemy.x = random.choice([80, 180, 280, 380])
            enemy.y = -100
            enemy_speeds[index] = random.randint(3, 6) + speed_level

    for coin in coins:
        coin["rect"].y += 5
        if coin["rect"].y > height:
            coin["rect"].x = random.choice([80, 180, 280, 380])
            coin["rect"].y = -random.randint(100, 400)
            coin["type"] = random_coin_type()

    for coin in coins:
        if player.colliderect(coin["rect"]):
            coin_score += coin["type"]["points"]
            collected += 1

            new_level = collected // SPEED_UP_EVERY
            if new_level > speed_level:
                speed_level = new_level
                for i in range(len(enemy_speeds)):
                    enemy_speeds[i] += 1

            coin["rect"].x = random.choice([80, 180, 280, 380])
            coin["rect"].y = -random.randint(100, 400)
            coin["type"] = random_coin_type()

    for enemy in enemies:
        if player.colliderect(enemy):
            running = False

    score += 1

    screen.fill(black)
    pygame.draw.rect(screen, gray,  (60, 0, 380, height))
    pygame.draw.rect(screen, green, (0, 0, 60, height))
    pygame.draw.rect(screen, green, (440, 0, 60, height))

    for lane_x in [145, 230, 315]:
        line_y = road_y
        while line_y < height:
            pygame.draw.rect(screen, white, (lane_x - 3, line_y, 6, 40))
            line_y += 90
    road_y = (road_y + 5) % 90

    pygame.draw.rect(screen, blue, player, border_radius=6)

    for enemy in enemies:
        pygame.draw.rect(screen, red, enemy, border_radius=6)

    for coin in coins:
        pygame.draw.circle(screen, coin["type"]["color"], coin["rect"].center, 10)
        pts = small_font.render(f"+{coin['type']['points']}", True, coin["type"]["color"])
        screen.blit(pts, (coin["rect"].x - 2, coin["rect"].y - 15))

    screen.blit(font.render(f"Score: {score // 10}", True, white), (70, 10))
    coin_text = font.render(f"Coins: {collected}  +{coin_score}pts", True, yellow)
    screen.blit(coin_text, (width - coin_text.get_width() - 10, 10))

    if speed_level > 0:
        lvl_text = font.render(f"Speed lvl: {speed_level}", True, red)
        screen.blit(lvl_text, (70, 35))

    for i, ct in enumerate(COIN_TYPES):
        pygame.draw.circle(screen, ct["color"], (75 + i * 100, height - 30), 8)
        lbl = small_font.render(f"+{ct['points']}", True, ct["color"])
        screen.blit(lbl, (88 + i * 100, height - 38))

    pygame.display.flip()

pygame.quit()