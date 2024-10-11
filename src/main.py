import pygame
import sys
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("A shooter Game")

font = pygame.font.Font(None, 36)
pause_font = pygame.font.Font(None, 72)

clock = pygame.time.Clock()

# Game status
score = 0
paused = False
game_over = False

# Player settings
player_width = 50
player_height = 60
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Bullet settings
bullet_width = 5
bullet_height = 10
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

# Function to reset the game when restarting
def reset_game():
  global score, bullets, enemies, player_x, game_over
  score = 0
  bullets = []
  enemies = []
  player_x = screen_width // 2 - player_width // 2
  game_over = False

def quit_game():
  pygame.quit()
  sys.exit()

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      quit_game()
    if event.type == pygame.KEYDOWN:
      if game_over:
        if event.key == pygame.K_RETURN:  # Press Enter to restart
          reset_game()
        elif event.key == pygame.K_ESCAPE:  # Press ESC to quit
          quit_game()
      if event.key == pygame.K_ESCAPE and not game_over:
        paused = not paused
      if event.key == pygame.K_SPACE and not paused and not game_over:
        bullet_x = player_x + player_width // 2 - bullet_width // 2
        bullet_y = player_y
        bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))

  # If the game is in Game Over state, show the Game Over screen
  if game_over:
    screen.fill((0, 0, 0))
    
    game_over_text = pause_font.render("GAME OVER", True, (255, 0, 0))
    restart_text = font.render("Press Enter to Restart or ESC to Quit", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)
    continue

  if paused:
    screen.fill((0, 0, 0))
    
    pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
    pause_rect = pause_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(pause_text, pause_rect)

    pygame.display.flip()
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
  # Remove bullets outside the screen
  bullets = [bullet for bullet in bullets if bullet.y > 0]

  # Update enemy positions and spawn new ones
  current_time = pygame.time.get_ticks()
  if current_time - enemy_timer > enemy_spawn_time:
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = -enemy_height
    enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))
    enemy_timer = current_time

  # Update enemy positions
  for enemy in enemies[:]:
    enemy.y += enemy_speed

    # Check if the enemy reached the bottom of the screen
    if enemy.y >= screen_height:
      enemies.remove(enemy)
      score -= 1  # Decrement score when enemy passes the screen

  # Check for collisions
  for bullet in bullets[:]:
    for enemy in enemies[:]:
      if check_collision(bullet, enemy):
        bullets.remove(bullet)
        enemies.remove(enemy)
        score += 1
        break

  # Check if score is below 0 to trigger Game Over
  if score < 0:
    game_over = True

  screen.fill((0, 0, 0))

  # Draw the player
  pygame.draw.rect(screen, (0, 128, 255), (player_x, player_y, player_width, player_height))

  # Draw bullets
  for bullet in bullets:
    pygame.draw.rect(screen, (255, 255, 255), bullet)

  # Draw enemies
  for enemy in enemies:
    pygame.draw.rect(screen, (255, 0, 0), enemy)

  # Render the score text
  score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
  score_rect = score_text.get_rect(center=(screen_width // 2, 30))  # Centered at the top
  screen.blit(score_text, score_rect)  # Draw the text on the screen

  pygame.display.flip()
  
  clock.tick(60)
