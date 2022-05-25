

class DataCollector:
    def __init__(self):
        self.step_in = 0
        self.step_up = 0
        self.steps_till_first = 0
        self.first_found = False

    def reset(self):
        self.step_in = 0
        self.step_up = 0
        self.steps_till_first = 0
        self.first_found = False


