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


class From:

    def __init__(self):
        self.from_state = None

    def f(self, from_state: State):
        """
        设置初始状态
        """
        self.from_state = from_state
        return self


class To:

    def __init__(self):
        self.to_state = None

    def t(self, to_state: State):
        self.to_state = to_state
        return self


class On:

    def __init__(self):
        self.event = None

    def on(self, event: Event):
        self.event = event
        return self


class When:

    def __init__(self):
        self.condition = None

    def when(self, condition: Condition):
        self.condition = condition
        return self


class Then:

    def __init__(self):
        self.action = None

    def then(self, action: Action):
        self.action = action
        return self
