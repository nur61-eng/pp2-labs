import pygame
from clock import Clock

pygame.init()

width, height = 600, 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Mickey's Clock")

fps_clock = pygame.time.Clock()
clock = Clock(screen, width,height)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    clock.draw()
    pygame.display.flip()
    fps_clock.tick(60)

pygame.quit()