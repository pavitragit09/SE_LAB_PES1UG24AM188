"""
GameEngine: owns the basket and all falling objects.

Starter version: basket movement and spawning both work at a basic
level (Tasks 2 and 3 ask you to improve them), there's no speed boost
yet (Task 4 builds it from scratch), and catch detection has two
known bugs (see game/collision.py and the catch-checking loop below)
that Task 1 asks you to fix.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_MIN = 35
SPAWN_INTERVAL_MAX = 75
MAX_ONSCREEN_OBJECTS = 5
MIN_SPAWN_DISTANCE = 80
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.last_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _spawn_object(self):
        if len(self.objects) >= MAX_ONSCREEN_OBJECTS:
            return

        radius = 14
        min_x = radius
        max_x = WIDTH - radius
        best_x = random.randint(min_x, max_x)

        if self.last_spawn_x is not None:
            for _ in range(10):
                candidate_x = random.randint(min_x, max_x)
                if abs(candidate_x - self.last_spawn_x) >= MIN_SPAWN_DISTANCE:
                    best_x = candidate_x
                    break

        self.last_spawn_x = best_x
        self.objects.append(FallingObject(x=best_x, y=-radius, radius=radius, speed=3))

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.basket.move_left()
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.basket.move_right()
        if keys_pressed[pygame.K_SPACE]:
            self.basket.activate_boost()
        self.basket.clamp(WIDTH)

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()

    def update(self):
        if self.game_over:
            return

        self.basket.update()

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_object()
            self.frames_until_spawn = random.randint(SPAWN_INTERVAL_MIN, SPAWN_INTERVAL_MAX)

        for obj in self.objects:
            obj.update()

        basket_rect = self.basket.get_rect()
        survivors = []
        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
            else:
                survivors.append(obj)
        self.objects = survivors

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))

        if self.basket.is_boosted:
            seconds_left = self.basket.boost_timer // 60 + 1
            renderer.draw_text(surface, font, f"BOOST! ({seconds_left}s)", (10, 62), color=(255, 200, 50))
        elif self.basket.cooldown_timer > 0:
            seconds_cd = self.basket.cooldown_timer // 60 + 1
            renderer.draw_text(surface, font, f"Boost Cooldown ({seconds_cd}s)", (10, 62), color=(150, 150, 150))
        else:
            renderer.draw_text(surface, font, "SPACE: Speed Boost", (10, 62), color=(100, 220, 255))

        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")
