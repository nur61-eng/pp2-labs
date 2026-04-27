import pygame
import datetime

class Clock:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.center = (width // 2, height // 2)

        self.face = pygame.image.load("images/mickey.png").convert_alpha()
        self.right_hand = pygame.image.load("images/right.png").convert_alpha()
        self.left_hand = pygame.image.load("images/left.png").convert_alpha()

        self.face = pygame.transform.scale(self.face, (500, 500))

    def get_angles(self):
        now = datetime.datetime.now()
        seconds = now.second
        minutes = now.minute

        angle_sec = -seconds * 6
        angle_min = -minutes * 6

        return angle_min, angle_sec

    def draw_hand(self, image, angle):
        rotated = pygame.transform.rotate(image, angle)
        rect = rotated.get_rect(center=self.center)
        self.screen.blit(rotated, rect)

    def draw(self):
        face_rect = self.face.get_rect(center=self.center)
        self.screen.blit(self.face, face_rect)

        angle_min, angle_sec = self.get_angles()

        self.draw_hand(self.right_hand, angle_min)
        self.draw_hand(self.left_hand, angle_sec)