import pygame
import sys
from menu import show_menu
from dialogue import run_dialogue
from game_world import enter_game_world
from Battle import enter_battle
    
def main():
    pygame.init()
    pygame.font.init()  # Initialize the font module explicitly

    w_width, w_height = 1280, 720
    screen = pygame.display.set_mode((w_width, w_height))
    pygame.display.set_caption("OOP Final Project")
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BOX_COLOR = (50, 50, 50)
    TEXT_COLOR = (255, 255, 255)
    WIDTH, HEIGHT = 800, 600

    current_state = "menu"
    running = True

    while running:
        if current_state == "menu":
            result = show_menu(screen)
            if result == "quit":
                running = False
            else:       
                current_state = result

        elif current_state == "dialogue":
            result = run_dialogue(screen)
            if result == "quit":
                running = False
            else:
                current_state = result

        elif current_state == "game_world":
            result = enter_game_world(screen)
            if result == "quit":
                running = False
            else:
                current_state = result

        else:
            current_state == 'enter_battle'
            result = enter_battle(screen)
            if result == 'quit':
                running = False
            else:
                current_state = result

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()