import pygame
import random
from player import Player
from enemy import Enemy


class GameWorld:
    def __init__(self, screen):
        print("Initializing GameWorld...")
        self.screen = screen

        # Load background
        self.background = pygame.image.load("my_game\\assets\\background\\pixil-layer-Background.png").convert()
        self.background = pygame.transform.scale(self.background, (1920, 1080))
        self.bg_rect = self.background.get_rect()
        self.camera_offset = pygame.Vector2(0, 0)

        # Initialize player and enemy
        self.player = Player(100, 300,
            ["my_game\\assets\\rightplayer\\0 (3).png", "my_game\\assets\\rightplayer\\1 (3).png", "my_game\\assets\\rightplayer\\2 (3).png", "my_game\\assets\\rightplayer\\3 (3).png"],
            ["my_game\\assets\\leftplayer\\0 (2).png", "my_game\\assets\\leftplayer\\1 (2).png", "my_game\\assets\\leftplayer\\2 (2).png", "my_game\\assets\\leftplayer\\3 (2).png"],
            ["my_game/assets/downplayer/0 (1).png", "my_game\\assets\\downplayer\\1 (1).png", "my_game\\assets\\downplayer\\2 (1).png", "my_game\\assets\\downplayer\\3 (1).png"],
            ["my_game\\assets\\upplayer\\0.png", "my_game\\assets\\upplayer\\1.png", "my_game\\assets\\upplayer\\2.png", "my_game\\assets\\upplayer\\3.png"]
        )
        self.enemy = Enemy(500, 300, [
            "my_game\\assets\\enemy1\\enemy1.png",
            "my_game\\assets\\enemy1\\enemy2.png",
            "my_game\\assets\\enemy1\\enemy3.png",
            "my_game\\assets\\enemy1\\enemy4.png"
        ])
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.player, self.enemy)
        print("GameWorld initialized with player and enemy.")

    def spawn_player(self):
        print("Spawning player at position (100, 300)...")
        self.player.rect.topleft = (100, 300)
        self.player.velocity = pygame.math.Vector2(0, 0)

    def spawn_enemy(self):
        print("Spawning enemy at position (500, 300)...")
        self.enemy.rect.topleft = (500, 300)

    def draw(self):
        # Update camera offset based on player position
        self.camera_offset.x = self.player.rect.centerx - self.screen.get_width() // 2
        self.camera_offset.y = self.player.rect.centery - self.screen.get_height() // 2

        # Clamp the camera offset to keep it inside background
        self.camera_offset.x = max(0, min(self.camera_offset.x, self.bg_rect.width - self.screen.get_width()))
        self.camera_offset.y = max(0, min(self.camera_offset.y, self.bg_rect.height - self.screen.get_height()))

        # Draw background
        self.screen.blit(self.background, (-self.camera_offset.x, -self.camera_offset.y))

        # Update and draw sprites relative to camera
        self.sprites.update()
        for sprite in self.sprites:
            offset_pos = sprite.rect.topleft - self.camera_offset
            self.screen.blit(sprite.image, offset_pos)

        pygame.display.flip()

    def check_collision(self):
        if pygame.sprite.collide_rect(self.player, self.enemy):
            print("Collision detected! Shake the screen and transition to battle.")
            return True
        return False

    def shake_screen(self, shakes=5, intensity=10, duration=50):
        """Shake the screen for a short time"""
        original_pos = self.screen.get_rect().topleft
        for _ in range(shakes):
            self.screen.get_rect().topleft = (original_pos[0] + random.randint(-intensity, intensity),
                                              original_pos[1] + random.randint(-intensity, intensity))
            pygame.time.delay(duration)
            self.screen.get_rect().topleft = original_pos
            pygame.time.delay(duration)

    def blackout_screen(self, duration=500):
        """Blackout the screen before transitioning to the battle scene"""
        black_surface = pygame.Surface(self.screen.get_size())
        black_surface.fill((0, 0, 0))
        self.screen.blit(black_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(duration)

    def white_fade_out(self, duration=1000, steps=30):
        """Fade from white to transparent over the screen"""
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((255, 255, 255))
        clock = pygame.time.Clock()

        for alpha in range(255, -1, -255 // steps):
            overlay.set_alpha(alpha)
            self.screen.blit(self.background, (-self.camera_offset.x, -self.camera_offset.y))
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            clock.tick(steps / (duration / 1000))

    def game_loop(self):
        print("Starting game loop...")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Window closed by user.")
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_w:
                        self.player.velocity.y = -self.player.speed
                    elif event.key == pygame.K_s:
                        self.player.velocity.y = self.player.speed
                    elif event.key == pygame.K_a:
                        self.player.velocity.x = -self.player.speed
                    elif event.key == pygame.K_d:
                        self.player.velocity.x = self.player.speed
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_w, pygame.K_s]:
                        self.player.velocity.y = 0
                    if event.key in [pygame.K_a, pygame.K_d]:
                        self.player.velocity.x = 0

            # Update player movement and prevent going out of bounds
            self.player.rect.clamp_ip(self.bg_rect)

            self.draw()

            if self.check_collision():
                self.shake_screen()
                self.blackout_screen()
                running = False

            pygame.time.delay(30)

        print("Exiting game loop...")


def enter_game_world(screen):
    print("Entering game world...")
    game_world = GameWorld(screen)

    # White fade out animation before spawning
    game_world.white_fade_out()

    game_world.spawn_player()
    game_world.spawn_enemy()
    game_world.game_loop()
