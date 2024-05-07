from little_finger.state_machine.state_machine import State


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
