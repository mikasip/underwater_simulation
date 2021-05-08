from Unit import Unit

class World:
    
    def __init__(self):
        self.run_time = 0
        self.done = False
        self.population = self.generate_initial_population()

    def run(self):
        while not self.done:
            for unit in population:
                unit.take_action()
            


            self.run_time += 1

    def generate_initial_population(self):
        population = []
        for i in range(100):
            population.append(Unit())