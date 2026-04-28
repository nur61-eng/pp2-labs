import pygame

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint")

font  = pygame.font.SysFont("Arial", 18)
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
gray  = (180, 180, 180)

colors = [
    (0,   0,   0  ),
    (220, 50,  50 ),
    (50,  200, 50 ),
    (50,  50,  220),
    (255, 220, 0  ),
    (255, 140, 0  ),
    (180, 0,   220),
    (255, 255, 255),
]

canvas    = pygame.Surface((width, height - 60))
canvas.fill(white)

tool      = "pen"
color     = black
drawing   = False
start     = None
temp      = None
running   = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if my < 60:
                for i, c in enumerate(colors):
                    if 10 + i * 45 < mx < 45 + i * 45 and 12 < my < 47:
                        color = c
                if 380 < mx < 440: tool = "pen"
                if 445 < mx < 505: tool = "rect"
                if 510 < mx < 570: tool = "circle"
                if 575 < mx < 635: tool = "eraser"
                if 640 < mx < 700: canvas.fill(white)
            else:
                drawing = True
                start   = (mx, my - 60)
                temp    = canvas.copy()

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start:
                mx, my = event.pos
                end = (mx, my - 60)
                if tool == "rect":
                    x = min(start[0], end[0])
                    y = min(start[1], end[1])
                    w = abs(end[0] - start[0])
                    h = abs(end[1] - start[1])
                    pygame.draw.rect(canvas, color, (x, y, w, h), 2)
                if tool == "circle":
                    cx = (start[0] + end[0]) // 2
                    cy = (start[1] + end[1]) // 2
                    r  = int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5 // 2)
                    if r > 0:
                        pygame.draw.circle(canvas, color, (cx, cy), r, 2)
            drawing = False
            start   = None

        if event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos
            if my > 60:
                pos = (mx, my - 60)
                if tool == "pen":
                    pygame.draw.circle(canvas, color, pos, 4)
                if tool == "eraser":
                    pygame.draw.circle(canvas, white, pos, 15)

    screen.fill(gray)
    screen.blit(canvas, (0, 60))

    pygame.draw.rect(screen, (80, 80, 80), (0, 0, width, 60))

    for i, c in enumerate(colors):
        pygame.draw.rect(screen, c,     (10 + i * 45, 12, 35, 35), border_radius=4)
        pygame.draw.rect(screen, black, (10 + i * 45, 12, 35, 35), 2, border_radius=4)
        if c == color:
            pygame.draw.rect(screen, white, (10 + i * 45, 12, 35, 35), 3, border_radius=4)

    for name, tx in [("Pen",380), ("Rect",445), ("Circle",510), ("Eraser",575), ("Clear",640)]:
        btn_color = (100, 100, 200) if tool == name.lower() else (60, 60, 60)
        pygame.draw.rect(screen, btn_color, (tx, 12, 60, 35), border_radius=4)
        label = font.render(name, True, white)
        screen.blit(label, (tx + 30 - label.get_width() // 2, 22))

    if drawing and start and tool in ("rect", "circle"):
        mx, my = pygame.mouse.get_pos()
        preview = temp.copy()
        end = (mx, my - 60)
        if tool == "rect":
            x = min(start[0], end[0])
            y = min(start[1], end[1])
            w = abs(end[0] - start[0])
            h = abs(end[1] - start[1])
            pygame.draw.rect(preview, color, (x, y, w, h), 2)
        if tool == "circle":
            cx = (start[0] + end[0]) // 2
            cy = (start[1] + end[1]) // 2
            r  = int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5 // 2)
            if r > 0:
                pygame.draw.circle(preview, color, (cx, cy), r, 2)
        screen.blit(preview, (0, 60))

    pygame.display.flip()

pygame.quit()