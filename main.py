import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("IHS Brawl")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
game_started = False

#define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

#load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

#load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#load start page images
start_img = pygame.image.load("assets/images/Start Page/start.png").convert_alpha()
title_img = pygame.image.load("assets/images/Start Page/title.png").convert_alpha()
frame_img = pygame.image.load("assets/images/Selection Page/frame.png").convert_alpha()

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

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

#function for drawing character selection page
def draw_character_selection_page(start_img, frame_img):
    screen.fill((0, 0, 0))

    start_width = 200  # desired width
    start_height = int(start_img.get_height() * (start_width / start_img.get_width()))
    start_img = pygame.transform.smoothscale(start_img, (start_width, start_height))
    screen.blit(start_img, (SCREEN_WIDTH // 2 - start_img.get_width() // 2, 400))

    frame_width = 200  # desired width
    frame_height = int(frame_img.get_height() * (frame_width / frame_img.get_width()))
    frame_img = pygame.transform.smoothscale(frame_img, (frame_width, frame_height))
    screen.blit(frame_img, (SCREEN_WIDTH // 3 - frame_img.get_width() // 2, 100))
    screen.blit(frame_img, (2 * SCREEN_WIDTH // 3 - frame_img.get_width() // 2, 100))

    warrior_idle_sheet = pygame.image.load("assets/images/warrior/Sprites/idle.png").convert_alpha()
    warrior_idle_frames = idle_animation(warrior_idle_sheet, 10)

    wizard_idle_sheet = pygame.image.load("assets/images/wizard/Sprites/idle.png").convert_alpha()
    wizard_idle_frames = idle_animation(wizard_idle_sheet, 8)

    # Draw idle animations for characters
    frame_rate = 10  # Frames per second for animation
    animation_time = pygame.time.get_ticks() // frame_rate
    warrior_frame_index = (animation_time // frame_rate) % len(warrior_idle_frames)
    wizard_frame_index = (animation_time // frame_rate) % len(wizard_idle_frames)

    # Blit the idle frames for both characters
    warrior_frame = warrior_idle_frames[warrior_frame_index]
    wizard_frame = wizard_idle_frames[wizard_frame_index]

    # Double the size of the idle frames
    warrior_frame = pygame.transform.scale(warrior_frame, (warrior_frame.get_width() * 2.5, warrior_frame.get_height() * 2.5))
    wizard_frame = pygame.transform.scale(wizard_frame, (wizard_frame.get_width() * 2, wizard_frame.get_height() * 2))

    # Draw the frames on the screen
    screen.blit(warrior_frame, (SCREEN_WIDTH // 3 - warrior_frame.get_width() // 2, 30))
    screen.blit(wizard_frame, (2 * SCREEN_WIDTH // 3 - wizard_frame.get_width() // 2, -50))

    pygame.display.update()

#make idle-ing animation for character selection page
def idle_animation(idle_sprite_sheet, animation_steps):
    idle_animation_list = []
    sheet_width, sheet_height = idle_sprite_sheet.get_size()
    frame_width = sheet_width // animation_steps
    for i in range(animation_steps):
        temp_img = idle_sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, sheet_height))
        idle_animation_list.append(temp_img)
    return idle_animation_list

#create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
# fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

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
                    draw_character_selection_page(start_img, frame_img)
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
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

        #update countdown
        if intro_count <= 0:
            #move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            #display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
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
                fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

#exit pygame
pygame.quit()