import pygame

from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites,create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load(
            'res/player/down/down_1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-60, -60)
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

        # attack
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack



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

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack() # create Weapon object
    # Function sets to a certain key the corresponding set of sprites from the folder "res/player/"
    def import_player_assets(self):
        path = './res/player/'
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

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.cooldowns()  # check cooldown
        self.get_status()  # update self.status
        self.animate()  # draw sprite
        self.move(self.speed)
