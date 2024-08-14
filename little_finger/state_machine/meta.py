import enum


class Event(enum.Enum):
    """子类继承"""
    ...


class State(enum.Enum):
    """
    子类继承
    """
    ...


class Context:

    def __init__(self, state, event):
        self.state = state
        self.event = event
