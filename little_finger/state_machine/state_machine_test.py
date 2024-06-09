from little_finger.state_machine.state_machine import State, Event


class OrderEvent(Event):
    """
    订单事件
    """

    DepositInit = 1
    DepositUnknown = 2
    DepositFinished = 3
    FreezeInit = 4
    FreezeUnknown = 5
    FreezeFinished = 6
    AcceptInit = 7
    AcceptUnknown = 8
    AcceptFinished = 9
    SettleInit = 10
    SettleUnknown = 11
    SettleFinished = 12
    Success = 13
    Fail = 14


class OrderState(State):
    """
    订单状态
    """

    INIT = 1
    PENDING_DEPOSIT = 2
    PENDING_FREEZE = 3
    PENDING_ACCEPT = 4
    PENDING_SETTLE = 5
    SUCCESS = 6
    FAIL = 7


class OrderStateMachine:



    def __init__(self):
        ...

    ...


if __name__ == '__main__':
    ...
