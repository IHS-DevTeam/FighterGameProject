import pygame
from pygame import mixer

mixer.init()
pygame.init()

from util.projectile import Projectile

ARROW_SIZE = 24
ARROW_SCALE = 5
'''
TODO: the arrow image is located higher then the arrow hitbox
'''
ARROW_OFFSET = [10, 21]
ARROW_DATA = [ARROW_SIZE, ARROW_SCALE, ARROW_OFFSET]

#musics
ARROW_fx = pygame.mixer.Sound("assets/audio/sword.wav")
ARROW_fx.set_volume(0.5)
ARROW_SHEET = pygame.image.load("assets/images/projectile/arrow/Arrow_Sprite.png").convert_alpha()

'''
last frame in "hit_stuff" state for the fireball projectile is blank
'''
ARROW_ANIMATION_STEPS = [2, 3]

class ARROW(Projectile):
  def __init__(self, cord, flip, target):
    
    super().__init__( cord, flip, ARROW_DATA, ARROW_SHEET, ARROW_ANIMATION_STEPS, ARROW_fx, target)