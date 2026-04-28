import pygame
import math
from collections import deque


def draw_pencil(surface, color, last_pos, cur_pos, size):
    pygame.draw.line(surface, color, last_pos, cur_pos, size)


def draw_line(surface, color, start, end, size):
    pygame.draw.line(surface, color, start, end, size)


def draw_rect(surface, color, start, end, size):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(end[0] - start[0])
    h = abs(end[1] - start[1])
    pygame.draw.rect(surface, color, (x, y, w, h), size)


def draw_square(surface, color, start, end, size):
    side = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    sx = start[0] if end[0] >= start[0] else start[0] - side
    sy = start[1] if end[1] >= start[1] else start[1] - side
    pygame.draw.rect(surface, color, (sx, sy, side, side), size)


def draw_circle(surface, color, start, end, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    r = int(math.hypot(end[0] - start[0], end[1] - start[1]) // 2)
    if r > 0:
        pygame.draw.circle(surface, color, (cx, cy), r, size)


def draw_rtriangle(surface, color, start, end, size):
    p1 = (start[0], start[1])
    p2 = (start[0], end[1])
    p3 = (end[0], end[1])
    pygame.draw.polygon(surface, color, [p1, p2, p3], size)


def draw_etriangle(surface, color, start, end, size):
    side = abs(end[0] - start[0])
    if side < 4:
        return
    cx = (start[0] + end[0]) // 2
    p1 = (cx, start[1])
    p2 = (start[0], start[1] + int(side * math.sqrt(3) / 2))
    p3 = (end[0], start[1] + int(side * math.sqrt(3) / 2))
    pygame.draw.polygon(surface, color, [p1, p2, p3], size)


def draw_rhombus(surface, color, start, end, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    p1 = (cx, start[1])
    p2 = (end[0], cy)
    p3 = (cx, end[1])
    p4 = (start[0], cy)
    pygame.draw.polygon(surface, color, [p1, p2, p3, p4], size)


def flood_fill(surface, pos, fill_color):
    x, y = pos
    w, h = surface.get_size()
    target_color = surface.get_at((x, y))[:3]
    fill_rgb = fill_color[:3] if len(fill_color) > 3 else fill_color

    if target_color == fill_rgb:
        return

    queue = deque()
    queue.append((x, y))
    visited = set()
    visited.add((x, y))

    while queue:
        cx, cy = queue.popleft()
        if surface.get_at((cx, cy))[:3] != target_color:
            continue
        surface.set_at((cx, cy), fill_rgb)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))