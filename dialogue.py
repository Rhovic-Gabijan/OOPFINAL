# dialogue.py
import pygame
from matrixrain import MatrixRainEffect
from game_world import enter_game_world

dialogue_lines = [
    "Welcome to the debug world!",
    "You're the only one who can fix the broken code.",
    "Complete the quests to restore order.",
    "Good luck, developer!"
]

def run_dialogue(screen):
    font = pygame.font.SysFont("arial", 28)
    clock = pygame.time.Clock()
    current_line = 0
    show_dialogue = True

    matrix = MatrixRainEffect(screen, font, font_size=20, rain_speed=9)

    screen_width, screen_height = screen.get_size()

    box_width = screen_width - 100
    box_height = 140
    box_x = 50
    box_y = screen_height - box_height - 50

    while show_dialogue:
        dt = clock.tick(60) / 1000
        matrix.update_and_draw(dt)

        # Draw dialogue box
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, (50, 50, 50), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)

        # Draw current dialogue line
        text = font.render(dialogue_lines[current_line], True, (255, 255, 255))
        screen.blit(text, (box_x + 20, box_y + 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_line += 1
                    if current_line >= len(dialogue_lines):
                        print("Running dialogue...")
                        return "game_world"

        pygame.display.flip()