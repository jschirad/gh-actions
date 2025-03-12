"""
Snake Game using Pygame
"""

import random
import time
import pygame

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

def init_pygame():
    """
    Initialize pygame and set up the display
    
    Returns:
        tuple: screen, font, and clock objects
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    font = pygame.font.SysFont(None, 35)
    clock = pygame.time.Clock()
    return screen, font, clock

def init_game():
    """
    Initialize game variables
    
    Returns:
        tuple: snake, snake_dir, food, score, and start_time
    """
    # Snake setup
    snake = [(100, 100), (90, 100), (80, 100)]
    snake_dir = (GRID_SIZE, 0)
    
    # Food setup
    food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
    
    # Score
    score = 0
    
    # Start time
    start_time = time.time()
    
    return snake, snake_dir, food, score, start_time

def draw_score_and_time(screen, font, score, elapsed):
    """
    Draw the score and elapsed time on the screen.
    
    Args:
        screen: The pygame display surface
        font: The pygame font object
        score (int): The current score.
        elapsed (float): The elapsed time in seconds.
    """
    score_text = font.render(f" Score: {score}", True, WHITE)
    time_text = font.render(f" Time: {int(elapsed)}s", True, WHITE)
    
    # Create a transparent surface
    info_surface = pygame.Surface((max(score_text.get_width(), time_text.get_width()), score_text.get_height() + time_text.get_height()), pygame.SRCALPHA)
    info_surface.fill((0, 0, 0, 128))  # Fill with black color and 50% transparency
    
    # Blit the score and time text onto the transparent surface
    info_surface.blit(score_text, (0, 0))
    info_surface.blit(time_text, (0, score_text.get_height()))
    
    # Blit the transparent surface onto the main screen
    screen.blit(info_surface, [0, 0])

def show_game_over(screen, font, score):
    """
    Display the game over screen with the final score.
    
    Args:
        screen: The pygame display surface
        font: The pygame font object
        score (int): The final score.
    """
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    
    # Create a transparent surface
    game_over_surface = pygame.Surface((max(game_over_text.get_width(), score_text.get_width()), game_over_text.get_height() + score_text.get_height()), pygame.SRCALPHA)
    game_over_surface.fill((0, 0, 0, 128))  # Fill with black color and 50% transparency
    
    # Blit the game over and score text onto the transparent surface
    game_over_surface.blit(game_over_text, (0, 0))
    game_over_surface.blit(score_text, (0, game_over_text.get_height()))
    
    # Blit the transparent surface onto the main screen
    screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - game_over_surface.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)  # Display the game over screen for 3 seconds

def run_game(screen, font, clock):
    """
    Run the main game loop
    
    Args:
        screen: The pygame display surface
        font: The pygame font object
        clock: The pygame clock object
        
    Returns:
        int: The final score
    """
    snake, snake_dir, food, score, start_time = init_game()
    
    # Game loop
    running = True
    while running:
        screen.fill(BLACK)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, GRID_SIZE):
                    snake_dir = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -GRID_SIZE):
                    snake_dir = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (GRID_SIZE, 0):
                    snake_dir = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-GRID_SIZE, 0):
                    snake_dir = (GRID_SIZE, 0)
        
        # Move the snake
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        
        # Check collisions
        if (new_head in snake or
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            running = False
        
        # Add new head
        snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == food:
            score += 1
            food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                    random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
        else:
            snake.pop()
        
        # Draw snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        
        # Draw food
        pygame.draw.rect(screen, YELLOW, (food[0], food[1], GRID_SIZE, GRID_SIZE))
        
        # Draw Score and time
        elapsed_time = time.time() - start_time
        draw_score_and_time(screen, font, score, elapsed_time)
        
        # Refresh display
        pygame.display.flip()
        clock.tick(10)
    
    # Show game over screen before returning
    show_game_over(screen, font, score)
    return score

def main():
    """
    Initialize pygame, run the game, and cleanup afterward
    
    Returns:
        int: The final score
    """
    # Initialize pygame and game components
    screen, font, clock = init_pygame()
    
    # Run the main game
    score = run_game(screen, font, clock)
    
    # Cleanup and quit
    pygame.quit()
    
    return score

if __name__ == "__main__":
    main()