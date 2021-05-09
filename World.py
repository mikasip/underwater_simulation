from Fish import Fish
from Food import Food
from settings import *
from helpers import get_random_pos
import numpy
import pygame


class World:
    def __init__(self):
        self.run_time = 0
        self.done = False
        self.energy = TOTAL_ENERGY
        self.vegetarian_food = pygame.sprite.Group()
        self.meat_food = pygame.sprite.Group()
        self.population = pygame.sprite.Group()
        self.__generate_initial_population()

    def __generate_initial_population(self):
        population = []
        for i in range(50):
            Fish(get_random_pos(), self.population)
            self.energy -= 10
        return population

    def events(self):
        for fish in self.population:
            fish.take_action()
        self.__generate_food()

    def __generate_food(self):
        while self.energy > 0:
            Food(get_random_pos(), "vegetarian", 1, self.vegetarian_food)
            self.energy -= 1
