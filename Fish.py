import numpy
import tensorflow
import pygame
from Brain import Brain
from settings import *
from GameUnit import GameUnit

brain = Brain(
    alpha=0.0005,
    gamma=0.85,
    epsilon=0.01,
    input_dims=(125, 1),
    n_actions=4,
    batch_size=32,
    replace=128,
)
weights = brain.get_weights()
for arr in weights:
    print(arr.shape)


class Fish(GameUnit):
    def __init__(
        self,
        pos,
        sprite_group,
        width=20,
        height=20,
        genes=numpy.random.normal(size=5),
        brain_genes=None,
    ):
        GameUnit.__init__(self, pos, FISH_IMAGE_PATH, sprite_group, width, height)
        self.size = (numpy.tanh(genes[0]) + 1) * 25
        if self.size < 10:
            self.size = 10
        self.speed = numpy.tanh(genes[1] + 1.5)
        # Todo: decode maturity and diet
        self.maturity = genes[2]
        self.diet = genes[3]
        self.sex = 0 if genes[4] < 0 else 1
        self.energy_left = 10
        self.direction = numpy.array([0, 1])
        self.prev_action = []
        self.prev_observation = []
        self.prev_reward = 0
        self.brain = Brain(
            alpha=0.0005,
            gamma=0.85,
            epsilon=0,
            input_dims=(32, 1),
            n_actions=2,
            batch_size=32,
            replace=128,
        )
        # Todo:
        # if brain_genes:
        #    self.brain.set_weights(brain_genes)

    def take_action(self, inp):
        if len(self.prev_action) > 0:
            self.brain.store_transition(
                self.prev_observation, self.prev_action, self.prev_reward, inp, False
            )
        if self.energy_left <= 0:
            self.kill()
        action = self.brain.choose_action(inp)[0].numpy()
        current_angle = numpy.arctan2(self.direction[0], self.direction[1])
        new_angle = current_angle + (numpy.pi / 4) * (action[0] * 2 - 1)
        self.direction = numpy.array([numpy.cos(new_angle), numpy.sin(new_angle)])
        move_speed = action[1] * 2
        new_pos = self.pos + self.direction * self.speed * move_speed
        self.pos = (
            new_pos
            if new_pos[0] >= 0
            and new_pos[0] <= MAP_WIDTH
            and new_pos[1] >= 0
            and new_pos[1] <= MAP_HEIGHT
            else self.pos
        )
        self.update_rect()
        energy_lost = 0.01 + 0.01 * (self.speed * move_speed * (self.size / 25))
        self.energy_left -= energy_lost
        self.prev_action = action
        self.prev_observation = inp
        self.prev_reward -= energy_lost
        # self.brain.learn()
        return energy_lost

    def learn(self, prev_state, new_state, reward):
        self.brain.learn()
