import enum
import json


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
