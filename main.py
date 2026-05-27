"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
@RyanMampilly (commit f54e5236c53873686a3f671b05fcdf57356d5cf3 and after)
"""

import pygame

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False

# Game state variables
program_active = False # Rename of is_playing for clarity
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_START_SPEED = -20  # The speed at which the player jumps
player_gravity_speed = 0
score = 0

# Initial screen
screen.fill("White")
player_surf = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_rect = player_surf.get_rect(center=(400,200))
screen.blit(player_surf,player_rect)
pygame.display.update()

while not program_active:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            program_active = True
        elif event.type == pygame.QUIT:
            pygame.quit()


# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)

score_surf = game_font.render("SCORE?", False, "Black")
score_rect = score_surf.get_rect(center=(400, 50))

game_over_surf = game_font.render("YOU LOSE! TRY AGAIN?", False, "White")
game_over_rect = game_over_surf.get_rect(center=(400,150))

# Load sprite assets
player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))

while running:
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif program_active:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                player_gravity_speed = JUMP_START_SPEED
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                program_active = True
                egg_rect.left = 800
                score = 0 # Reset score

    if program_active:
        screen.fill("purple")  # Wipe the screen

        # Update score
        score += 1
            # finer score updates every frame, 
            # but the in-game score will be the amount of seconds elapsed
        score_surf = game_font.render(f"{score // 60}", False, "Black") 
        score_rect = score_surf.get_rect(center=(400, 50)) # Re-center text

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        screen.blit(score_surf, score_rect)

        # Adjust egg's horizontal location then blit it
        egg_rect.x -= 5
        if egg_rect.right <= 0:
            egg_rect.left = 800
        screen.blit(egg_surf, egg_rect)

        # Adjust player's vertical location then blit it
        player_gravity_speed += 1
        player_rect.y += player_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        # When player collides with enemy, game ends
        if egg_rect.colliderect(player_rect):
            program_active = False

    # When is over, display game over message
    else:
        screen.fill("black")
        screen.blit(game_over_surf, game_over_rect)
        score_surf = game.font.render(f"SCORE: {score // 60}", False, "White") 
        screen.blit(score_surf, score_surf.get_rect(center=(400, 250)))
        
    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits loop to 60 FPS

pygame.quit()
