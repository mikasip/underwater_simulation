import pygame
import sys
from settings import *
from World import World


class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_NAME)
        self.screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        self.world = World()

        self.background = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.background.fill(pygame.Color(BG_COLOR))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.key_events()
            self.world.events()
            self.render_world()

    def render_world(self):
        # render background
        self.screen.blit(self.background, (0, 0))
        for fish in self.world.population:
            # render unit
            self.screen.blit(fish.image, fish.pos)
        for food in self.world.vegetarian_food:
            self.screen.blit(food.image, food.pos)
        for food in self.world.meat_food:
            self.screen.blit(food.image, food.pos)
        pygame.display.flip()

    def quit(self):
        self.playing = False
        pygame.quit()
        sys.exit()

    def key_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
