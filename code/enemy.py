import pygame
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.status = 'idle'  # init position
        self.import_graphics(monster_name)  # import animation sprites
        self.image = self.animations[self.status][self.frame_index]

        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-215, -85)  # trim the empty area
        self.obstacle_sprites = obstacle_sprites
        self.can_attack = True
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']

    def import_graphics(self, name):
        # the keys equal to the names of the directories
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [],
                           'idle': []}
        main = f'../res/entities/{name}'
        # import all png files by name in a loop
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main + '/' + animation)

    # the function calculates the distance from the enemy to the player
    # and the direction of the enemy vector in relation to the player
    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def animate(self):
        animation = self.animations[self.status] # getting array of status sprites

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'down':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]  # get a sprite
        self.rect = self.image.get_rect(center=self.hitbox.center)

    # The function calculates self.status based on direction && distance
    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        direct = self.get_player_distance_direction(player)[1]

        x = direct.x  # [-1:1] value range
        y = direct.y  # [-1:1] value range
        if distance <= self.attack_radius and self.can_attack:
            if '_attack' not in self.status:
                self.frame_index = 0
            self.status = '_attack'
            if 1 >= x > 0 and 0.98 >= y >= -0.98:
                self.status = 'right' + self.status
            elif y > 0.98:
                self.status = 'down' + self.status
            elif -1 <= x < 0 and 0.98 >= y >= -0.98:
                self.status = 'left' + self.status
            elif y < -0.98:
                self.status = 'up' + self.status
            elif x == 0 and y == 0:
                self.status = 'idle'


        elif distance <= self.notice_radius and distance > self.attack_radius:
            if x <= 1 and x > 0 and y <= 0.98 and y >= -0.98:
                self.status = 'right'
            elif y > 0.98:
                self.status = 'down'
            elif x >= -1 and x < 0 and y <= 0.98 and y >= -0.98:
                self.status = 'left'
            elif y < -0.98:
                self.status = 'up'

        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status != 'idle':  # If the status is not idle, the enemy goes to the player
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()  # enemy just stands

    # @Override
    def update(self):

        self.move(self.speed)
        self.animate()

    #This function updates the sprites in level.py
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
