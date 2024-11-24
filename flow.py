import os
import numpy as np
import matplotlib.pyplot as plt
from floris import FlorisModel
import floris.layout_visualization as layoutviz
from floris.flow_visualization import visualize_cut_plane

fmodel = FlorisModel("jensen.yaml")

fmodel.set(layout_x=[0, 300], layout_y=[0, 0])
fmodel.set(
    wind_directions=np.array([270.0]), wind_speeds=[8.0], turbulence_intensities=np.array([0.06])
)

fmodel.run()

fig, axarr = plt.subplots(1, 1, figsize=(8, 5), sharex=False, layout="constrained")
MIN_WS = 0
MAX_WS = 8

horizontal_plane = fmodel.calculate_horizontal_plane(height=90.0)
visualize_cut_plane(
    horizontal_plane,
    ax=axarr,
    min_speed=MIN_WS,
    max_speed=MAX_WS,
)

layoutviz.plot_turbine_points(fmodel, ax=axarr, plotting_dict={"color": "w"})
layoutviz.plot_turbine_rotors(fmodel, ax=axarr)
axarr.set_title("Wake Visualisation")
axarr.set_xlabel("x (m)")
axarr.set_ylabel("y (m)")

plt.show()
