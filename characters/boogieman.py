import pygame
from pygame import mixer

mixer.init()
pygame.init()

from util.fighter import Fighter

WARRIOR_SIZE = 160
WARRIOR_SCALE = 2
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

#musics
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
warrior_sheet = pygame.image.load("assets/images/boogie_man/Sprits/Boogie_Man.png").convert_alpha()

WARRIOR_ANIMATION_STEPS = [4, 4, 1, 3, 3, 3, 3]
class Boogie_Man(Fighter):
  def __init__(self, player, cord, flip):
    Spawn_X, Spawn_Y = cord
    super().__init__(player, Spawn_X, Spawn_Y, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)