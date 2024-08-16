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


#define game variables

last_count_update = pygame.time.get_ticks()

#function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#function for drawing start page
def draw_start_page(title_img, start_img):
    screen.fill((0, 0, 0))
    # Scale down the title image and blit
    title_width = 400  # desired width
    title_height = int(title_img.get_height() * (title_width / title_img.get_width()))
    title_img = pygame.transform.smoothscale(title_img, (title_width, title_height))
    screen.blit(title_img, (SCREEN_WIDTH // 2 - title_img.get_width() // 2, 50))

    start_width = 400  # desired width
    start_height = int(start_img.get_height() * (start_width / start_img.get_width()))
    start_img = pygame.transform.smoothscale(start_img, (start_width, start_height))
    screen.blit(start_img, (SCREEN_WIDTH // 2 - start_img.get_width() // 2, 300))




from characters.warrior import Warrior
from characters.wizzard import Wizard
#create two instances of fighters
# fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx) -> Simplified with subclass
fighter_1 = Warrior(1, 200, 310, False)
fighter_2 = Wizard(2, 700, 310, True)
# fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx) -> Simplified with subclass

#game loop
run = True
while run:
    clock.tick(FPS)

    if not game_started:
        draw_start_page(title_img, start_img)
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
        draw_bg()

        #show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
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
                fighter_1 = Warrior(1, 200, 310, False)
                fighter_2 = Wizard(2, 700, 310, True)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

#exit pygame
pygame.quit()