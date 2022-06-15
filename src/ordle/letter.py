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

    def update_state(self, new):
        if self.value != new.value:
            raise ValueError("Values must match when updating letters")

        if self.state == Letter.State.CORRECT:
            return

        if new.state != Letter.State.EXCLUDED:
            self.state = new.state
        elif self.state != Letter.State.INCLUDED:
            self.state = new.state
