from epoch_viz.viz import *
import os


DATA_DIR = "run_1"
ez = EpochViz(DATA_DIR)
res = ez.info()
print(res)

#Plotting density

time_range = (25.0, 35.0)
space_range = (19.5, 20.5)
times_are_nodes = False
space_are_nodes = False
fig, ax = ez.plot_density_image(
    normalize=True,
    time_range=time_range,
    space_range=space_range,
    times_are_nodes=times_are_nodes,
    space_are_nodes=space_are_nodes,
    cmap = "viridis",
    aspect="auto",
    interpolation="none",
    vmin=0.0,
    vmax=10,
    show_fig=False
)
plt.show(fig)
#Plotting FFT
data, T, X = ez.load_data(
    data_types=["Ey"],
    space_range=[0, 4000, 8000],
    space_are_nodes=True,
    return_data=True,
    normalize=True,
    overwrite=True
)

f = ez.plot_ffts(
    field="Ey",
    xlim="max",
    ylim=None,
    prefix=None,
    format="png",
    ylog=True,
    plot_lines=False,
    show_fig = True,
    return_fig = False,
)
    