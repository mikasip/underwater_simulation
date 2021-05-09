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
            inp = self.__input_for_pos(fish.pos, fish)
            energy_lost = fish.take_action(inp)
            self.__check_collisions(fish, self.vegetarian_food)
            self.energy -= energy_lost
        self.__generate_food()

    def __generate_food(self):
        while self.energy > 0:
            Food(get_random_pos(), "vegetarian", 1, self.vegetarian_food)
            self.energy -= 1

    def __check_collisions(self, fish, sprite_group):
        hits = pygame.sprite.spritecollide(fish, sprite_group, True)
        fish.energy_left += len(hits)
        fish.prev_reward += len(hits)

    def __input_for_pos(self, pos, fish):
        input_vec = []
        x = pos[0] - 100
        y = pos[1] - 100
        for i in range(4):
            for j in range(4):
                rect = pygame.Rect(x + i * 50, y + j * 50, 50, 50)
                input_vec.append(
                    1 if any(rect.colliderect(food.rect) for food in self.vegetarian_food) else 0
                )
                # input_vec.append(meat_food_collisions = 1 if any(rect.colliderect(food.rect) for food in self.meat_food) else 0)
                input_vec.append(
                    1
                    if any(
                        rect.colliderect(other_fish.rect)
                        for other_fish in self.population
                        if fish != other_fish
                    )
                    else 0
                )
                # Todo: check collisions for mating partners and enemy fish and add to input
        return numpy.expand_dims(numpy.array(input_vec), 1)
