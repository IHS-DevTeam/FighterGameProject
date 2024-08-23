import pygame
from pygame import mixer
from util.constants import *
from util.constants import *
mixer.init()
pygame.init()


class Projectile():
    def __init__(self, cord, flip, data, sprite_sheet, animation_steps, sound, target):
        self.spawn_x, self.spawn_y = cord 
        self.size = data[0]
        self.image_scale = data[1]
        self.flip = flip
        self.state = {
            "flying":       0,
            "hit_stuff":    1
        }
        self.action = self.state["flying"]
        self.frame_index = 0
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.hit_stuff = False
        self.action = 0
        self.frame_index = 0
        self.hit_stuff = False
        self.rect = pygame.Rect((self.spawn_x, self.spawn_y, 30,30))
        self.image_scale = data[1]
        self.offset = data[2]
        self.destruct_sound = sound
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.vel_y = 0
        self.target = target
        

        '''
        self.ready_to_be_removed is used to tell wheter the projectile
        is ready to be removed from the projectile list
        set this to true after:
            1. self.hit_stuff == True
            2. self.image == self.animation_list[self.hit_stuff][len(self.)]
        '''
        self.ready_to_be_removed = False
        
        self.do_damage = True



    #useed to initialize PIV
    def load_images(self, sprite_sheet, animation_steps):
        #extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #this should be constantly calleds
    def move(self, screen_width, screen_height, target):
        SPEED = 50
        dx = 10

        if self.flip:
            dx *= -1
        # dy = 2
        # GRAVITY = 10
        dy = 0
        GRAVITY = 0


        #apply gravity 
        self.vel_y += GRAVITY
        dy += self.vel_y

        '''
        if the projectile hit the enemy:
        '''

        attacking_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        if attacking_rect.colliderect(target.rect):
            self.update_action(self.state["hit_stuff"])
            if self.do_damage == True:
                target.health -= 10
                target.hit = True
                self.destruct_sound.play()
                self.do_damage = False
            
            dx = 0
            dy = 0
        else:
            '''
            if projectile hit the walls or the ground,
            but MISSED THE PLAYER
            then set self.hit_stuff = True
            '''
            
            if self.rect.left + dx < 0:
                dx = -self.rect.left
                self.update_action(self.state["hit_stuff"])
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
                self.update_action(self.state["hit_stuff"])
            if self.rect.bottom + dy > screen_height - 110:
                self.vel_y = 0
                dy = screen_height - 110 - self.rect.bottom
                self.update_action(self.state["hit_stuff"])

        self.rect.x += dx 
        self.rect.y += dy

    def draw(self, surface):
        RED = (255,0,0)
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))




    def update_image(self):
        animation_cooldown = 35
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        #check if animation is finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #if the projectile hit stuff, let the image freeze as the last image
            if self.hit_stuff == True:
                self.action = self.state["hit_stuff"]
                self.frame_index = len(self.animation_list[self.action]) -1
                self.ready_to_be_removed = True
        
            else:#if the projectile didn't hit stuff, loop through the flying animations
                self.frame_index = 0

            


    
    def ready_to_be_removed(self):
        return self.ready_to_be_removed
    #handle animation updates
    def update(self):
        
        self.move(SCREEN_WIDTH, SCREEN_HEIGHT, self.target)

        self.update_image()
        

        

        


                