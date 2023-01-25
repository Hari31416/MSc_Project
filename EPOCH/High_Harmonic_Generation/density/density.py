from epoch_viz.viz import EpochViz
import numpy as np
import matplotlib.pyplot as plt
import os
from style import cprint
from scipy.signal import hilbert

SAVE_DIR = "density_images"
plt.rcParams["figure.figsize"] = (9, 6)


def main(DIR):
    cprint(f"\nProcessing {DIR}...", "green")
    ez = EpochViz(DIR, SAVE_DIR)
    info = ez.info()
    FACTOR = ez.deck_info["FACTOR"]

    time_range = (29.0, 33.0)
    space_range = (19.8, 20.2)
    times_are_nodes = False
    space_are_nodes = False
    vmax = min(FACTOR * 2, 20)
    vmin = None

    # Plotting density image
    fig, ax = ez.plot_density_image(
        normalize=True,
        time_range=time_range,
        space_range=space_range,
        times_are_nodes=times_are_nodes,
        space_are_nodes=space_are_nodes,
        cmap="viridis",
        aspect="auto",
        show_fig=False,
        vmax=vmax,
        vmin=vmin,
        # file_name=f"density_raw_{FACTOR}.png",
        # title=f"Raw Density Factor: {FACTOR}",
    )

    ## Potting the envelope lines
    Ts = np.linspace(ax.get_ylim()[0], ax.get_ylim()[1], ez.time_nodes.shape[0])
    Xs = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], ez.space_nodes.shape[0])
    Ts = Ts[::-1]

    # Gradient
    grad = np.gradient(ez.data["Ne"])
    max_grad = np.argmax(grad[1], axis=1)

    # Threshold
    first = np.zeros(ez.data["Ne"].shape[0], dtype=int)
    for i in range(ez.data["Ne"].shape[0]):
        nonzeros = np.where(ez.data["Ne"][i] > ez.deck_info["FACTOR"] / 3)[0]
        if len(nonzeros) > 0:
            first[i] = nonzeros[0]

    # Hilbert
    h = hilbert(ez.data["Ne"])
    h = np.abs(h)
    hilbert_points = np.zeros(h.shape[0], dtype=int)
    for i in range(h.shape[0]):
        nonzeros = np.where(h[i] > 2)[0]
        if len(nonzeros) > 0:
            nonzeros_f = nonzeros[nonzeros > 50]
            hilbert_points[i] = nonzeros_f[0]

    # Mean
    mean = (0.5 * Xs[max_grad] + 1.5 * Xs[hilbert_points] + 3 * Xs[first]) / 5

    # Plotting the lines on figure
    ax.lines.clear()
    ax.plot(Xs[max_grad], Ts, color="red", linewidth=1.5, label="Gradient")
    ax.plot(Xs[first], Ts, color="black", linewidth=1.5, label="Threshold")
    ax.plot(Xs[hilbert_points], Ts, color="green", linewidth=1.5, label="Hilbert")
    ax.plot(mean, Ts, color="blue", linewidth=1.5, label="Mean")
    ax.legend()
    ax.set_title(f"Density with Envelopes Density: {FACTOR}")
    fig.savefig(os.path.join(SAVE_DIR, f"density_{FACTOR}.png"))
    plt.close()

    # Plotting just the threshold line on figure
    ax.lines.clear()
    ax.plot(Xs[first], Ts, color="black", linewidth=1.5, label="Threshold")
    ax.legend()
    ax.set_title(f"Density with Envelopes Density: {FACTOR}")
    fig.savefig(os.path.join(SAVE_DIR, f"density_just_threshold_{FACTOR}.png"))
    plt.close()

    # PLotting the gradient line
    plt.figure()
    plt.plot(Xs[max_grad], Ts)
    plt.xlabel("X $[\lambda]$")
    plt.ylabel(r"T $[\tau]$")
    plt.title(f"Gradient Factor: {ez.deck_info['FACTOR']}")
    plt.savefig(os.path.join(SAVE_DIR, f"gradient_line_{FACTOR}.png"))
    plt.close()

    # PLotting the threshold line
    plt.figure()
    plt.plot(Xs[first], Ts)
    plt.xlabel("X $[\lambda]$")
    plt.ylabel(r"T $[\tau]$")
    plt.title(f"Threshold Factor: {ez.deck_info['FACTOR']}")
    plt.savefig(os.path.join(SAVE_DIR, f"threshold_line_{FACTOR}.png"))
    plt.close()

    # PLotting the hilbert line
    plt.figure()
    plt.plot(Xs[hilbert_points], Ts)
    plt.xlabel("X $[\lambda]$")
    plt.ylabel(r"T $[\tau]$")
    plt.title(f"Hilbert Factor: {ez.deck_info['FACTOR']}")
    plt.savefig(os.path.join(SAVE_DIR, f"hilbert_line_{FACTOR}.png"))
    plt.close()

    # PLotting the mean line
    plt.figure()
    plt.plot(mean, Ts)
    plt.xlabel("X $[\lambda]$")
    plt.ylabel(r"T $[\tau]$")
    plt.title(f"Mean Factor: {ez.deck_info['FACTOR']}")
    plt.savefig(os.path.join(SAVE_DIR, f"mean_line_{FACTOR}.png"))
    plt.close()


if __name__ == "__main__":
    dirs = os.listdir()
    dirs = [dir for dir in dirs if os.path.isdir(dir)]
    f_dirs = []
    excludes = ["images", ".ipynb_checkpoints", "density_images"]
    for dir in dirs:
        if dir not in excludes:
            f_dirs.append(dir)
    for dir in f_dirs:
        # print(dir)
        main(dir)
    # main("run_1")
