import enum


class StateMachine:
    def __init__(self, cfg, states, events_handler, actions_handler):
        # config information for an instance
        self.cfg = cfg
        # define the states and the initial state
        self.states = [s.lower() for s in states]
        self.state = self.states[0]
        # process the inputs according to current state
        self.events = dict()
        # actions according to current transfer 
        self.actions = {state: dict() for state in self.states}
        # cached data for temporary use
        self.records = dict()
        # add events and actions
        for i, state in enumerate(self.states):
            self._add_event(state, events_handler[i])
            for j, n_state in enumerate(self.states):
                self._add_action(state, n_state, actions_handler[i][j])

    def _add_event(self, state, handler):
        self.events[state] = handler

    def _add_action(self, cur_state, next_state, handler):
        self.actions[cur_state][next_state] = handler

    def run(self, inputs):
        # decide the state-transfer according to the inputs
        new_state, outputs = self.events[self.state](inputs, self.states, self.records, self.cfg)
        # do the actions related with the transfer 
        self.actions[self.state][new_state](outputs, self.records, self.cfg)
        # do the state transfer
        self.state = new_state
        return new_state

    def reset(self):
        self.state = self.states[0]
        self.records = dict()


class Action:

    def d(self):
        ...


class Event:

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
        ...

class Condition:

    def satisfied(self, ctx: Context):
        ...
    ...


class Transaction:

    def __init__(self,
                 from_state: State,
                 to_state: State,
                 event: Event,
                 condition: Condition,
                 action: Action):
        self.from_state = from_state
        self.to_state = to_state
        self.event = event
        self.condition = condition
        self.action = action

    ...


class StateMachine:

    def __init__(self, states: dict[State, list[Transaction]]):
        ...

    def run(self, inputs):
        ...

    def reset(self):
        ...


class TransactionBuilder:

    def __init__(self):
        self.from_state = None
        self.to_state = None
        self.event = None
        self.condition = None
        self.action = None

    def f(self, from_state: State):
        self.from_state = from_state
        return self

    def t(self, to_state: State):
        self.to_state = to_state
        return self

    def on(self, event: Event):
        self.event = event
        return self

    def when(self, condition: Condition):
        self.condition = condition
        return self

    def then(self, action: Action):
        self.action = action
        return self

    def build(self):
        return Transaction(
            self.from_state,
            self.to_state,
            self.event,
            self.condition,
            self.action
        )


class InternalTransactionBuilder(TransactionBuilder):

    def __init__(self):
        super().__init__()

    def i(self, state: State):
        self.f(state)
        self.t(state)
        return self

    ...


class StateMachineBuilder:

    def external(self):
        return TransactionBuilder()

    def internal(self):
        return InternalTransactionBuilder()

    def build(self):
        ...


if __name__ == '__main__':
    ...