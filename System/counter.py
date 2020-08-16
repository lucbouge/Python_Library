from .print import eprint


class Counter:
    def __init__(self):
        self.counter_dict = dict()

    def increment(self, tag):
        if tag not in self.counter_dict:
            self.counter_dict[tag] = 0
        self.counter_dict[tag] += 1

    def eprint(self):
        eprint("_" * 20)
        for (tag, nb) in sorted(self.counter_dict.items()):
            eprint(tag + ": ", nb)
