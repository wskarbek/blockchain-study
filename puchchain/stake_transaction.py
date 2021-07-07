from collections import OrderedDict


class StakeTransaction:
    def __init__(self, sender, node, time, signature, amount):
        self.sender = sender
        self.node = node
        self.time = time
        self.signature = signature
        self.amount = amount

    def __repr__(self):
        return str(self.__dict__)

    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('time', self.time), ('amount', self.amount)])
