
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams["font.size"] = 14
import glob
import sdf
import tqdm
from scipy.integrate import quad
from epoch_viz.viz import EpochViz


def prepare(p):

    DIR = f"SG_{p}"

    ez = EpochViz(DIR,'density_plots') 

    time_range =(27, 37)
    space_range = (19.5, 20.5)
    space_are_nodes = False
    time_are_nodes = False
    fig, ax = ez.plot_density_image(
    normalize=True,
    time_range=time_range,
    space_range=space_range,
    space_are_nodes=space_are_nodes,
    times_are_nodes=time_are_nodes,
    show_fig=False,
    title=f"SG_{p}",
    aspect="auto",
    file_name=f"SG_{p}",)


if __name__ == "__main__":
    ps = [2, 4, 6, 8, 10, 12]
    for p in ps:
        prepare(p)


