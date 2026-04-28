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

clock = pygame.time.Clock()
font  = pygame.font.SysFont("Arial", 24)

player = pygame.Rect(225, 580, 50, 80)
player_speed = 5

enemies = []
for i in range(4):
    enemy = pygame.Rect(random.choice([80, 180, 280, 380]), -100 - i * 150, 50, 80)
    enemies.append(enemy)

coins = []
for i in range(3):
    coin = pygame.Rect(random.choice([80, 180, 280, 380]), -200 - i * 200, 20, 20)
    coins.append(coin)

enemy_speeds = [random.randint(3, 6) for _ in enemies]

road_y    = 0
score     = 0
collected = 0
running   = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]  and player.x > 65:    player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < 385:   player.x += player_speed

    for index, enemy in enumerate(enemies):
        enemy.y += enemy_speeds[index]
        if enemy.y > height:
            enemy.x = random.choice([80, 180, 280, 380])
            enemy.y = -100
            enemy_speeds[index] = random.randint(3, 6)

    for coin in coins:
        coin.y += 5
        if coin.y > height:
            coin.x = random.choice([80, 180, 280, 380])
            coin.y = -100

    for coin in coins:
        if player.colliderect(coin):
            collected += 1
            coin.x = random.choice([80, 180, 280, 380])
            coin.y = -random.randint(100, 400)

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
        pygame.draw.circle(screen, yellow, coin.center, 10)

    screen.blit(font.render(f"Score: {score // 10}", True, white), (70, 10))
    coin_text = font.render(f"Coins: {collected}", True, yellow)
    screen.blit(coin_text, (width - coin_text.get_width() - 10, 10))

    pygame.display.flip()

pygame.quit()