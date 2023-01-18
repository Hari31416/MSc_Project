from epoch_viz.viz import *
import os

DATA_DIR = "run_1"
ez = EpochViz(DATA_DIR)
res = ez.info()
print(res)

time_range = (25.0, 35.0)
space_range = [0, 4000, 8000]
times_are_nodes = False
space_are_nodes = False
data_types = ["Ey", "Ne"]
data, T, X = ez.load_data(
    data_types=data_types,
    time_range=time_range,
    space_range=space_range,
    times_are_nodes=times_are_nodes,
    space_are_nodes=space_are_nodes,
    return_data=True,
    normalize=True,
    overwrite=True
)

# ez.plot_density_image(
#     normalize=True,
#     time_range=(26.0, 30.0),
#     space_range=(19.5, 20.5),
#     times_are_nodes=False,
#     space_are_nodes=False,
#     cmap = "viridis",
#     aspect="auto",
#     file_name="density.png" 
    
# )

# ez.plot_density_image(
#     normalize=True,
#     time_range=(26.0, 30.0),
#     space_range=(18.5, 20.5),
#     times_are_nodes=False,
#     space_are_nodes=False,
#     cmap = "viridis",
#     aspect="auto",
#     file_name="density.png"
    
# )

ez.plot_ffts(
    field="Ey",
    # xlim=[0, 19],
    plot_lines=True,
    # prefix="fft",
    show_fig=True

)

# ez.plot_fft(
#     node=40000,
#     show_fig=True
# )
