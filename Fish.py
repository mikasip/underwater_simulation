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
    input_dims=(48, 1),
    n_actions=3,
    batch_size=32,
    replace=128,
)
weights = brain.get_weights()
array = numpy.array([])
for arr in weights:
    print(arr.shape)
    array = numpy.append(array, arr)

print(array.shape)


class Fish(GameUnit):
    def __init__(
        self,
        pos,
        sprite_group,
        width=20,
        height=20,
        genes=numpy.random.normal(size=5),
        brain_genes=[],
    ):
        GameUnit.__init__(self, pos, FISH_IMAGE_PATH, sprite_group, width, height)
        self.size = (numpy.tanh(genes[0]) + 1) * 25
        if self.size < 10:
            self.size = 10
        self.speed = numpy.tanh(genes[1] + 1.5)
        # Todo: decode maturity and diet
        self.genes = genes
        self.maturity = genes[2]
        self.diet = genes[3]
        self.sex = 0 if genes[4] < 0.5 else 1
        self.energy_left = 10
        angle = numpy.random.uniform(0, 2 * numpy.pi)
        self.direction = numpy.array([numpy.cos(angle), numpy.sin(angle)])
        self.prev_action = []
        self.prev_observation = []
        self.prev_reward = 0
        self.wants_to_mate = False
        self.mate_timer = 0
        self.move_speed = 1
        self.brain = Brain(
            alpha=0.0005,
            gamma=0.85,
            epsilon=0,
            input_dims=(48, 1),
            n_actions=3,
            batch_size=32,
            replace=128,
        )
        if len(brain_genes) > 0:
            self.brain.set_weights(brain_genes)

    def take_action(self, inp, update_action=False):
        # if len(self.prev_action) > 0:
        #    self.brain.store_transition(
        #        self.prev_observation, self.prev_action, self.prev_reward, inp, False
        #    )
        if self.energy_left <= 0:
            self.kill()
        if update_action:
            action = self.brain.choose_action(inp)[0].numpy()
            current_angle = numpy.arctan2(self.direction[0], self.direction[1])
            new_angle = current_angle + (numpy.pi / 8) * (action[0] * 2 - 1)
            self.direction = numpy.array([numpy.cos(new_angle), numpy.sin(new_angle)])
            self.move_speed = action[1] * 2
        new_pos = self.pos + self.direction * self.speed * self.move_speed
        self.pos = (
            new_pos
            if new_pos[0] >= 0
            and new_pos[0] <= MAP_WIDTH
            and new_pos[1] >= 0
            and new_pos[1] <= MAP_HEIGHT
            else self.pos
        )
        if self.mate_timer >= 300:
            self.wants_to_mate = True if self.prev_action[2] > 0.5 else False
        self.update_rect()
        energy_lost = 0.02 + 0.02 * (self.speed * self.move_speed * (self.size / 25))
        self.energy_left -= energy_lost
        if update_action:
            self.prev_action = action
            self.prev_observation = inp
            self.prev_reward -= energy_lost
        self.mate_timer += 1
        # self.brain.learn()
        return energy_lost

    def get_genes(self):
        genes = numpy.array(self.genes)
        weights = brain.get_weights()
        brain_genes = numpy.array([])
        for arr in weights:
            brain_genes = numpy.append(brain_genes, arr)
        genes = numpy.append(genes, brain_genes)
        return genes
