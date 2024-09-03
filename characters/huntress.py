import pygame
from pygame import mixer

mixer.init()
pygame.init()

from util.fighter import Fighter

HUNTRESS_SIZE = 100
HUNTRESS_SCALE = 4
HUNTRESS_OFFSET = [72, 56]
HUNTRESS_DATA = [HUNTRESS_SIZE, HUNTRESS_SCALE, HUNTRESS_OFFSET]

#musics
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
huntress_sheet = pygame.image.load("assets/images/huntress/Sprites/huntress.png").convert_alpha()

HUNTRESS_ANIMATION_STEPS = [10, 8, 2, 6, 0, 3, 10]
class Huntress(Fighter):
  def __init__(self, player, cord, flip, isAI):
    
    super().__init__(player, cord, flip, HUNTRESS_DATA, huntress_sheet, HUNTRESS_ANIMATION_STEPS, sword_fx, isAI)