import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from state_machine import WaterTankController, WaterTank, Shield

def create_graph(wc):
    num_states = len(wc.states)+1
    gi = np.zeros((2, num_states, num_states)) # Incidence Matrix of Graph

    # Close = 0, open=1
    # -1 state is fail state
    gi[0][-1][-1] = 1
    gi[1][-1][-1] = 1

    # Close
    steps = list(range(-wc.watertank.inflow[1], -wc.watertank.inflow[0]+1))
    wt_in_num_states = len(steps)
    wt_in_prob = np.ones(wt_in_num_states)/wt_in_num_states
    steps = list(range(wc.watertank.outflow[0], wc.watertank.outflow[1]+1))
    wt_out_num_states = len(steps)
    wt_out_prob = np.ones(wt_out_num_states)/wt_out_num_states
    for i in range(len(wc.states)):
        s1, s2 = wc.states[i]
        s2_next, fail = wc.shield.next_state(s2, "close")
        if fail:
            gi[0][i][-1] = 1
        else:
            for j in range(len(steps)):
                if s1 - steps[j] >= 0 and s1 - steps[j] < wc.watertank.water_capacity:
                    gi[0][i][(s1-steps[j])*len(wc.shield.states) + s2_next] += wt_out_prob[j]
                else:
                    gi[0][i][-1] += wt_out_prob[j]

    # Open
    steps = list(range(wc.watertank.outflow[0] - wc.watertank.inflow[1], wc.watertank.outflow[1] - wc.watertank.inflow[0]+1))
    wt_num_states = len(steps)
    wt_prob = np.convolve(wt_out_prob, wt_in_prob)

    for i in range(len(wc.states)):
        s1, s2 = wc.states[i]
        s2_next, fail = wc.shield.next_state(s2, "open")
        if fail:
            gi[1][i][-1] = 1
        else:
            for j in range(len(steps)):
                if s1 - steps[j] >= 0 and s1 - steps[j] < wc.watertank.water_capacity:
                    gi[1][i][(s1-steps[j])*len(wc.shield.states) + s2_next] += wt_prob[j]
                else:
                    gi[1][i][-1] += wt_prob[j]
    return gi

def find_safe_states(wc, min_prob=1):
    gi = create_graph(wc)
    print(gi)
    unsafe = np.logical_and((gi[0, :, -1] > 1-min_prob).astype(int), gi[1, :, -1] > 1-min_prob)
    prev_unsafe = np.zeros(unsafe.shape).astype(bool)
    while (prev_unsafe != unsafe).any():
        prev_unsafe = unsafe
        close_unsafe = np.sum(prev_unsafe*gi[0, :, :], axis=1)
        close_unsafe = (close_unsafe > 1-min_prob)
        # print(close_unsafe)
        open_unsafe = np.sum(prev_unsafe*gi[1, :, :], axis=1)
        open_unsafe = (open_unsafe > 1-min_prob)
        # print(open_unsafe)
        unsafe =np.logical_or(np.logical_and(close_unsafe, open_unsafe), prev_unsafe)

    unsafe = unsafe[:-1]
    # print(unsafe)
    
    states_grid = unsafe.reshape((len(wc.watertank.states), len(wc.shield.states))).astype(int)
    print(states_grid)
    return states_grid

def get_safety_map(wc, iterations=100):
    gi = create_graph(wc)
    print(gi)
    safemap = np.zeros(len(wc.states)+1)
    safemap[-1] = 1
    for i in range(iterations):
        temp = gi*safemap.reshape((1,-1))
        temp = np.sum(temp, axis=-1)
        safemap = np.min(temp, axis=0)
        print(safemap)
    safemap = safemap[:-1].reshape((len(wc.watertank.states), len(wc.shield.states)))
    return safemap

wc = WaterTankController(WaterTank(water_capacity=100, init_level=3, inflow = (1, 2), outflow = (0, 1)), 
                            Shield(switch_time_interval=20))

unsafe_states_grid = find_safe_states(wc, min_prob=1)
safety_map = get_safety_map(wc, iterations=100)

plt.imshow(unsafe_states_grid.T)
plt.title("Unsafe States Plot")
plt.colorbar()
plt.show()

plt.imshow(safety_map.T)
plt.title("Safety Map Plot")
plt.colorbar()
plt.show()