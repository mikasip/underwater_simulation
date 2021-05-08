import random
import numpy
import settings
from World import World
from Brain import Brain


def get_data(world):
    # extract and return data
    return []


def run_simulation(time=settings.SIM_TIME):
    world = World()
    # world.run(time)
    data = get_data(world)
    print(data)


if __name__ == "__main__":
    # run_simulation()

    brain = Brain(
        alpha=0.0005,
        gamma=0.85,
        epsilon=1,
        input_dims=(9, 9, 1),
        n_actions=10,
        batch_size=32,
        replace=128,
    )
    for item in brain.get_weights():
        print(item.shape)
