import pygame
import sys
from datetime import datetime
import tools

pygame.init()

WIDTH, HEIGHT = 1000,850
TOOLBAR_H = 60
CANVAS_H = HEIGHT - TOOLBAR_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - TSIS2")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
text_font = pygame.font.SysFont("Arial", 22)

white = (255, 255, 255)
black = (0, 0, 0)
gray  = (80, 80, 80)
lgray = (180, 180, 180)

COLORS = [
    (0,   0,   0  ), (220, 50,  50 ), (50,  200, 50 ),
    (50,  50,  220), (255, 220, 0  ), (255, 140, 0  ),
    (180, 0,   220), (0,   200, 200), (255, 255, 255),
]

TOOLS = [
    ("Pencil",  "pencil"),
    ("Line",    "line"),
    ("Rect",    "rect"),
    ("Square",  "square"),
    ("Circle",  "circle"),
    ("R.Tri",   "rtriangle"),
    ("E.Tri",   "etriangle"),
    ("Rhombus", "rhombus"),
    ("Fill",    "fill"),
    ("Text",    "text"),
    ("Eraser",  "eraser"),
]

SIZES = [2, 5, 10]

canvas = pygame.Surface((WIDTH, CANVAS_H))
canvas.fill(white)

tool       = "pencil"
color      = black
brush_size = SIZES[0]
drawing    = False
start      = None
last_pos   = None
temp       = None

text_mode  = False
text_pos   = None
text_input = ""

running = True


def canvas_pos(mx, my):
    return (mx, my - TOOLBAR_H)


def draw_toolbar():
    pygame.draw.rect(screen, (60, 60, 60), (0, 0, WIDTH, TOOLBAR_H))

    for i, c in enumerate(COLORS):
        rx = 5 + i * 38
        pygame.draw.rect(screen, c, (rx, 10, 30, 30), border_radius=4)
        pygame.draw.rect(screen, black, (rx, 10, 30, 30), 1, border_radius=4)
        if c == color:
            pygame.draw.rect(screen, white, (rx, 10, 30, 30), 3, border_radius=4)

    pygame.draw.rect(screen, color, (5, 44, 30, 14), border_radius=3)

    tool_x = 360
    btn_w  = 62
    for i, (name, tname) in enumerate(TOOLS):
        bx = tool_x + i * btn_w
        active = (tool == tname)
        bc = (100, 100, 200) if active else (50, 50, 50)
        pygame.draw.rect(screen, bc, (bx, 8, btn_w - 4, 22), border_radius=4)
        lbl = font.render(name, True, white)
        screen.blit(lbl, (bx + (btn_w - 4) // 2 - lbl.get_width() // 2, 13))

    for i, s in enumerate(SIZES):
        bx = tool_x + i * 50
        active = (brush_size == s)
        bc = (100, 180, 100) if active else (50, 50, 50)
        pygame.draw.rect(screen, bc, (bx, 34, 44, 18), border_radius=3)
        lbl = font.render(f"{s}px [{i+1}]", True, white)
        screen.blit(lbl, (bx + 22 - lbl.get_width() // 2, 36))

    hint = font.render("Ctrl+S = Save", True, lgray)
    screen.blit(hint, (WIDTH - hint.get_width() - 8, 22))


while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if text_mode:
                if event.key == pygame.K_RETURN:
                    if text_input:
                        rendered = text_font.render(text_input, True, color)
                        canvas.blit(rendered, text_pos)
                    text_mode  = False
                    text_input = ""
                    text_pos   = None
                elif event.key == pygame.K_ESCAPE:
                    text_mode  = False
                    text_input = ""
                    text_pos   = None
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    if event.unicode:
                        text_input += event.unicode
            else:
                if event.key == pygame.K_1:
                    brush_size = SIZES[0]
                elif event.key == pygame.K_2:
                    brush_size = SIZES[1]
                elif event.key == pygame.K_3:
                    brush_size = SIZES[2]
                elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    fname = f"canvas_{ts}.png"
                    pygame.image.save(canvas, fname)
                    pygame.display.set_caption(f"Saved: {fname}")

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if my < TOOLBAR_H:
                for i, c in enumerate(COLORS):
                    if 5 + i * 38 < mx < 35 + i * 38 and 10 < my < 40:
                        color = c
                tool_x = 360
                btn_w  = 62
                for i, (name, tname) in enumerate(TOOLS):
                    bx = tool_x + i * btn_w
                    if bx < mx < bx + btn_w - 4 and 8 < my < 30:
                        tool = tname
                for i, s in enumerate(SIZES):
                    bx = tool_x + i * 50
                    if bx < mx < bx + 44 and 34 < my < 52:
                        brush_size = s
            else:
                cp = canvas_pos(mx, my)
                if tool == "fill":
                    tools.flood_fill(canvas, cp, color)
                elif tool == "text":
                    text_mode  = True
                    text_pos   = cp
                    text_input = ""
                else:
                    drawing  = True
                    start    = cp
                    last_pos = cp
                    temp     = canvas.copy()

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start:
                mx, my = event.pos
                cp = canvas_pos(mx, my)
                if tool == "line":
                    tools.draw_line(canvas, color, start, cp, brush_size)
                elif tool == "rect":
                    tools.draw_rect(canvas, color, start, cp, brush_size)
                elif tool == "square":
                    tools.draw_square(canvas, color, start, cp, brush_size)
                elif tool == "circle":
                    tools.draw_circle(canvas, color, start, cp, brush_size)
                elif tool == "rtriangle":
                    tools.draw_rtriangle(canvas, color, start, cp, brush_size)
                elif tool == "etriangle":
                    tools.draw_etriangle(canvas, color, start, cp, brush_size)
                elif tool == "rhombus":
                    tools.draw_rhombus(canvas, color, start, cp, brush_size)
            drawing  = False
            start    = None
            last_pos = None

        if event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos
            if my > TOOLBAR_H:
                cp = canvas_pos(mx, my)
                if tool == "pencil":
                    if last_pos:
                        tools.draw_pencil(canvas, color, last_pos, cp, brush_size)
                    last_pos = cp
                elif tool == "eraser":
                    pygame.draw.circle(canvas, white, cp, brush_size * 3)

    screen.fill(gray)
    screen.blit(canvas, (0, TOOLBAR_H))

    if drawing and start and tool in ("line", "rect", "square", "circle", "rtriangle", "etriangle", "rhombus"):
        mx, my = pygame.mouse.get_pos()
        cp = canvas_pos(mx, my)
        preview = temp.copy()
        if tool == "line":
            tools.draw_line(preview, color, start, cp, brush_size)
        elif tool == "rect":
            tools.draw_rect(preview, color, start, cp, brush_size)
        elif tool == "square":
            tools.draw_square(preview, color, start, cp, brush_size)
        elif tool == "circle":
            tools.draw_circle(preview, color, start, cp, brush_size)
        elif tool == "rtriangle":
            tools.draw_rtriangle(preview, color, start, cp, brush_size)
        elif tool == "etriangle":
            tools.draw_etriangle(preview, color, start, cp, brush_size)
        elif tool == "rhombus":
            tools.draw_rhombus(preview, color, start, cp, brush_size)
        screen.blit(preview, (0, TOOLBAR_H))

    if text_mode and text_pos and text_input:
        preview_surf = text_font.render(text_input + "|", True, color)
        screen.blit(preview_surf, (text_pos[0], text_pos[1] + TOOLBAR_H))

    draw_toolbar()
    pygame.display.flip()

pygame.quit()
sys.exit()