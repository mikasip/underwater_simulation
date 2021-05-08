import numpy
import tensorflow
from Brain import Brain

class Unit:

    def __init__(self, genes = numpy.random.normal(size=)):
        self.size = genes[0]
        self.speed = genes[1]
        self.maturity = genes[2]
        self.diet = genes[3]
        self.sex = genes[4]
        #self.brain = Brain(genes[5:])


    def take_action(self):
        print("action")    
