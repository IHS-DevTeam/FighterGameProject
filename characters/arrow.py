import pygame
from pygame import mixer

mixer.init()
pygame.init()

from util.projectile import Projectile

FIRE_BALL_SIZE = 160
FIRE_BALL_SCALE = 1
FIRE_BALL_OFFSET = [72, 56]
FIRE_BALL_DATA = [FIRE_BALL_SIZE, FIRE_BALL_SCALE, FIRE_BALL_OFFSET]

#musics
fire_ball_fx = pygame.mixer.Sound("assets/audio/sword.mp3")
fire_ball_fx.set_volume(0.5)
FIRE_BALL_SHEET = pygame.image.load("assets/images/projectile/fire_ball.png").convert_alpha()

'''
last frame in "hit_stuff" state for the fireball projectile is blank
'''
FIRE_BALL_ANIMATION_STEPS = [4, 5]

class Fire_Ball(Projectile):
  def __init__(self, cord, flip, target):
    
    super().__init__( cord, flip, FIRE_BALL_DATA, FIRE_BALL_SHEET, FIRE_BALL_ANIMATION_STEPS, fire_ball_fx, target)