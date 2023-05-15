import pygame



class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.status.split('_')[0]
        self.image = pygame.Surface((32, 32)) # attack area near the player
        self.image.set_alpha(0) # make the surface transparent
        self.sprite_type = 'weapon'

        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.hitbox.midright)
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.hitbox.midleft)
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.hitbox.midtop)
        else:
            self.rect = self.image.get_rect(midtop=player.hitbox.midbottom)
