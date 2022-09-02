import random
import itertools

class WaterTank:
    def __init__(self, water_capacity=100, init_level=50, inflow = (1, 2), outflow = (0, 1)):
        self.water_capacity = water_capacity
        self.water_level_states = list(range(0, self.water_capacity))
        self.current_state = init_level
        self.inflow = inflow
        self.outflow = outflow
        self.failed = False
        self.states = list(range(water_capacity))

    def transition(self, action):
        if not self.failed:
            out = random.randrange(self.outflow[0], self.outflow[1]+1)
            if action == "open":
                change = random.randrange(self.inflow[0], self.inflow[1]+1) - out
                self.current_state = self.current_state + change
            else:
                change = -out
                self.current_state = self.current_state + change
            
            if self.current_state < 0 or self.current_state >= self.water_capacity:
                self.failed = True

    def next_state(self, current_state, action, failed=False):
        if failed:
            return current_state, failed
        else:
            out = random.randrange(self.outflow[0], self.outflow[1]+1)
            if action == "open":
                change = random.randrange(self.inflow[0], self.inflow[1]+1) - out
            else:
                change = -out
            
            if current_state + change < 0 or current_state + change >= self.water_capacity:
                failed = True
            
            return current_state + change, failed


class Shield:
    def __init__(self, switch_time_interval=3):
        self.switch_time_interval = switch_time_interval
        self.shield_states = list(range(0, 2*self.switch_time_interval))
        self.current_state = 0
        self.states = list(range(2*switch_time_interval))
        self.failed = False
        

    def transition(self, action):
        if not self.failed:
            if action == "open":
                if self.current_state < self.switch_time_interval:
                    self.current_state = self.current_state + 1
                elif self.current_state == self.switch_time_interval:
                    self.current_state = self.current_state
                else:
                    self.failed = True
            else:
                if self.current_state >= self.switch_time_interval:
                    self.current_state = (self.current_state + 1)%len(self.shield_states)
                elif self.current_state == 0:
                    self.current_state = self.current_state
                else:
                    self.failed = True

    def next_state(self, current_state, action, failed=False):
        if self.failed:
            return current_state, failed
        else:
            if action == "open":
                if current_state < self.switch_time_interval:
                    return current_state + 1, failed
                elif current_state == self.switch_time_interval:
                    current_state = current_state
                else:
                    failed = True
            else:
                if current_state >= self.switch_time_interval:
                    return (current_state + 1)%len(self.shield_states), failed
                elif current_state == 0:
                    return current_state, failed
                else:
                    failed = True
            return current_state, failed

class WaterTankController():
    def __init__(self, WaterTank, Shield):
        # WaterTank.__init__(self)
        # Shield.__init__(self)
        self.watertank = WaterTank
        self.shield = Shield
        self.action_set = ["open", "close"]
        self.safe_set = set(itertools.product(WaterTank.water_level_states, Shield.shield_states))
        self.current_state = (WaterTank.current_state, Shield.current_state)
        self.failed = WaterTank.failed or Shield.failed
        self.states = list(itertools.product(WaterTank.states, Shield.states))
        print(self.states)

    def transition(self, action):
        if not self.failed:
            self.shield.transition(action)
            self.watertank.transition(action)
            self.current_state = (self.watertank.current_state, self.shield.current_state)
            self.failed =  self.watertank.failed or self.shield.failed

    def next_state(self, current_state, action):
            next1, fail1 = self.watertank.next_state(current_state[0], action)
            next2, fail2 = self.shield.next_state(current_state[1], action)
            next = (next1, next2)
            fail = fail1 or fail2
            return next, fail

# wc = WaterTankController(WaterTank(), Shield())
# print(wc.current_state)
# wc.transition(action="close")
# print(wc.current_state)
# wc.transition(action="open")
# print(wc.current_state)
# print(len(wc.X))
