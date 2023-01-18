from epoch_viz.viz import *
import os

if not os.path.exists(".temp"):
    os.mkdir(".temp")
DATA_DIR = "run_2"
ez = EpochViz(DATA_DIR, ".temp")
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
    file_name = "density.png",
    cmap = "viridis",
    aspect="auto",
    interpolation="none",
    vmin=0.0,
    vmax=10,
    show_fig=False
)
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
    ylim=(1e-1, 1e3),
    prefix="run_2",
    format="png",
    ylog=True,
    plot_lines=True,
    show_fig = False,
    return_fig = False,
)
    
