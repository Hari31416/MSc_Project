import matplotlib.pyplot as plt
import numpy as np
import sdf
import glob

plt.rcParams["font.size"] = 14
plt.rcParams["figure.figsize"] = (10, 8)

DATA_DIR = "7run"
ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
ALL_FILES.sort()
POINTS = len(ALL_FILES)

EXTENT = [-10, 10, -10, 10]

raw_data = sdf.read(ALL_FILES[0])

lambd = 1e-6
c = 3e8
omega = 2 * np.pi * c / lambd
n_c = omega * omega / (4 * np.pi * np.pi * 81)

plt.imshow(raw_data.Derived_Number_Density_Electron.data.T / n_c)
plt.colorbar()
plt.savefig("density.png")


def plot_field(data_dir, ax, component="y"):
    raw_data = sdf.read(data_dir)
    comp = {
        "x": raw_data.Electric_Field_Ex,
        "y": raw_data.Electric_Field_Ey,
        "z": raw_data.Electric_Field_Ez,
    }
    field = comp[component].data.T
    t = raw_data.Header["time"] * 1e15
    field = field / (field.max() + 1e-10)
    ax.imshow(
        field**2,
        cmap="jet",
        origin="lower",
        extent=EXTENT,
        aspect="auto",
        # interpolation='nearest',
    )
    ax.set_xlabel("$x \, [\mu m]$")
    ax.set_ylabel("$y \, [\mu m]$")
    ax.set_title(f"t = {t:.1f} fs")


def get_field(id, component):
    raw_data = sdf.read(ALL_FILES[id])
    comp = {
        "x": raw_data.Electric_Field_Ex,
        "y": raw_data.Electric_Field_Ey,
        "z": raw_data.Electric_Field_Ez,
    }
    field = comp[component].data.T
    return field


# plot_field(ALL_FILES[-10], plt.gca(), component="y")

fig, ax = plt.subplots(4, 2, figsize=(25, 22))
ax = ax.flatten()
i = 0
for dir in ALL_FILES[:-8]:
    plot_field(dir, ax[i], component="y")
    i += 1
    if i == 8:
        break
plt.tight_layout()
plt.savefig("field.png")

import os

file_dir = os.path.dirname(os.path.realpath(__file__))
