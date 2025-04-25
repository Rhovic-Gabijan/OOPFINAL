# matrix_rain.py
import pygame
import random

class MatrixRainEffect:
    def __init__(self, screen, font, font_size=20, rain_speed=9):
        self.screen = screen
        self.font = font
        self.font_size = font_size
        self.rain_speed = rain_speed
        self.width, self.height = screen.get_size()
        self.chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*"
        self.columns = self.width // self.font_size
        self.drops = [random.uniform(0, self.height // self.font_size) for _ in range(self.columns)]
        self.last_rows = [-1] * self.columns
        self.fade_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
    
    def update_and_draw(self, dt):
        self.fade_surface.fill((0, 0, 0, 13))
        self.screen.blit(self.fade_surface, (0, 0))

        for i in range(self.columns):
            current_row = int(self.drops[i])

            if current_row != self.last_rows[i]:
                x = i * self.font_size
                y = current_row * self.font_size

                if y < self.height:
                    char = random.choice(self.chars)
                    char_surface = self.font.render(char, True, (0, 255, 0))
                    self.screen.blit(char_surface, (x, y))
                    self.last_rows[i] = current_row

            self.drops[i] += self.rain_speed * dt

            if self.drops[i] * self.font_size > self.height and random.random() > 0.975:
                self.drops[i] = 0
                self.last_rows[i] = -1