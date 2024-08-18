import pygame
from pygame import mixer
import random

mixer.init()
pygame.init()


class Projectile():
    def __init__(self, cord, data, sprite_sheet, animation_steps, sound):
        self.spawn_x, self.spawn_y = cord 
        self.state = {
            "flying":       0,
            "hit_enemy":    1
        }
        self.image_scale = data[1]
        self.offset = data[2]
