

class ValueHolder:
    def __init__(self, value, domain):
        self.value = value
        self.domain = set(domain)
        self.is_first = False

    def remove(self, domain_value):
        self.domain.remove(domain_value)

