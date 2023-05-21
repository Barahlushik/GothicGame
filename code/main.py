import pygame
import sys
from level import Level
from settings import *


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Dark Souls")
        self.clock = pygame.time.Clock()
        self.level = Level()
        # creating start screen
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load('../res/map/pdp_title.png')
        self.title_start_paused = True
    def run(self):
        while True:
            while self.title_start_paused:
                self.screen.blit(self.image, self.image.get_rect())
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.title_start_paused = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # if health <= 0 break game and start new game
            if self.level.is_player_death:
                break
            self.screen.fill('black')

            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)
        # start new game after death
        game_next = Game()
        game_next.run()

if __name__ == '__main__':
    game = Game()
    game.run()
