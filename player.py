import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, right_images, left_images, down_images, up_images):
        super().__init__()

        self.image = pygame.image.load(right_images[0])  # Default facing right
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 3  # You can reduce this for slower movement

        # Load animation frames
        self.right_images = [pygame.image.load(img) for img in right_images]
        self.left_images = [pygame.image.load(img) for img in left_images]
        self.down_images = [pygame.image.load(img) for img in down_images]
        self.up_images = [pygame.image.load(img) for img in up_images]

        self.direction = "right"
        self.frame_index = 0
        self.frame_delay = 8  # Higher = slower animation
        self.frame_counter = 0

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.velocity.x > 0:
            self.direction = "right"
        elif self.velocity.x < 0:
            self.direction = "left"
        elif self.velocity.y > 0:
            self.direction = "down"
        elif self.velocity.y < 0:
            self.direction = "up"

        # Animate based on direction
        if self.direction == "right":
            self.animate(self.right_images)
        elif self.direction == "left":
            self.animate(self.left_images)
        elif self.direction == "down":
            self.animate(self.down_images)
        elif self.direction == "up":
            self.animate(self.up_images)

    def animate(self, images):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(images)
            self.image = images[self.frame_index]
            self.frame_counter = 0
