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


if __name__ == '__main__':
    ...