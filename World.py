from Unit import Unit
from Food import Food
from settings import *
import numpy
import pygame


class World:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.run_time = 0
        self.done = False
        self.population = self.generate_initial_population()
        self.energy = TOTAL_ENERGY
        self.vegetarian_food = []
        self.meat_food = []

    def run(self):
        while not self.done:
            self.clock.tick(FPS)
            self.generate_food()

            for unit in self.population:
                unit.take_action()

            self.render_world()
            # flip screen
            self.run_time += 1

    def generate_initial_population(self):
        population = []
        for i in range(100):
            population.append(Unit())
            self.energy -= 10
        return population

    def generate_food(self):
        while self.energy > 0:
            pos = numpy.random.randint(MAP_HEIGHT, size=2)
            self.vegetarian_food.append(Food(pos, "vegetarian", 1))
            self.energy -= 1

    def render_world(self):
        # render background
        for unit in self.population:
            # render unit
            continue
        for food in self.vegetarian_food:
            # render food
            continue
        for food in self.meat_food:
            # render food
            continue
