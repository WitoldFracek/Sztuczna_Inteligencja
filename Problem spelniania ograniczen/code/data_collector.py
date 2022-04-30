

class DataCollector:

    __slots__ = ['nodes', 'steps_till_first', 'first_found']

    def __init__(self):
        self.nodes = 0
        self.steps_till_first = 0
        self.first_found = False

    def reset(self):
        self.nodes = 0
        self.steps_till_first = 0
        self.first_found = False


