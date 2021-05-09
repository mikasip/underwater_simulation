from os import path
import pygame
from settings import *
import numpy


def load_image(path_in_assets):
    image_path = path.join(path.dirname(__file__), "assets", path_in_assets)
    image = pygame.image.load(image_path).convert_alpha()
    return image


def get_random_pos():
    return numpy.array([numpy.random.randint(MAP_WIDTH), numpy.random.randint(MAP_HEIGHT)])
