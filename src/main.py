import pygame
import sys
import random
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

arrow_path = resource_path('assets/sprites/arrow.png')
controls_path = resource_path('assets/sprites/controls.png')
player_path = resource_path('assets/sprites/player.png')
tom_path = resource_path('assets/sprites/tom.png')
music_path = resource_path('assets/sounds/music_1.mp3')
loser_sound_path = resource_path('assets/sounds/loser.ogg')

pygame.init()
pygame.mixer.init()

# Load sounds
loser_sound = pygame.mixer.Sound(loser_sound_path)
pygame.mixer.music.load(music_path)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
game_name = "Jack: The last warrior"
pygame.display.set_caption(game_name)

font = pygame.font.Font(None, 36)
pause_font = pygame.font.Font(None, 72)
menu_font = pygame.font.Font(None, 64)

clock = pygame.time.Clock()

# Game status
score = 0
paused = False
game_over = False
show_controls = False
in_main_menu = True

played_loser_sound = False

# Player settings
player_width = 50
player_height = 60
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5
fire_rate = 500
last_shot_time = 0

# Bullet settings
bullet_width = 15
bullet_height = 25
bullet_speed = 7
bullets = []

# Enemy settings
enemy_width = 50
enemy_height = 60
enemy_speed = 2
enemies = []

# Spawn an enemy every 2 seconds
enemy_timer = 0
enemy_spawn_time = 2000

# Collision detection function
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def reset_game():
    global score, bullets, enemies, player_x, game_over, show_controls, played_loser_sound
    score = 0
    bullets = []
    enemies = []
    player_x = screen_width // 2 - player_width // 2
    game_over = False
    show_controls = False
    played_loser_sound = False

def quit_game():
    pygame.quit()
    sys.exit()

# Function to display controls
def screen_show_control():
    screen.fill((255, 255, 255))
    
    controls = pygame.image.load(controls_path)
    
    screen.blit(controls, (0, 0))
    
    # Display instruction for returning to main menu
    return_text = font.render("Press ESC to Return to Main Menu", True, (0, 0, 0))
    return_rect = return_text.get_rect(center=(screen_width // 2, screen_height - 50))
    
    screen.blit(return_text, return_rect)
    
    pygame.display.flip()

# New function to display the main menu
def screen_main_menu():
    screen.fill((0, 0, 0))
    
    title_text = menu_font.render(game_name, True, (255, 255, 255))
    play_text = font.render("Press Enter to Play", True, (255, 255, 255))
    controls_text = font.render("Press C for Controls", True, (255, 255, 255))
    quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))
    version_text = font.render("v0.2.0", True, (255, 255, 255))
    
    # Positioning texts
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    play_rect = play_text.get_rect(center=(screen_width // 2, screen_height // 2))
    controls_rect = controls_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    version_rect = version_text.get_rect(bottomright=(screen_width - 10, screen_height - 10))
    
    # Blit texts to the screen
    screen.blit(title_text, title_rect)
    screen.blit(play_text, play_rect)
    screen.blit(controls_text, controls_rect)
    screen.blit(quit_text, quit_rect)
    screen.blit(version_text, version_rect)
    
    pygame.display.flip()


def screen_game_over():
    screen.fill((0, 0, 0))

    game_over_text = pause_font.render("GAME OVER", True, (255, 0, 0))
    restart_text = font.render("Press Enter to Restart or ESC to Quit", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()


def screen_pause():
    screen.fill((0, 0, 0))
    
    # Display the paused message
    pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(pause_text, pause_rect)
    
    # Display the instructions for key presses
    resume_text = font.render("Press Enter to Resume", True, (255, 255, 255))
    menu_text = font.render("Press ESC to Main Menu", True, (255, 255, 255))
    
    resume_rect = resume_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    
    screen.blit(resume_text, resume_rect)
    screen.blit(menu_text, menu_rect)
    
    pygame.display.flip()


player_image = pygame.image.load(player_path)
player_image = pygame.transform.scale(player_image, (player_width, player_height))

bullet_image = pygame.image.load(arrow_path)
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))

enemy_image = pygame.image.load(tom_path)
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type == pygame.KEYDOWN:
            if in_main_menu:
                if event.key == pygame.K_RETURN:  # Start the game
                    in_main_menu = False
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_c:  # Show controls
                    show_controls = True
                    in_main_menu = False
                elif event.key == pygame.K_ESCAPE:  # Quit the game
                    quit_game()
            elif show_controls:
                if event.key == pygame.K_ESCAPE:  # Return from controls
                    show_controls = False
                    in_main_menu = True
            elif game_over:
                if event.key == pygame.K_RETURN:  # Restart the game
                    reset_game()
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_ESCAPE:  # Quit the game
                    quit_game()
                    pygame.mixer.music.stop()
            elif paused:
                if event.key == pygame.K_RETURN:  # Resume the game
                    paused = False
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_ESCAPE:  # Go to the main menu
                    paused = False
                    in_main_menu = True
            else:
                if event.key == pygame.K_ESCAPE:  # Pause the game
                    paused = not paused
                    pygame.mixer.music.stop()
                if event.key == pygame.K_SPACE and not paused and not game_over:  # Fire bullet
                    current_time = pygame.time.get_ticks()
                    if current_time - last_shot_time > fire_rate:
                        bullet_x = player_x + player_width // 2 - bullet_width // 2
                        bullet_y = player_y
                        bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))
                        last_shot_time = current_time  # Update the last shot time

    # Main Menu Screen
    if in_main_menu:
        screen_main_menu()
        clock.tick(60)
        continue

    # Show controls screen
    if show_controls:
        screen_show_control()
        clock.tick(60)
        continue

    # Game over screen
    if game_over:
        if not played_loser_sound:
            loser_sound.play()
            played_loser_sound = True 
    
        screen_game_over()
        clock.tick(60)
        continue

    # Pause screen
    if paused:
        screen_pause()
        clock.tick(60)
        continue

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Update bullet positions
    for bullet in bullets:
        bullet.y -= bullet_speed
    bullets = [bullet for bullet in bullets if bullet.y > 0]

    # Spawn enemies
    current_time = pygame.time.get_ticks()
    if current_time - enemy_timer > enemy_spawn_time:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = -enemy_height
        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))
        enemy_timer = current_time

    # Update enemy positions
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y >= screen_height:
            enemies.remove(enemy)
            score -= 1

    # Check for collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_collision(bullet, enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

    # Check game over condition
    if score < 0:
        game_over = True

    # Drawing the game
    screen.fill((255, 255, 255))
    
    screen.blit(player_image, (player_x, player_y))

    for bullet in bullets:
        screen.blit(bullet_image, bullet.topleft)
    for enemy in enemies:
        screen.blit(enemy_image, enemy.topleft)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(screen_width // 2, 30))
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    clock.tick(60)