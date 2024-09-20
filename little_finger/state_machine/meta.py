import enum


class Event(str, enum.Enum):
    """子类继承"""
    ...


class State(str, enum.Enum):
    """
    子类继承
    """
    ...


class Context:

    def __init__(self, state, event):
        self.state = state
        self.event = event
