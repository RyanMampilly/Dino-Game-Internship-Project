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
lives = 3
lives_bar = []

def object_movement(object_surf, object_list):
    for obj in object_list:
        obj.x -= 5
        if obj.right <= 0:
            object_list.remove(obj)
        screen.blit(object_surf, obj)

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
sky_surf = pygame.image.load("graphics/level/sky.png").convert()
ground_surf = pygame.image.load("graphics/level/ground.png").convert()

score_surf = game_font.render("SCORE?", False, "Black")
score_rect = score_surf.get_rect(center=(400, 50))

game_over_surf = game_font.render("YOU LOSE! TRY AGAIN?", False, "White")
game_over_rect = game_over_surf.get_rect(center=(400,150))

# Load sprite assets
player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))

heart_f_surf = pygame.image.load("graphics/status/heart_full.png").convert_alpha()
heart_b_surf = pygame.image.load("graphics/status/heart_broken.png").convert_alpha()
for i in range(3):
    lives_bar.append(heart_f_surf)

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

        # Scroll the sky to give a feeling of running instead of the eggs coming to you
        sky_surf.scroll(-1,0,pygame.SCROLL_REPEAT)

        # Blit the level assets
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND_Y))
        screen.blit(score_surf, score_rect)

        # Adjust egg's horizontal location then blit it
        object_movement(egg_surf, enemy_list)

        # Adjust player's vertical location then blit it
        player_gravity_speed += 1
        player_rect.y += player_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        # Blit hearts bar
        for i in range(len(lives_bar)): screen.blit(lives_bar[i], (10+i*50,10))

        # When player collides with enemy, game ends
        for egg in enemy_list:
            if egg.colliderect(player_rect):
                lives -= 1
                lives_bar[lives] = heart_b_surf
                enemy_list.remove(egg)
        if lives <= 0:
            gameloop_active = False
            # Game Over animation
            player_gravity_speed = -10
            player_surf = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
            while player_rect.bottom < 500:
                player_gravity_speed += 0.5
                player_rect.y += player_gravity_speed

                screen.fill("purple")
                screen.blit(sky_surf, (0, 0))
                screen.blit(ground_surf, (0, GROUND_Y))
                screen.blit(score_surf, score_rect)
                for i in range(len(lives_bar)): screen.blit(lives_bar[i], (10+i*50,10))
                for egg in enemy_list: screen.blit(egg_surf, egg)
                screen.blit(player_surf, player_rect)

                pygame.display.update()
                clock.tick(60)

            lives = 3
            player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
            lives_bar = [heart_f_surf for i in lives_bar]
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
