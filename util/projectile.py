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
        self.flying = True
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
        set this to True when the destruct() method is finished
        '''
        self.ready_to_be_removed = False



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


    #this should be constantly calleds
    def move(self, screen_width, screen_height):
        SPEED = 10
        dx = 1
        dy = 2
        GRAVITY = 10


        #apply gravity 
        self.vel_y += GRAVITY
        dy += self.vel_y

        '''
        if projectile hit the walls or the ground,
        then set self.hit_stuff = True
        '''
        #ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
            self.hit_stuff = True
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
            self.hit_stuff = True
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            dy = screen_height - 110 - self.rect.bottom
            self.hit_stuff = True

        self.rect.x += dx 
        self.rect.y += dy

    def draw(self, surface):
        RED = (255,0,0)
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))

        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))


    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

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
                self.frame_index = len(self.animation_list[self.action]) -1
                self.ready_to_be_removed = True
        
            else:#if the projectile didn't hit stuff, loop through the flying animations
                self.frame_index = 0

            

    '''
    function for distructing the projectile
    call this function when self.hit_stuff == true

    '''
    def destruct(self, target):
        self.destruct_sound.play()
        #projectile hit box is the same as the init rect
        attacking_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
            target.hit = True
    
    def ready_to_be_removed(self):
        return self.ready_to_be_removed
    #handle animation updates
    def update(self):
        
        self.move(SCREEN_WIDTH, SCREEN_HEIGHT)

        if self.hit_stuff:
            self.destruct(self.target)

        self.update_image()

        

        

        



# 
#         #check if the animation has finished
#         if self.frame_index >= len(self.animation_list[self.action]):
#             #if the player is dead then end the animation
#             if self.hit_stuff == True:
#                 '''
#                 When the projectile hit something, either wall/groud/enemy
#                 And when the destruct animation is called
#                 turn the projectile image to blank
#                 and wait to be removed from projectile list

#                 '''
#                 self.frame_index = len(self.animation_list[self.action])
#             else:
#                 self.frame_index = 0
                