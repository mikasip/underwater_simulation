from helpers import load_image
import pygame


class GameUnit(pygame.sprite.Sprite):
    def __init__(self, pos, image_path, sprite_group, width=20, height=20):
        pygame.sprite.Sprite.__init__(self, sprite_group)
        image = load_image(image_path)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(left=pos[0], top=pos[1])
        self.pos = pos

    def update_rect(self):
        # Todo: rotate image
        self.rect = self.image.get_rect(left=self.pos[0], top=self.pos[1])
