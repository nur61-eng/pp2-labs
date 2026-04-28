import pygame
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint")

font  = pygame.font.SysFont("Arial", 16)
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

canvas = pygame.Surface((width, height - 60))
canvas.fill(white)

tool    = "pen"
color   = black
drawing = False
start   = None
temp    = None
running = True

def draw_shape(surface, tool, color, start, end):
    x1, y1 = start
    x2, y2 = end

    if tool == "rect":
        x = min(x1, x2); y = min(y1, y2)
        w = abs(x2 - x1); h = abs(y2 - y1)
        pygame.draw.rect(surface, color, (x, y, w, h), 2)

    elif tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        sx = x1 if x2 >= x1 else x1 - side
        sy = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surface, color, (sx, sy, side, side), 2)

    elif tool == "circle":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        r  = int(math.hypot(x2 - x1, y2 - y1) // 2)
        if r > 0:
            pygame.draw.circle(surface, color, (cx, cy), r, 2)

    elif tool == "rtriangle":
        p1 = (x1, y1)
        p2 = (x1, y2)
        p3 = (x2, y2)
        pygame.draw.polygon(surface, color, [p1, p2, p3], 2)

    elif tool == "etriangle":
        side = abs(x2 - x1)
        if side < 4:
            return
        cx = (x1 + x2) // 2
        p1 = (cx, y1)
        p2 = (x1, y1 + int(side * math.sqrt(3) / 2))
        p3 = (x2, y1 + int(side * math.sqrt(3) / 2))
        pygame.draw.polygon(surface, color, [p1, p2, p3], 2)

    elif tool == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        p1 = (cx, y1)
        p2 = (x2, cy)
        p3 = (cx, y2)
        p4 = (x1, cy)
        pygame.draw.polygon(surface, color, [p1, p2, p3, p4], 2)

tools_list = [
    ("Pen",      "pen"),
    ("Rect",     "rect"),
    ("Square",   "square"),
    ("Circle",   "circle"),
    ("R.Tri",    "rtriangle"),
    ("E.Tri",    "etriangle"),
    ("Rhombus",  "rhombus"),
    ("Eraser",   "eraser"),
    ("Clear",    "clear"),
]

btn_w  = 72
btn_x0 = 380

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

                for i, (name, tname) in enumerate(tools_list):
                    bx = btn_x0 + i * btn_w
                    if bx < mx < bx + btn_w - 4 and 12 < my < 47:
                        if tname == "clear":
                            canvas.fill(white)
                        else:
                            tool = tname
            else:
                drawing = True
                start   = (mx, my - 60)
                temp    = canvas.copy()

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start:
                mx, my = event.pos
                end = (mx, my - 60)
                if tool not in ("pen", "eraser", "clear"):
                    draw_shape(canvas, tool, color, start, end)
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

    for i, (name, tname) in enumerate(tools_list):
        bx = btn_x0 + i * btn_w
        active = (tool == tname)
        btn_color = (100, 100, 200) if active else (60, 60, 60)
        pygame.draw.rect(screen, btn_color, (bx, 12, btn_w - 4, 35), border_radius=4)
        label = font.render(name, True, white)
        screen.blit(label, (bx + (btn_w - 4) // 2 - label.get_width() // 2, 22))

    if drawing and start and tool not in ("pen", "eraser", "clear"):
        mx, my = pygame.mouse.get_pos()
        preview = temp.copy()
        end = (mx, my - 60)
        draw_shape(preview, tool, color, start, end)
        screen.blit(preview, (0, 60))

    pygame.display.flip()

pygame.quit()