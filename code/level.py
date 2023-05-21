import pygame
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from support import import_csv_layout
from ui import UI
from enemy import Enemy

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.attackable_sprites = pygame.sprite.Group() # enemy
        self.attack_sprites = pygame.sprite.Group() # weapon

        self.create_map()

        # weapon var
        self.current_attack = None

        # ui init
        self.ui = UI()

        # player_death_flag
        self.is_player_death = False

    def create_map(self):

        layouts = {
            'boundary': import_csv_layout('../res/map/boundary.csv'),
            'entities': import_csv_layout('../res/map/entities.csv')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), self.obstacle_sprites, 'invisible')
                        if style == 'entities':
                            if col == '26':
                                self.player = Player((x, y), self.visible_sprites, self.obstacle_sprites,
                                                     self.create_attack, self.destroy_attack)
                            elif col == '4274':
                                self.enemy = Enemy('opolchenets', (x, y),
                                                  [self.visible_sprites,self.attackable_sprites],
                                                  self.obstacle_sprites,self.damage_player, self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites,self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def add_exp(self, amount):
        self.player.exp += amount

    def damage_player(self, amount):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                for sprite in self.attackable_sprites:

                    if attack_sprite.rect.colliderect(sprite.hitbox):
                        sprite.get_damage(self.player, attack_sprite.sprite_type)
    # The function checks if the player is dead
    def player_death_handler(self):
        if self.player.health <= 0:
            self.is_player_death = True
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.player_death_handler()
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.floor_surface = pygame.image.load('../res/map/map.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)