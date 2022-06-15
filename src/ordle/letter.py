from enum import Enum


class Letter:
    class State(Enum):
        UNKNOWN = 0
        CORRECT = 1
        INCLUDED = 2
        EXCLUDED = 3

    def __init__(self, value):
        self.value = value
        self.state = Letter.State.UNKNOWN
