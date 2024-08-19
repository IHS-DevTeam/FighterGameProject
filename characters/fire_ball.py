import pygame
from pygame import mixer

mixer.init()
pygame.init()

from util.projectile import Projectile

FIRE_BALL_SIZE = 160
FIRE_BALL_SCALE = 2
FIRE_BALL_OFFSET = [72, 56]
FIRE_BALL_DATA = [FIRE_BALL_SIZE, FIRE_BALL_SCALE, FIRE_BALL_OFFSET]

#musics
sword_fx = pygame.mixer.Sound("assets/audio/fire_ball.mp3")
sword_fx.set_volume(0.5)
FIRE_BALL_sheet = pygame.image.load("assets/images/boogie_man/Sprits/Boogie_Man.png").convert_alpha()

'''
last frame in "hit_stuff" state for the fireball projectile is blank
'''
FIRE_BALL_ANIMATION_STEPS = [4, 5]

class Fire_Ball(Projectile):
  def __init__(self, player, cord, flip, isAI):
    
    super().__init__(player, cord, False, FIRE_BALL_DATA, FIRE_BALL_sheet, FIRE_BALL_ANIMATION_STEPS, sword_fx, isAI)