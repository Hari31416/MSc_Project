import sdf_helper as sh
import matplotlib.pyplot as plt
import os
from matplotlib import colors

import sdf

plt.rcParams["font.size"] = 13
import numpy as np

EXTENT = [-20, 20, -20, 20]
all_files = [f for f in os.listdir(".") if f.endswith(".sdf")]


def plot_field(data_dir, ax, component="y"):
    raw_data = sdf.read(data_dir)
    comp = {
        "x": raw_data.Electric_Field_Ex,
        "y": raw_data.Electric_Field_Ey,
        "z": raw_data.Electric_Field_Ez,
    }
    field = comp[component].data
    t = raw_data.Header["time"] * 1e15
    field = field / (field.max() + 1e-10)
    ax.imshow(
        field.T,
        cmap="coolwarm",
        origin="lower",
        extent=EXTENT,
        aspect="auto",
        interpolation="nearest",
        # norm=colors.Normalize(vmin=-0.3, vmax=0.5),
    )
    ax.set_xlabel("$y \, [\mu m]$")
    ax.set_ylabel("$x \, [\mu m]$")
    ax.set_title(f"t = {t:.0f} fs")


def get_field(id, component):
    raw_data = sdf.read(all_files[id])
    comp = {
        "x": raw_data.Electric_Field_Ex,
        "y": raw_data.Electric_Field_Ey,
        "z": raw_data.Electric_Field_Ez,
    }
    field = comp[component].data
    return field


def plot_with_scale(data_dir, component="x"):
    raw_data = sdf.read(data_dir)
    comp = {
        "x": raw_data.Electric_Field_Ex,
        "y": raw_data.Electric_Field_Ey,
        "z": raw_data.Electric_Field_Ez,
    }
    field = comp[component]

    t = raw_data.Header["time"] * 1e15
    c_label = f"$(E_{component})^2$ in $({field.units})^2$"

    plt.figure(figsize=(15, 8))
    plt.imshow(
        field.data.T, cmap="coolwarm", origin="lower", extent=EXTENT, aspect="auto",
    )
    plt.xlabel("$Y \, [\mu m]$")
    plt.ylabel("$X \, [\mu m]$")
    plt.title(f"t = {t:.0f} fs")
    cbar = plt.colorbar()
    cbar.ax.set_ylabel(c_label)
    plt.show()


if __name__ == "__main__":
    fig, ax = plt.subplots(3, 4, figsize=(25, 22))
    i = 0
    component = "y"
    field = f"E_{component}"
    fig.suptitle(rf"$({field})^2$" + r"in $({\frac{V}{m}})^2$", fontsize=18)
    i = 0
    for data_dir in all_files:
        t = i * 10
        plot_field(data_dir, ax[i // 4, i % 4], component=component)
        i += 1
    fig.tight_layout()
    plt.show()

    plot_with_scale("0008.sdf", component="y")
