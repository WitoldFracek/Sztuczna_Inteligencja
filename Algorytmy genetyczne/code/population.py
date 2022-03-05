from staticData import StaticData
from factoryPlacement import FactoryIndividual

EASY = 'easy'
FLAT = 'flat'
HARD = 'hard'
EASY_SIZE = (3, 3)
FLAT_SIZE = (1, 12)
HARD_SIZE = (4, 5)

# Set exercise mode
MODE = EASY
MODE_SIZE = EASY_SIZE


class Population:
    def __init__(self, size):
        self.data = StaticData(MODE)
        self.data.prepare_matrices()
        self.individuals = []
        for _ in range(size):
            ind = FactoryIndividual(self.data.machine_count, MODE_SIZE)
            ind.random_start()
            self.individuals.append(ind)

    def get_adaptations(self):
        return [ind.adaptation(self.data.value_matrix) for ind in self.individuals]


