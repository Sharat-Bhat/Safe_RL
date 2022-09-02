import numpy as np
from state_machine import WaterTankController, WaterTank, Shield

wc = WaterTankController(WaterTank(water_capacity=10, init_level=50, inflow = (1, 2), outflow = (0, 1)), 
                            Shield(switch_time_interval=3))

action_set = wc.actions

