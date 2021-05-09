import numpy
import tensorflow
import pygame
from Brain import Brain
from settings import *
from GameUnit import GameUnit


class Fish(GameUnit):
    def __init__(self, pos, sprite_group, width=20, height=20, genes=numpy.random.normal(size=125)):
        GameUnit.__init__(self, pos, FISH_IMAGE_PATH, sprite_group, width, height)
        self.size = (numpy.tanh(genes[0]) + 1) * 25
        if self.size < 10:
            self.size = 10
        self.speed = numpy.tanh(genes[1] + 1.5)
        self.maturity = genes[2]
        self.diet = genes[3]
        self.sex = 0 if genes[4] < 0 else 1
        self.energy_left = 10
        self.brain = Brain(
            alpha=0.0005,
            gamma=0.85,
            epsilon=0.01,
            input_dims=(125, 1),
            n_actions=4,
            batch_size=32,
            replace=128,
        )

    def take_action(self):
        # if energy <= 0:
        # unit dies
        action = numpy.random.uniform(size=4)
        direction = numpy.random.uniform(-1, 1, 2)
        scaled_direction = direction / numpy.linalg.norm(direction)
        new_pos = self.pos + scaled_direction * self.speed
        self.pos = (
            new_pos
            if new_pos[0] >= 0
            and new_pos[0] <= MAP_WIDTH
            and new_pos[1] >= 0
            and new_pos[1] <= MAP_HEIGHT
            else self.pos
        )
        self.energy_left -= 0.01

        # todo: if self.collides(): act accordingly
