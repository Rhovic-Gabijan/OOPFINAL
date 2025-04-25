import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.images = [pygame.image.load(img) for img in images]
        self.image = self.images[0]  # Default enemy image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.frame_index = 0
        self.frame_delay = 10  # Higher = slower animation
        self.frame_counter = 0

    def update(self):
        """Update the enemy animation"""
        self.animate()

    def animate(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.image = self.images[self.frame_index]
            self.frame_counter = 0
