from staticData import StaticData
from factoryPlacement import FactoryIndividual


class Population:
    def __init__(self):
        self.data = StaticData()
        self.data.prepare_matrices()
        self.individuals = []


