import pygame
from ball import Ball

width=500
height=500
fps=30

white=(255, 255, 255)

def main():
    pygame.init()
    screen=pygame.display.set_mode((width,height))
    pygame.display.set_caption("moving ball game")
    clock=pygame.time.Clock()

    ball=Ball(width,height)

    running=True
    while running:

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                running = False

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    ball.move("up")
                elif event.key==pygame.K_DOWN:
                    ball.move("down")
                elif event.key==pygame.K_LEFT:
                    ball.move("left")
                elif event.key==pygame.K_RIGHT:
                    ball.move("right")

        screen.fill(white)
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()