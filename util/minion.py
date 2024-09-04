import pygame
from pygame import mixer
import random

mixer.init()
pygame.init()


class minion():
  def __init__(self, player, cord, flip, data, sprite_sheet, animation_steps, sound):
    print("DevUp")