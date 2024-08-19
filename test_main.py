import pygame
from pygame import mixer

mixer.init()
pygame.init()


from util.fighter import *
from util.constants import *
from util.projectile import * 


# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

from util.functions import *
from util.image_loader import *

from util.projectile_list import *


#set framerate
clock = pygame.time.Clock()

pygame.display.set_caption("IHS Brawl")

last_count_update = pygame.time.get_ticks()


from characters.warrior import Warrior
from characters.wizzard import Wizard
from characters.boogieman import Boogie_Man
from characters.fire_ball import * 

is_single_player = True


# Resize images once before the character selection loop
start_img = pygame.transform.smoothscale(start_img, (200, int(start_img.get_height() * (200 / start_img.get_width()))))
single_toggle_off = pygame.transform.smoothscale(single_toggle_off, (100, int(single_toggle_off.get_height() * (100 / single_toggle_off.get_width()))))
single_toggle_on = pygame.transform.smoothscale(single_toggle_on, (100, int(single_toggle_on.get_height() * (100 / single_toggle_on.get_width()))))


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
                character_selected = False

                #checks for character selection
                while not character_selected:
                    draw_character_selection_page(screen, start_img, frame_img)
                    draw_single_toggle(screen, single_toggle_on, single_toggle_off, is_single_player)
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            character_selected = True
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            
                            # Rect for start button
                            start_img_rect = start_img.get_rect(topleft=(SCREEN_WIDTH // 2 - start_img.get_width() // 2, 450))
                            # Rect for toggle button
                            single_toggle_rect = pygame.Rect(SCREEN_WIDTH // 2 - single_toggle_off.get_width() // 2, 350, single_toggle_off.get_width(), single_toggle_off.get_height())

                            if start_img_rect.collidepoint(mouse_pos):
                                # Start the game when start button is pressed
                                game_started = True
                                intro_count = 3
                                character_selected = True

                            elif single_toggle_rect.collidepoint(mouse_pos):
                                # Toggle single/multiplayer when toggle button is pressed
                                is_single_player = not is_single_player
                                draw_single_toggle(screen, single_toggle_on, single_toggle_off, is_single_player)
                        

                # Once character is selected and game starts, create two instances of fighters
                fighter_1 = Boogie_Man(1, FIGHTER_1_SPAWN_COORD, False, False)
                fighter_2 = Wizard(2, FIGHTER_2_SPAWN_COORD, False, is_single_player)
                # test_projectile = Fire_Ball((100,350), False, fighter_2)

                                
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
        
        '''
        TODO: finish the animation before the instance is removed
        '''
        if len(PROJECTILE_LIST) > 0:
            # print("Got shit")
            for i in range(0, len(PROJECTILE_LIST)):
                    current_projectile = PROJECTILE_LIST[i]
                  
                    current_projectile.update()
                    current_projectile.draw(screen)


               



        #update coordinate for AIs
        fighter_1.set_opponent_position(fighter_2.get_position())
        fighter_2.set_opponent_position(fighter_1.get_position())

        #draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        # test_projectile.draw(screen)

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
                fighter_2 = Wizard(2, FIGHTER_2_SPAWN_COORD, True, is_single_player)
                PROJECTILE_LIST = []
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

#exit pygame
pygame.quit()