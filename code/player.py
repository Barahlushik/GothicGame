import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites,create_attack, destroy_attack,create_abilities):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../res/player/down/down_1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-80, -40)
        self.speed = 5
        ############ start animation var block ############
        self.import_player_assets()  # import player sprites

        self.attacking = False  # attack flag
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        self.frame_index = 0  # index of animation sprite
        self.animation_speed = 0.15

        self.status = 'down'
        ############ end animation var block ############
        self.direction = pygame.math.Vector2()

        self.vulnerable = True # player can get damage from enemy, if false - not
        self.hurt_time = None # timer
        self.invulnerability_duration = 500 # invulnerability time after the attack
        self.weapon = list(weapon_data.keys())[0]
        # attack
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        # stats
        self.stats = {'health': 100, 'energy': 100, 'attack': 10, 'speed': 7, 'heals': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 500
        self.speed = self.stats['speed']
        self.heals = self.stats['heals']
        # create abilities block
        self.create_abilities = create_abilities
        self.using_health_ability = False
        self.using_roll_ability = False
        self.heal_time = None
        self.roll_time = None
        self.using_health_ability_cooldown = 4000
        self.using_roll_ability_cooldown = 500
        self.roll_bonus = 20
        self.roll_duration = 100
        self.roll_decrement = False

    def input(self):  # Disabling movement during an attack
        if not self.attacking:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'  # "res/player/up" group of sprites
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'  # "res/player/down" group of sprites
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'  # "res/player/left" group of sprites
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'  # "res/player/right" group of sprites
            else:
                self.direction.x = 0
            # attack
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack() # create Weapon object
        if not self.using_health_ability:
            if keys[pygame.K_f]:
                if self.create_abilities('heal', self.stats['health']/2, 0):
                    self.using_health_ability = True
                    self.heal_time = pygame.time.get_ticks()
        if not self.using_roll_ability:
            if keys[pygame.K_LSHIFT]:
                if self.create_abilities('roll', self.roll_bonus, 25):
                    self.roll_decrement = True
                    self.using_roll_ability = True
                    self.roll_time = pygame.time.get_ticks()
    # Function sets to a certain key the corresponding set of sprites from the folder "res/player/"
    def import_player_assets(self):
        path = '../res/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [],
                           'down_idle': [], 'up_idle': [], 'left_idle': [], 'right_idle': []}
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    # Function checks the cooldown
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack() # destroy Weapon object sprite
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
        if self.using_health_ability:
            if current_time - self.heal_time >= self.using_health_ability_cooldown:
                self.using_health_ability = False
        if self.using_roll_ability:
            if self.roll_decrement:
                if current_time - self.roll_time >= self.roll_duration:
                    self.speed -= self.roll_bonus
                    self.roll_decrement = False
            if current_time - self.roll_time >= self.using_roll_ability_cooldown:
                self.using_roll_ability = False

    # The function sets the status of the player's action based on the movement and the initial status
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    # The main animation function that assigns self.image && self.rect according to self.animation_speed
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        # block creates a flickering sprite after impact
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    # calculate weapon + player damage
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.25
        else:
            self.energy = self.stats['energy']
    # @Override
    def update(self):
        self.input()
        self.cooldowns()  # check cooldown
        self.get_status()  # update self.status
        self.animate()  # draw sprite
        self.move(self.speed)
        self.energy_recovery()