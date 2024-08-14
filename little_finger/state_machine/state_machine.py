import json

from little_finger.state_machine.meta import Context, State, Event


class Action:

    def do(self, ctx: Context):
        """
        具体的事件处理逻辑
        需要子类具体实现
        """
        ...


class Condition:
    """
    条件判断, 用于判断是否满足状态转移的条件
    需要子类具体实现
    """

    def satisfied(self, ctx: Context):
        ...


class Transaction:
    """
    从一个状态到另一个状态的转移
    包含初始结束状态, 触发事件, 是否符合执行条件判断, 动作
    """

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

    def event_match(self, ctx: Context):
        return self.event == ctx.event

    def satisfied(self, ctx: Context):
        return self.condition.satisfied(ctx)


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
