import json

from little_finger.state_machine.state_machine import State, Event


class OrderEvent(Event):
    """
    订单事件
    """

    DepositInit = 'DepositInit'
    DepositUnknown = 'DepositUnknown'
    DepositFinished = 'DepositFinished'
    FreezeInit = 'FreezeInit'
    FreezeUnknown = 'FreezeUnknown'
    FreezeFinished = 'FreezeFinished'
    AcceptInit = 'AcceptInit'
    AcceptUnknown = 'AcceptUnknown'
    AcceptFinished = 'AcceptFinished'
    SettleInit = 'SettleInit'
    SettleUnknown = 'SettleUnknown'
    SettleFinished = 'SettleFinished'
    Success = 'Success'
    Fail = 'Fail'


class OrderState(State):
    """
    订单状态
    """

    INIT = 'INIT'
    PENDING_DEPOSIT = 'PENDING_DEPOSIT'
    PENDING_FREEZE = 'PENDING_FREEZE'
    PENDING_ACCEPT = 'PENDING_ACCEPT'
    PENDING_SETTLE = 'PENDING_SETTLE'
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'


class OrderStateMachine:



    def __init__(self):
        ...

    ...


if __name__ == '__main__':
    print(json.dumps({"state": OrderState.INIT, "event": OrderEvent.DepositInit}))
    ...
