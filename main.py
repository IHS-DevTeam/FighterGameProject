import pygame
from pygame import mixer

mixer.init()
pygame.init()


from util.fighter import *
from util.constants import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
from util.functioins import *
from util.image_loader import *


#set framerate
clock = pygame.time.Clock()

pygame.display.set_caption("IHS Brawl")

last_count_update = pygame.time.get_ticks()






from characters.warrior import Warrior
from characters.wizzard import Wizard
from characters.boogieman import Boogie_Man
#create two instances of fighters
fighter_1 = Boogie_Man(1, FIGHTER_1_SPAWN_COORD, False, False)

fighter_2 = Wizard(2, FIGHTER_2_SPAWN_COORD, False, True)

#game loop
run = True
while run:
    clock.tick(FPS)

    if not game_started:
        draw_start_page(screen, title_img, start_img)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_img.get_rect(topleft=(SCREEN_WIDTH // 2 - start_img.get_width() // 2, 300)).collidepoint(mouse_pos):
                    character_selected = False

                #checks for character selection
                while not character_selected:
                    draw_character_selection_page(screen, start_img, frame_img)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            character_selected = True
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if start_img.get_rect(topleft=(SCREEN_WIDTH // 2 - start_img.get_width() // 2, 300)).collidepoint(mouse_pos):
                                game_started = True
                                intro_count = 3
                                character_selected = True
    else:
        #draw background
        draw_bg(screen)

        #show player stats
        draw_health_bar(screen, fighter_1.health, 20, 20)
        draw_health_bar(screen, fighter_2.health, 580, 20)
        draw_text(screen, "P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text(screen, "P2: " + str(score[1]), score_font, RED, 580, 60)

        #update countdown
        if intro_count <= 0:
            #move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            #display count timer
            draw_text(screen, str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            #update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        #update fighters
        fighter_1.update()
        fighter_2.update()

        #update coordinate for AIs
        fighter_1.set_opponent_position(fighter_2.get_position())
        fighter_2.set_opponent_position(fighter_1.get_position())

        #draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        #check for player defeat
        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            #display victory image
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Boogie_Man(1, FIGHTER_1_SPAWN_COORD, False, False)
                fighter_2 = Wizard(2, FIGHTER_2_SPAWN_COORD, True, False)
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

#exit pygame
pygame.quit()