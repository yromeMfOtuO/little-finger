import json

from little_finger.state_machine.meta import Context, State
from little_finger.state_machine.transaction_builder import TransactionBuilder, InternalTransactionBuilder
from little_finger.state_machine.transaction_meta import Transaction


class StateMachine:
    """
    状态机
    """

    def __init__(self, name: str, states: dict[State, list[Transaction]]):
        self.states = states
        self.name = name
        print(f"State machine created: {name}, state->transactions: {json.dumps(states)} ")

    def fire_event(self, context: Context) -> State:
        transaction = self.match_transition(context)
        if transaction is None:
            return context.state
        transaction.action.do(context)

    def match_transition(self, context: Context):
        if context.state not in self.states:
            return None
        for transaction in self.states[context.state]:
            if transaction.event_match(context) and transaction.satisfied(context):
                return transaction

        return None

    def reset(self):
        self.states.clear()


class StateMachineFactory:

    def __init__(self):
        ...

    state_machines = dict()

    @staticmethod
    def register(name: str, state_machine: StateMachine):
        StateMachineFactory.state_machines[name] = state_machine

    @staticmethod
    def get(name: str):
        if name not in StateMachineFactory.state_machines:
            raise Exception(f"State machine {name} not found")
        return StateMachineFactory.state_machines.get(name)

    @staticmethod
    def remove(name: str):
        StateMachineFactory.state_machines.pop(name)


class StateMachineBuilder:

    def __init__(self):
        self.states = dict()

    def external(self):
        return TransactionBuilder(self.states)

    def internal(self):
        return InternalTransactionBuilder(self.states)

    def build(self, name: str) -> StateMachine:
        assert self.states is not None
        assert len(name) > 0

        machine = StateMachine(name, self.states)
        StateMachineFactory.register(name, machine)
        return machine


if __name__ == '__main__':
    ...
