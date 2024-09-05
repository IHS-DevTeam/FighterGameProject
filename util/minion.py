import pygame
from pygame import mixer
import random

mixer.init()
pygame.init()


class Minion():
  def __init__(self, opponent_x, opponent_y):
    self.x = opponent_x
    self.y = opponent_y
    self.rect = pygame.Rect((self.x, self.y, 40, 40))
    self.speed = 10
    self.attack_cooldown = 0
    self.lifespan = 100

  def attack(self, target):
    if self.attack_cooldown == 0:        
      #execute attack
      self.attacking = True
      attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):          
        target.health -= 10
        target.hit = True

  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED = self.speed
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    #can only perform other actions if not currently attacking
    if self.attacking == False and self.alive == True and round_over == False:
      x_diff = self.rect.x - self.opponent_x

      #AI control Logic
      if self.isAI == True:
        temp = random.random()
        if temp < 0.5:
          if x_diff >= 150:
            dx = -SPEED
            self.running = True
          if x_diff <= -150:
            dx = SPEED
            self.running = True
        elif temp < 0.52 and self.jump == False:
          self.vel_y = -30
          self.jump = True

    #apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y

    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #ensure minion face opponent
    if target.rect.centerx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True

    #apply attack cooldown
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    #update player position
    self.rect.x += dx
    self.rect.y += dy

    self.target = target

def update(self):
  print("whatup")

def main():    print("whatup")

if __name__ == '__main__':
  main()

