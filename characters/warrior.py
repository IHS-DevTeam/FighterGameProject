import pygame
from pygame import mixer

mixer.init()
pygame.init()

from fighter import Fighter

WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

#musics
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()

WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
class Warrior(Fighter):
  def __init__(self, player, x, y, flip):
    super().__init__(player, x, y, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)