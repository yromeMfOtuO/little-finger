from little_finger.state_machine.meta import State, Event
from little_finger.state_machine.transaction_meta import Transaction, Action, Condition


class TransactionBuilder:

    def __init__(self, states: dict[State, list[Transaction]]):
        self.from_state = None
        self.to_state = None
        self.event = None
        self.condition = None
        self.action = None
        self.states = states

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
        transaction = Transaction(self.from_state, self.to_state, self.event, self.condition, self.action)
        if self.from_state not in self.states:
            self.states[self.from_state] = []
        self.states[self.from_state].append(transaction)
        return transaction


class InternalTransactionBuilder(TransactionBuilder):

    def i(self, state: State):
        self.f(state)
        self.t(state)
        return self