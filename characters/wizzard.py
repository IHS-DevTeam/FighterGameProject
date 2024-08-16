import pygame
from pygame import mixer

mixer.init()
pygame.init()

from fighter import Fighter

WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]


magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#load spritesheets

wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

#define number of steps in each animation

WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]


class Wizard(Fighter):
  def __init__(self, player, x, y, flip):
    super().__init__(player, x, y, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)