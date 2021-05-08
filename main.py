import random
import numpy
import settings
from World import World

def get_data(world):
    # extract and return data
    return []

def run_simulation(time = settings.SIM_TIME):
    world = World()
    world.run(time)
    data = get_data(world)
    print(data)

if __name__ == "__main__":
    run_simulation()