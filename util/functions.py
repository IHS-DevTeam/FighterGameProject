import pygame
pygame.init()
from util.constants import * 
from util.image_loader import * 
'''
All "draw_XXX" functions should all take 'screen' as their first arguement
'''
#function for drawing start page
def draw_start_page(screen, title_img, start_img):
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
    
def draw_health_bar(screen, health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))
    
def draw_bg(screen):
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#function for drawing text
def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_single_toggle(screen, single_toggle_on, single_toggle_off, is_single_player):
    # toggle_width = 100 (desired width)

    if(is_single_player):
        screen.blit(single_toggle_on, (SCREEN_WIDTH // 2 - 50, 350))
    if(not is_single_player):
        screen.blit(single_toggle_off, (SCREEN_WIDTH // 2 - 50, 350))



#function for drawing character selection page
def draw_character_selection_page(screen, start_img, frame_img):
    screen.fill((0, 0, 0))

    start_width = 200  # desired width
    start_height = int(start_img.get_height() * (start_width / start_img.get_width()))
    start_img = pygame.transform.smoothscale(start_img, (start_width, start_height))
    screen.blit(start_img, (SCREEN_WIDTH // 2 - start_img.get_width() // 2, 450))

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


#make idle-ing animation for character selection page
def idle_animation(idle_sprite_sheet, animation_steps):
    idle_animation_list = []
    sheet_width, sheet_height = idle_sprite_sheet.get_size()
    frame_width = sheet_width // animation_steps
    for i in range(animation_steps):
        temp_img = idle_sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, sheet_height))
        idle_animation_list.append(temp_img)
    return idle_animation_list