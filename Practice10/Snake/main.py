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

white  = (255, 255, 255)
black  = (0, 0, 0)
green  = (0, 200, 0)
red    = (200, 0, 0)
yellow = (255, 220, 0)
gray   = (40, 40, 40)

snake     = [(10, 10), (9, 10), (8, 10)]
direction = (1, 0)
food      = (15, 15)
score     = 0
level     = 1
eaten     = 0
speed     = 8
gameover  = False

def new_food():
    while True:
        pos = (random.randint(0, cols - 1), random.randint(0, rows - 1))
        if pos not in snake:
            return pos

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
                food      = new_food()
                score     = 0
                level     = 1
                eaten     = 0
                speed     = 8
                gameover  = False

    if not gameover:
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if head[0] < 0 or head[0] >= cols or head[1] < 0 or head[1] >= rows or head in snake:
            gameover = True
        else:
            snake.insert(0, head)
            if head == food:
                score  += 10
                eaten  += 1
                food    = new_food()
                if eaten % 4 == 0:
                    level += 1
                    speed += 2
            else:
                snake.pop()

    screen.fill(gray)

    pygame.draw.rect(screen, red, (food[0] * cell + 2, food[1] * cell + 2, cell - 4, cell - 4), border_radius=4)

    for i, part in enumerate(snake):
        color = (0, 220, 0) if i == 0 else green
        pygame.draw.rect(screen, color, (part[0] * cell + 1, part[1] * cell + 1, cell - 2, cell - 2), border_radius=4)

    screen.blit(font.render(f"Score: {score}", True, white), (10, 10))
    lvl = font.render(f"Level: {level}", True, yellow)
    screen.blit(lvl, (width - lvl.get_width() - 10, 10))

    if gameover:
        over = font_big.render("GAME OVER", True, red)
        hint = font.render("R - restart", True, white)
        screen.blit(over, (width // 2 - over.get_width() // 2, height // 2 - 40))
        screen.blit(hint, (width // 2 - hint.get_width() // 2, height // 2 + 20))

    pygame.display.flip()

pygame.quit()