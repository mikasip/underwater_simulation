from helpers import load_image
import pygame


class GameUnit(pygame.sprite.Sprite):
    def __init__(self, pos, image_path, sprite_group, width=20, height=20):
        pygame.sprite.Sprite.__init__(self, sprite_group)
        image = load_image(image_path)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.pos = pos

    def get_tuple_pos():
        return (self.pos[0], self.pos[1])
