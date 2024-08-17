import pygame
pygame.init()

#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

#load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#load start and character selection page images
start_img = pygame.image.load("assets/images/Start Page/start.png").convert_alpha()
title_img = pygame.image.load("assets/images/Start Page/title.png").convert_alpha()
frame_img = pygame.image.load("assets/images/Selection Page/frame.png").convert_alpha()
single_toggle_off = pygame.image.load("assets/images/Selection Page/single_off.png").convert_alpha()
single_toggle_on = pygame.image.load("assets/images/Selection Page/single_on.png").convert_alpha()


#load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)



#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

