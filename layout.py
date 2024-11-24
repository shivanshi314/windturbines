import os
import numpy as np
import matplotlib.pyplot as plt
from floris import FlorisModel
import floris.layout_visualization as layoutviz
from floris.flow_visualization import visualize_cut_plane
from floris import WindRose
from floris.optimization.layout_optimization.layout_optimization_scipy import (
    LayoutOptimizationScipy,
)


opt_options = {
    "maxiter": 60,
    "disp": True,
    "iprint": 2,
    "ftol": 1e-12,
    "eps": 0.05,
}


fmodel = FlorisModel('jensen.yaml')
wind_directions = np.arange(270, 315, 5.0)
wind_speeds = np.array([8.0])
freq_table = np.zeros((len(wind_directions), len(wind_speeds)))
np.random.seed(1)
freq_table[:,0] = (np.abs(np.sort(np.random.randn(len(wind_directions)))))
freq_table = freq_table / freq_table.sum()

wind_rose = WindRose(
    wind_directions=wind_directions,
    wind_speeds=wind_speeds,
    freq_table=freq_table,
    ti_table=0.06,
)

print(freq_table)

fmodel.set(wind_data=wind_rose)

n = 2
D = 222.0
L = 15000

boundaries = [(0.0, 0.0), (0.0, L), (L, L), (L, 0.0), (0.0, 0.0)]

layout_x = []
layout_y = []
for i in range(n):
    layout_x.append((L//(n-1))*i)
    layout_y.append((L//(n-1))*i)


reversed_layout_y = []
for item in reversed(layout_y):
    reversed_layout_y.append(item)
layout_y = reversed_layout_y
fmodel.set(layout_x=layout_x, layout_y=layout_y)


layout_opt = LayoutOptimizationScipy(fmodel, boundaries, optOptions=opt_options)


sol = layout_opt.optimize()


print("... calculating improvement in AEP")
fmodel.run()
base_aep = fmodel.get_farm_AEP() / 1e6
fmodel.set(layout_x=sol[0], layout_y=sol[1])
fmodel.run()
opt_aep = fmodel.get_farm_AEP() / 1e6

percent_gain = 100 * (opt_aep - base_aep) / base_aep


print("Optimal layout: " + str(sol))
print(
    f"Optimal layout improves AEP by {percent_gain:.1f}% "
    f"from {base_aep:.1f} MWh to {opt_aep:.1f} MWh"
)
layout_opt.plot_layout_opt_results()

plt.show()
