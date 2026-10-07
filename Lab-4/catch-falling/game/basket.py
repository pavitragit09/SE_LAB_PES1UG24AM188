"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.boosted_frames = 0
        self.normal_speed = speed
        self.boost_speed = speed

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def clamp(self, screen_width):
        half_w = self.width / 2
        self.x = max(half_w, min(screen_width - half_w, self.x))

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
