import pygame
import random

pygame.init()

cell = 20
cols, rows = 25, 25
width, height = cols * cell, rows * cell

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

clock    = pygame.time.Clock()
font     = pygame.font.SysFont("Arial", 24)
font_big = pygame.font.SysFont("Arial", 40)
small    = pygame.font.SysFont("Arial", 15)

white  = (255, 255, 255)
black  = (0, 0, 0)
green  = (0, 200, 0)
red    = (200, 0, 0)
yellow = (255, 220, 0)
gray   = (40, 40, 40)
orange = (255, 140, 0)
pink   = (255, 80, 180)

FOOD_TYPES = [
    {"name": "normal", "color": red,    "points": 10, "weight": 60, "lifetime": 8},
    {"name": "bonus",  "color": orange, "points": 25, "weight": 30, "lifetime": 5},
    {"name": "rare",   "color": pink,   "points": 50, "weight": 10, "lifetime": 3},
]

def random_food_type():
    total = sum(f["weight"] for f in FOOD_TYPES)
    r = random.randint(1, total)
    cum = 0
    for ft in FOOD_TYPES:
        cum += ft["weight"]
        if r <= cum:
            return ft
    return FOOD_TYPES[0]

def new_food(snake):
    while True:
        pos = (random.randint(0, cols - 1), random.randint(0, rows - 1))
        if pos not in snake:
            ft = random_food_type()
            return {"pos": pos, "type": ft, "timer": ft["lifetime"]}

snake     = [(10, 10), (9, 10), (8, 10)]
direction = (1, 0)
score     = 0
level     = 1
eaten     = 0
speed     = 8
gameover  = False

food = new_food(snake)
food_tick = 0

running = True

while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP    and direction != (0, 1):  direction = (0, -1)
            if event.key == pygame.K_DOWN  and direction != (0, -1): direction = (0, 1)
            if event.key == pygame.K_LEFT  and direction != (1, 0):  direction = (-1, 0)
            if event.key == pygame.K_RIGHT and direction != (-1, 0): direction = (1, 0)
            if gameover and event.key == pygame.K_r:
                snake     = [(10, 10), (9, 10), (8, 10)]
                direction = (1, 0)
                score     = 0
                level     = 1
                eaten     = 0
                speed     = 8
                gameover  = False
                food      = new_food(snake)
                food_tick = 0

    if not gameover:
        food_tick += 1
        ticks_per_second = speed
        if food_tick >= ticks_per_second * food["type"]["lifetime"]:
            food = new_food(snake)
            food_tick = 0

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if head[0] < 0 or head[0] >= cols or head[1] < 0 or head[1] >= rows or head in snake:
            gameover = True
        else:
            snake.insert(0, head)
            if head == food["pos"]:
                score  += food["type"]["points"]
                eaten  += 1
                food    = new_food(snake)
                food_tick = 0
                if eaten % 4 == 0:
                    level += 1
                    speed += 2
            else:
                snake.pop()

    screen.fill(gray)

    food_color = food["type"]["color"]
    time_left = food["type"]["lifetime"] - food_tick / speed
    if time_left < 1.5:
        flash = pygame.time.get_ticks() // 200 % 2
        if flash:
            food_color = white

    fx, fy = food["pos"]
    pygame.draw.rect(screen, food_color, (fx * cell + 2, fy * cell + 2, cell - 4, cell - 4), border_radius=4)
    pts_label = small.render(f"+{food['type']['points']}", True, food_color)
    screen.blit(pts_label, (fx * cell, fy * cell - 14))

    timer_ratio = max(0, (food["type"]["lifetime"] - food_tick / max(speed, 1)) / food["type"]["lifetime"])
    bar_width = int((cell - 4) * timer_ratio)
    pygame.draw.rect(screen, yellow, (fx * cell + 2, fy * cell - 4, bar_width, 3))

    for i, part in enumerate(snake):
        color = (0, 220, 0) if i == 0 else green
        pygame.draw.rect(screen, color, (part[0] * cell + 1, part[1] * cell + 1, cell - 2, cell - 2), border_radius=4)

    screen.blit(font.render(f"Score: {score}", True, white), (10, 10))
    lvl = font.render(f"Level: {level}", True, yellow)
    screen.blit(lvl, (width - lvl.get_width() - 10, 10))

    for i, ft in enumerate(FOOD_TYPES):
        pygame.draw.rect(screen, ft["color"], (10 + i * 70, height - 22, 12, 12), border_radius=3)
        lbl = small.render(f"+{ft['points']}", True, ft["color"])
        screen.blit(lbl, (26 + i * 70, height - 23))

    if gameover:
        over = font_big.render("GAME OVER", True, red)
        hint = font.render("R - restart", True, white)
        screen.blit(over, (width // 2 - over.get_width() // 2, height // 2 - 40))
        screen.blit(hint, (width // 2 - hint.get_width() // 2, height // 2 + 20))

    pygame.display.flip()

pygame.quit()