

class ValueHolder:
    def __init__(self, value):
        self.value = value
        self.domain_checked = set()

    def __add__(self, domain_value):
        self.domain_checked.add(domain_value)

