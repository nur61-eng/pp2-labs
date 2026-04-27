import pygame
from player import MusicPlayer

WIDTH = 500
HEIGHT = 300
FPS = 30


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    player = MusicPlayer()

    font_big = pygame.font.SysFont("Arial", 28)
    font_small = pygame.font.SysFont("Arial", 20)

    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  
                running = False

            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_p:    
                    player.play()
                elif event.key == pygame.K_s:  
                    player.stop()
                elif event.key == pygame.K_n:  
                    player.next_track()
                elif event.key == pygame.K_b:  
                    player.prev_track()
                elif event.key == pygame.K_q:  
                    running = False

        screen.fill(BLACK)  

        track_text = font_big.render(
            player.get_track_name(), True, WHITE
        )
        screen.blit(track_text, (20, 50))

        if player.is_playing:
            status_text = font_small.render("▶ Playing", True, GREEN)
        else:
            status_text = font_small.render("■ Stopped", True, RED)
        screen.blit(status_text, (20, 100))

        controls = [
            "P - Play",
            "S - Stop", 
            "N - Next",
            "B - Back",
            "Q - Quit"
        ]
        for i, text in enumerate(controls):
            hint = font_small.render(text, True, GRAY)
            screen.blit(hint, (20, 160 + i * 25))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()