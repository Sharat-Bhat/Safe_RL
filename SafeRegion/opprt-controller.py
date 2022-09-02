import numpy as np
from state_machine import WaterTankController, WaterTank, Shield

def calculate_sets(wc, action_set, num_iter=1000):
    rc_set = wc.safe_set.copy()
    ss_set = rc_set.copy()
    for i in range(num_iter+1):
        # rem_elem = set()
        for state in list(rc_set):
            # next = []
            fail = []
            for action in action_set:
                next1, fail1 = wc.next_state(current_state=state, action=action)
                # next.append(next1)
                fail.append(fail1 or (next1 not in rc_set))
            
            fail = np.array(fail)
            if np.all(fail):
                rc_set.discard(state)
                ss_set.discard(state)
                # print(state, " removed.", fail)
            if np.any(fail):
                ss_set.discard(state)
                # print(state, " removed.", fail)
            #     # rem_elem.add(state)
            #     ss_set.discard(state)
            # elif not np.all(fail):
            #     ss_set.discard(state)
        # rc_set = rc_set.difference(rem_elem)
        if i%100 == 0:
            print("Iter:", i, "Set: ",len(wc.safe_set), " RC Set:", len(rc_set), "SS Set:", len(ss_set))
    return rc_set, ss_set

wc = WaterTankController(WaterTank(water_capacity=10), Shield(switch_time_interval=3))
# print(wc.current_state)
# wc.transition(action="close")
# print(wc.current_state)
# wc.transition(action="open")
# print(wc.current_state)
# print(len(wc.safe_set))

safe_set = wc.safe_set.copy()
rc_set = safe_set.copy()
strengthen_safety_set = safe_set.copy()
action_set = ["close", "open"]
rc_set, ss_set = calculate_sets(wc, action_set)
rc_set = list(rc_set)
rc_set.sort()
# print(rc_set)                
print(wc.next_state((1,5), action="close"))


