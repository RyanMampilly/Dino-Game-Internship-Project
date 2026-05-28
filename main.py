"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
@RyanMampilly (commit f54e5236c53873686a3f671b05fcdf57356d5cf3 and after)
"""

import pygame
from random import randint

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False

# Game state variables
gameloop_active = False # Rename of is_playing for clarity
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_START_SPEED = -20  # The speed at which the player jumps
player_gravity_speed = 0
score = 0
spawner = pygame.USEREVENT + 1
pygame.time.set_timer(spawner,randint(600,2000))
enemy_list = []
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)

# Initial screen
screen.fill("White")
title_surf  = game_font.render("EGG SPRINT!", False, "Black")
title_rect  = title_surf.get_rect(center=(400,50))

subtitle_surf  = pygame.font.Font(pygame.font.get_default_font(),20).render("Press <SPACE> or <MOUSE1> to start!", False, "Black")
subtitle_rect  = subtitle_surf.get_rect(center=(400,350))

player_surf = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_surf = pygame.transform.scale2x(player_surf)
player_rect = player_surf.get_rect(center=(400,200))

screen.blit(player_surf,player_rect)
screen.blit(title_surf,title_rect)
screen.blit(subtitle_surf,subtitle_rect)

pygame.display.update()

while not gameloop_active:
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
            gameloop_active = True
        elif event.type == pygame.QUIT:
            pygame.quit()


# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()

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

        elif gameloop_active:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                player_gravity_speed = JUMP_START_SPEED
            elif event.type == spawner:
                enemy_list.append(egg_surf.get_rect(bottomleft=(800, GROUND_Y)))
                pygame.time.set_timer(spawner,randint(600,2000))
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                gameloop_active = True
                egg_rect.left = 800
                score = 0 # Reset score

    if gameloop_active:
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
        for egg in enemy_list:
            egg.x -= 5
            if egg.right <= 0:
                enemy_list.remove(egg)
            screen.blit(egg_surf, egg)

        # Adjust player's vertical location then blit it
        player_gravity_speed += 1
        player_rect.y += player_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        # When player collides with enemy, game ends
        for egg in enemy_list:
            if egg.colliderect(player_rect):
                gameloop_active = False
                enemy_list.clear()


    # When is over, display game over message
    else:
        screen.fill("black")
        screen.blit(game_over_surf, game_over_rect)
        score_surf = game_font.render(f"SCORE: {score // 60}", False, "White") 
        screen.blit(score_surf, score_surf.get_rect(center=(400, 250)))
        
    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits loop to 60 FPS

pygame.quit()
