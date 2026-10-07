"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


BOOST_DURATION_FRAMES = 180
BOOST_COOLDOWN_FRAMES = 180


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.normal_speed = speed
        self.boost_speed = speed * 2
        self.speed = speed
        self.is_boosted = False
        self.boost_timer = 0
        self.cooldown_timer = 0

    def activate_boost(self):
        if not self.is_boosted and self.cooldown_timer <= 0:
            self.is_boosted = True
            self.boost_timer = BOOST_DURATION_FRAMES
            self.speed = self.boost_speed

    def update(self):
        if self.is_boosted:
            self.boost_timer -= 1
            if self.boost_timer <= 0:
                self.is_boosted = False
                self.speed = self.normal_speed
                self.cooldown_timer = BOOST_COOLDOWN_FRAMES
        elif self.cooldown_timer > 0:
            self.cooldown_timer -= 1

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
