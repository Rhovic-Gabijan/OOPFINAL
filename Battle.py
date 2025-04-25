import pygame
import sys
import random

def show_outro(screen, font, WIDTH, HEIGHT):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))  # Change to black background
    outro_font = pygame.font.SysFont('arial', 64)
    text = outro_font.render("To be continued...", True, (255, 255, 255))  # White text on black

    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(fade_surface, (0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(50)

    pygame.time.delay(5000)  # Wait 5 seconds after fade-in
    pygame.quit()
    sys.exit()

def enter_battle(screen):
    WIDTH, HEIGHT = 1280, 720
    pygame.display.set_caption("Pyth-on-Bug")

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (50, 205, 50)
    BLACK = (0, 0, 0)
    LIGHT_GRAY = (200, 200, 200)
    SELECTED_COLOR = (173, 216, 230)

    font = pygame.font.SysFont('arial', 36)
    small_font = pygame.font.SysFont('arial', 24)

    player_imgs = [
        pygame.transform.scale(pygame.image.load('my_game/assets/Bigger_Player/0 (4).png'), (120, 120)),
        pygame.transform.scale(pygame.image.load('my_game/assets/Bigger_Player/2 (4).png'), (120, 120))
    ]

    enemy_imgs = [
        pygame.transform.scale(pygame.image.load(f'my_game/assets/enemy1/enemy{i}.png'), (120, 120))
        for i in range(1, 5)
    ]

    player_hp, enemy_hp, max_hp = 100, 100, 100
    battle_over = False

    player_frame, enemy_frame = 0, 0
    frame_counter = 0

    challenges = [
        {
            "buggy": "pritn('Hello World')",
            "choices": ["print('Hello World')", "prnt('Hello World')", "echo('Hello World')", "printf('Hello World')"],
            "answer": 0
        },
        {
            "buggy": "for  in range(5):",
            "choices": ["for i in range(5):", "for in i range(5):", "loop i in range(5):", "for i range(5)"],
            "answer": 0
        },
        {
            "buggy": "if x = 10:",
            "choices": ["if x == 10:", "if x = 10", "if x === 10:", "if (x == 10)"],
            "answer": 0
        },
        {
            "buggy": "def greet print('Hi')",
            "choices": ["def greet(): print('Hi')", "greet() print('Hi')", "func greet() print('Hi')", "def greet print()"],
            "answer": 0
        },
        {
            "buggy": "while True print('Looping')",
            "choices": ["while True: print('Looping')", "while True {print('Looping')}", "while True >> print('Looping')", "loop True print('Looping')"],
            "answer": 0
        },
    ]

    current_challenge = random.choice(challenges)
    selected_answer = None

    def draw_health_bar(x, y, hp):
        bar_width = 200
        bar_height = 20
        fill = (hp / max_hp) * bar_width
        pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (x, y, fill, bar_height))

    def draw_quiz():
        question = font.render("Fix the buggy code! Choose the correct answer.", True, BLACK)
        buggy = font.render("Buggy: " + current_challenge["buggy"], True, BLACK)
        screen.blit(question, (WIDTH // 2 - question.get_width() // 2, 160))
        screen.blit(buggy, (WIDTH // 2 - buggy.get_width() // 2, 220))

        for i, choice in enumerate(current_challenge["choices"]):
            label = chr(65 + i) + ") " + choice
            y_offset = 300 + i * 60
            box_rect = pygame.Rect(WIDTH // 2 - 200, y_offset, 400, 50)

            if selected_answer == i:
                pygame.draw.rect(screen, SELECTED_COLOR, box_rect)
            pygame.draw.rect(screen, BLACK, box_rect, 3)
            text = small_font.render(label, True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset + 10))

    clock = pygame.time.Clock()
    while True:
        screen.fill((150, 220, 255))

        frame_counter += 1
        if frame_counter % 20 == 0:
            player_frame = (player_frame + 1) % len(player_imgs)
            enemy_frame = (enemy_frame + 1) % len(enemy_imgs)

        screen.blit(player_imgs[player_frame], (100, 250))
        screen.blit(enemy_imgs[enemy_frame], (550, 50))

        draw_health_bar(100, 220, player_hp)
        draw_health_bar(550, 20, enemy_hp)

        if not battle_over:
            draw_quiz()
        else:
            if enemy_hp <= 0:
                result_text = font.render("You Win!", True, BLACK)
                screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 500))
                pygame.display.update()
                pygame.time.delay(1000)
                show_outro(screen, font, WIDTH, HEIGHT)
                return  # Exit battle scene
            else:
                result_text = font.render("You Lose!", True, BLACK)
                screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for i in range(4):
                    y_offset = 300 + i * 60
                    box_rect = pygame.Rect(WIDTH // 2 - 200, y_offset, 400, 50)
                    if box_rect.collidepoint(pos):
                        selected_answer = i
                        if selected_answer == current_challenge["answer"]:
                            damage = random.randint(15, 25)
                            enemy_hp = max(0, enemy_hp - damage)
                            print(f"Correct! Enemy HP: {enemy_hp}")
                        else:
                            damage = random.randint(10, 20)
                            player_hp = max(0, player_hp - damage)
                            print(f"Wrong! Player HP: {player_hp}")
                        current_challenge = random.choice(challenges)
                        selected_answer = None

        if enemy_hp <= 0 or player_hp <= 0:
            battle_over = True

        pygame.display.update()
        clock.tick(60)
