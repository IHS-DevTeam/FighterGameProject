import pygame
from pygame import mixer

mixer.init()
pygame.init()

from util.fighter import Fighter
from util.minion import Minion

from util.projectile_list import *

from characters.arrow import *
HUNTRESS_SIZE = 100
HUNTRESS_SCALE = 4.5
HUNTRESS_OFFSET = [43, 31]
HUNTRESS_DATA = [HUNTRESS_SIZE, HUNTRESS_SCALE, HUNTRESS_OFFSET]

#musics
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
huntress_sheet = pygame.image.load("assets/images/huntress/Sprites/huntress.png").convert_alpha()

HUNTRESS_ANIMATION_STEPS = [10, 8, 2, 6, 2, 3, 10]
class Huntress(Fighter):
  def __init__(self, player, cord, flip, isAI):
    super().__init__(player, cord, flip, HUNTRESS_DATA, huntress_sheet, HUNTRESS_ANIMATION_STEPS, sword_fx, isAI)
    self.speed = 17
    self.health = 70
    self.is_there_minion = False
    self.minion = None  # Initialize minion as None

  def attack(self, target):
      if self.attack_cooldown == 0:
        # Execute attack
          self.attacking = True
          self.attack_sound.play()
          attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
          if self.get_attack_type() == 2:
              if attacking_rect.colliderect(target.rect):
                  self.summon(self.opponent_x, self.opponent_y)
          elif self.get_attack_type() == 1:
              current_projectile = ARROW(self.get_center(), self.get_fliped(), target)
              PROJECTILE_LIST.append(current_projectile)

  # Handle animation updates
  def update(self):
    Fighter.update(self)
    if self.is_there_minion:
      print("DevUp")
      # Update the minion if it exists
      if self.minion:
        self.minion.update()

  def summon(self, opponent_x, opponent_y):
      if self.attack_cooldown == 0 and not self.is_there_minion:
        self.is_there_minion = True
        # Summon minion and store it as an attribute
        self.minion = Minion(opponent_x, opponent_y)