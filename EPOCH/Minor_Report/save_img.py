import sdf
import matplotlib.pyplot as plt
from matplotlib import colors
import sys
import os, glob
import numpy as np


def save_density(directory):
    all_files = glob.glob(os.path.join(os.curdir, directory, "*.sdf"))
    all_files.sort()
    D = []
    input_deck = os.path.join(os.curdir, directory, "input.deck")
    with open(input_deck, "r") as f:
        lines = f.readlines()
    a = lines[7].strip().split(" ")[-1]
    for i, file in enumerate(all_files):
        data = sdf.read(file)
        D.append(data.Derived_Number_Density_Electron.data)

    plt.imshow(np.array(D), aspect="auto", cmap="gray")
    cmap = colors.ListedColormap("gray")
    plt.colorbar(cmap=cmap)
    file_name = f"{directory}_{a}.jpg"
    file_dir = os.path.join("Images", file_name)
    plt.title(file_name)
    plt.savefig(file_dir)


if __name__ == "__main__":
    save_density(sys.argv[1])
