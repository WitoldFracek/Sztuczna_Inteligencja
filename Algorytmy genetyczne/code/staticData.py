import numpy as np
import json

# EASY = 'easy'
# FLAT = 'flat'
# HARD = 'hard'
# EASY_SIZE = (3, 3)
# FLAT_SIZE = (1, 12)
# HARD_SIZE = (4, 5)
#
# # Set exercise mode
# MODE = EASY
# MODE_SIZE = EASY_SIZE
#
# COST_PATH = f'../data/{MODE}_cost.json'
# FLOW_PATH = f'../data/{MODE}_flow.json'


class StaticData:
    def __init__(self, mode):
        self.cost_matrix = np.zeros((1, 1))
        self.flow_matrix = np.zeros((1, 1))
        self.value_matrix = np.zeros((1, 1))
        self.machine_count = 0
        self.COST_PATH = f'../data/{mode}_cost.json'
        self.FLOW_PATH = f'../data/{mode}_flow.json'

    def __get_list(self, path):
        with open(path, encoding='utf-8') as file:
            loaded_dict = json.load(file)
        return loaded_dict

    def __check_machine_count(self, data_list):
        machine_list = set()
        for d in data_list:
            machine_list.add(d['source'])
            machine_list.add(d['dest'])
        return max(machine_list)

    def prepare_matrices(self):
        costs = self.__get_list(self.COST_PATH)
        flows = self.__get_list(self.FLOW_PATH)
        count = self.__check_machine_count(costs) + 1
        self.machine_count = count
        self.cost_matrix = np.zeros((count, count), dtype=np.int64)
        self.flow_matrix = np.zeros((count, count), dtype=np.int64)
        self.__assign_cost(costs)
        self.__assign_flow(flows)
        self.value_matrix = self.cost_matrix * self.flow_matrix

    def __assign_cost(self, data_list):
        for d in data_list:
            source = d['source']
            dest = d['dest']
            cost = d['cost']
            self.cost_matrix[source, dest] = cost

    def __assign_flow(self, data_list):
        for d in data_list:
            source = d['source']
            dest = d['dest']
            flow = d['amount']
            self.flow_matrix[source, dest] = flow

    # temp public
    def get_list(self, path):
        return self.__get_list(path)

    def cmc(self, path):
        return self.__check_machine_count(path)
