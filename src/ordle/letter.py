from enum import Enum


class Letter:
    """A representation of a letter and the knowledge associated with it

    Public attributes:
    - value: its associated character
    - state: what is known about it (in the context of the given game)
    """

    class State(Enum):
        """The different states of knowledge"""

        UNKNOWN = 0
        CORRECT = 1
        INCLUDED = 2
        EXCLUDED = 3

    def __init__(self, value):
        self.value = value
        self.state = Letter.State.UNKNOWN

    def update_state(self, new):
        """Merge new knowledge (other Letter object) into existing Letter object"""
        if self.value != new.value:
            raise ValueError("Values must match when updating letters")

        if self.state == Letter.State.CORRECT:
            return

        if new.state != Letter.State.EXCLUDED:
            self.state = new.state
        elif self.state != Letter.State.INCLUDED:
            self.state = new.state
