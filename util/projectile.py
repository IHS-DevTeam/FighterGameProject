import pygame
from pygame import mixer
from util.constants import *
mixer.init()
pygame.init()
'''
There's a bug for this class.
Firstly:
    when (the projectile hit an enemy) and (destruct animation finished)
        -> the animation will freeze on a blank image
Secondly:
    the fozen blank image will remain on the screen even if the second round starts
'''
class Projectile():
    def __init__(self, cord, flip, data, sprite_sheet, animation_steps, sound, target):
        self.spawn_x, self.spawn_y = cord 
        self.size = data[0]
        self.image_scale = data[1]
        self.flip = flip
        self.state = {
            "flying": 0,
            "hit_stuff": 1
        }
        self.action = self.state["flying"]
        self.frame_index = 0
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.hit_stuff = False
        self.rect = pygame.Rect((self.spawn_x, self.spawn_y, 30, 30))
        self.offset = data[2]
        self.destruct_sound = sound
        self.vel_y = 0
        self.target = target

        self.ready_to_be_removed = False
        self.do_damage = True

    def load_images(self, sprite_sheet, animation_steps):
        # Extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def update_action(self, new_action):
        # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def move(self, screen_width, screen_height, target):
        SPEED = 50
        dx = 10

        if self.flip:
            dx *= -1

        dy = 0
        GRAVITY = 0

        self.vel_y += GRAVITY
        dy += self.vel_y

        attacking_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        if attacking_rect.colliderect(target.rect):
            self.update_action(self.state["hit_stuff"])
            self.hit_stuff = True
            if self.do_damage:
                target.health -= 10
                target.hit = True
                self.destruct_sound.play()
                self.do_damage = False
            
            dx = 0
            dy = 0
        else:
            if self.rect.left + dx < 0:
                dx = -self.rect.left
                self.update_action(self.state["hit_stuff"])
                self.hit_stuff = True
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
                self.update_action(self.state["hit_stuff"])
                self.hit_stuff = True
            if self.rect.bottom + dy > screen_height - 110:
                self.vel_y = 0
                dy = screen_height - 110 - self.rect.bottom
                self.update_action(self.state["hit_stuff"])
                self.hit_stuff = True

        self.rect.x += dx 
        self.rect.y += dy

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        #uncmment the bleow line to show projectile hitbox
        # pygame.draw.rect(surface, (255,0,0), self.rect)
        
    def update_image(self):
        animation_cooldown = 35
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.hit_stuff:
                self.frame_index = len(self.animation_list[self.action]) - 1
                self.ready_to_be_removed = True
            else:
                self.frame_index = 0

    def is_ready_to_be_removed(self):
        return self.ready_to_be_removed

    def update(self):
        self.move(SCREEN_WIDTH, SCREEN_HEIGHT, self.target)
        self.update_image()
