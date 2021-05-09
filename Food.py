import pygame
from settings import FOOD_IMAGE_PATH
from helpers import load_image
from GameUnit import GameUnit


class Food(GameUnit):
    def __init__(self, pos, food_type, energy, sprite_group, width=10, height=10):
        GameUnit.__init__(self, pos, FOOD_IMAGE_PATH, sprite_group, width, height)
        self.pos = pos
        self.food_type = food_type
        self.energy = energy
