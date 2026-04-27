import pygame

class Ball:
    def __init__(self, screen_width, screen_height):
        self.radius = 25       
        self.speed = 20         
        self.color = (255, 0, 0)  

        
        self.x = screen_width // 2
        self.y = screen_height // 2

        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, direction):
        if direction == "up":
            if self.y - self.radius - self.speed >= 0:
                self.y -= self.speed

        elif direction == "down":
            if self.y + self.radius + self.speed <= self.screen_height:
                self.y += self.speed

        elif direction == "left":
            if self.x - self.radius - self.speed >= 0:
                self.x -= self.speed

        elif direction == "right":
            if self.x + self.radius + self.speed <= self.screen_width:
                self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)