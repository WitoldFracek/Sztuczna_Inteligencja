import numpy as np
import json


class StaticData:
    def __init__(self, mode, autoprepare=False):
        self.__cost_matrix = np.zeros((1, 1))
        self.__flow_matrix = np.zeros((1, 1))
        self.value_matrix = np.zeros((1, 1))
        self.__machine_count = 0
        self.__COST_PATH = f'../data/{mode}_cost.json'
        self.__FLOW_PATH = f'../data/{mode}_flow.json'
        if autoprepare:
            self.prepare_matrices()

    def __get_list(self, path):
        with open(path, encoding='utf-8') as file:
            loaded_dict = json.load(file)
        return loaded_dict

    def __check_machine_count(self, data_list):
        machine_list = set()
        for d in data_list:
            machine_list.add(d['source'])
            machine_list.add(d['dest'])
        return max(machine_list) + 1

    def prepare_matrices(self):
        costs = self.__get_list(self.__COST_PATH)
        flows = self.__get_list(self.__FLOW_PATH)
        count = self.__check_machine_count(costs)
        self.__machine_count = count
        self.__cost_matrix = np.zeros((count, count), dtype=np.int64)
        self.__flow_matrix = np.zeros((count, count), dtype=np.int64)
        self.__assign_cost(costs)
        self.__assign_flow(flows)
        self.value_matrix = self.__cost_matrix * self.__flow_matrix

    def __assign_cost(self, data_list):
        for d in data_list:
            source = d['source']
            dest = d['dest']
            cost = d['cost']
            self.__cost_matrix[source, dest] = cost

    def __assign_flow(self, data_list):
        for d in data_list:
            source = d['source']
            dest = d['dest']
            flow = d['amount']
            self.__flow_matrix[source, dest] = flow

    @property
    def machine_count(self):
        return self.__machine_count

    # debug
    def debug(self):
        print(self.value_matrix)
