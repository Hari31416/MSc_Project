import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import sdf
import re
import glob, os
import tqdm
from style import cprint

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = "Ubuntu"
plt.rcParams["font.monospace"] = "Ubuntu Mono"
plt.rcParams["font.size"] = 18
plt.rcParams["axes.labelsize"] = 20
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titlesize"] = 18
plt.rcParams["figure.figsize"] = (10, 8)

m = 9.10938356e-31
e = 1.60217662e-19
c = 299792458
PI = np.pi
epsilon = 8.85e-12


def main(
    data_dir,
    save_figs=False,
    fig_dir=None,
    show_figs=False,
    plot_density=False,
    plot_density_2d=False,
    plot_ffts=False,
    plot_fields2d=False,
    plot_fields_with_time=False,
    return_data=False,
):
    DATA_DIR = data_dir
    with open(os.path.join(DATA_DIR, "input.deck"), "r") as myfile:
        data = myfile.read()

    def find_value(info):
        regex = re.compile(rf"\s{info}\s*=\s*-?(\d+\.?\d*)")
        match = regex.search(data)
        if match:
            return float(match.group(1))
        else:
            return None

    LAMBD = find_value("lambda0") * 1e-6
    LAS_TIME = int(find_value("las_time"))
    T_MAX = int(find_value("t_end"))
    DT = find_value("dt_snapshot") * 1e-15
    A0 = find_value("a0")
    FACTOR = int(find_value("factor"))
    NX = int(find_value("nx"))
    X_MIN = -int(find_value("x_min"))
    # print("Values from input.deck:")
    # print("lambda0 = ", LAMBD)
    # print("laser_time = ", LAS_TIME)
    # print("t_end = ", T_MAX)
    # print("dt_snapshot = ", DT)
    # print("a0 = ", A0)
    # print("factor = ", FACTOR)
    # print("nx = ", NX)
    # print("x_min = ", X_MIN)

    omega0 = 2 * PI * c / LAMBD
    tau = 2 * PI / omega0
    nc = epsilon * m * omega0**2 / e**2
    Er = m * omega0 * c / e
    n0 = FACTOR * nc
    LAS_TIME = LAS_TIME * tau
    f_max = 1 / (DT)
    omega_max = 2 * np.pi * f_max
    # print("Calculated Values for the simulation are:")
    # print("omega0 = ", omega0)
    # print("tau = ", tau)
    # print("nc = ", nc)
    # print("Er = ", Er)
    # print("n0 = ", n0)
    # print("LAS_TIME = ", LAS_TIME)
    # print("f_max = ", f_max)
    # print("omega_max = ", omega_max / omega0)

    ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
    ALL_FILES.sort()
    X = np.linspace(X_MIN, -X_MIN, NX)
    T = np.linspace(0, T_MAX, len(ALL_FILES))

    def get_image_file_name(name):
        name = f"{DATA_DIR}_{name}"
        if name.endswith(".png"):
            return os.path.join(fig_dir, name)

        return os.path.join(fig_dir, name + ".png")

    if plot_density:
        data = sdf.read(ALL_FILES[100])
        plt.plot(X, data.Derived_Number_Density_Electron.data / nc)
        plt.xlabel("X")
        plt.ylabel("$n_0/n_c$")
        if show_figs:
            plt.show()
        if save_figs:
            plt.savefig(get_image_file_name("density"))
        plt.close()

    def time_node(time):
        max_time = T.max()
        all_files = len(ALL_FILES)
        return int((time / max_time) * all_files)

    Eys = np.zeros((len(ALL_FILES), NX))
    densities = np.zeros((len(ALL_FILES), 800))
    for i in tqdm.tqdm(range(len(ALL_FILES)), desc="Getting Data..."):
        data = sdf.read(ALL_FILES[i])
        dens = data.Derived_Number_Density_Electron.data / nc
        densities[i] = dens[NX // 2 - 600 : NX // 2 + 200]
        ey = data.Electric_Field_Ey.data
        Eys[i] = ey

    start_time_node = time_node(18)
    densities = densities[start_time_node:]

    def plot_density_2d_function():
        extent = [-1.5, 0.5, T.max(), 18]
        plt.figure()
        plt.imshow(densities, aspect="auto", extent=extent, cmap="jet")
        plt.xlabel("X $[\lambda]$")
        plt.ylabel("T $[\\tau]$")
        plt.colorbar()
        if show_figs:
            plt.show()
        if save_figs:
            plt.savefig(get_image_file_name("density_2d"))
        plt.close()

    if plot_density_2d:
        plot_density_2d_function()

    def plot_fft(
        Ey,
        omegas,
        lines=False,
        xlim=(0, 20),
        ylim=None,
        fig_name=None,
        return_data=False,
    ):
        Ey_fft = np.fft.fft(Ey)
        Ey_fft = np.fft.fftshift(Ey_fft)
        Ey_fft = np.abs(Ey_fft)
        Ey_fft = Ey_fft / Ey_fft.max()
        plt.figure()
        plt.plot(omegas, Ey_fft)
        plt.xlabel("Frequency")
        plt.ylabel("Amplitude")
        plt.yscale("log")
        plt.title(fig_name)
        points = np.arange(1, 21, 2)
        if lines:
            for point in points:
                plt.axvline(point, color="red", linestyle="--")
        if xlim:
            plt.xlim(xlim)
        if ylim:
            plt.ylim(ylim)
        plt.xticks(points)
        if show_figs:
            plt.show()
        if save_figs:
            plt.savefig(get_image_file_name(fig_name))
        plt.close()
        if return_data:
            return Ey_fft, omegas

    omegas = np.linspace(-omega_max / 2, omega_max / 2, len(ALL_FILES))
    omegas = omegas / omega0
    if plot_ffts:
        # ids = [0, 5000, 7000, 7600, 7700, 7800, 7900, 8000]
        ids = [7000, 7600, 7700, 7800, 8000]
        for id_ in ids:
            fig_name = f"ffty_{id_}"
            data = plot_fft(
                Eys[:, id_],
                omegas,
                lines=True,
                fig_name=fig_name,
                ylim=(1e-4, 1),
                return_data=return_data,
            )
            if return_data:
                Ey_fft, omegas = data
                file_name_to_save = os.path.join(fig_dir, f"{DATA_DIR}_ffty_{id_}.npz")
                np.savez(
                    file_name_to_save,
                    Ey_fft=Ey_fft,
                    omegas=omegas,
                )

    def plot_field():
        extent = [X_MIN, -X_MIN, T_MAX, 0]
        plt.figure()
        plt.imshow(Eys, aspect="auto", extent=extent, cmap="jet")
        plt.xlabel("X in $\lambda$")
        plt.ylabel("T in $\tau$")
        plt.colorbar()
        if show_figs:
            plt.show()
        if save_figs:
            plt.savefig(get_image_file_name("field2d"))
        plt.close()

    if plot_fields2d:
        plot_field()

    def plot_one_e_fileld(id_, ax):
        raw_data = sdf.read(ALL_FILES[id_])
        ey = raw_data.Electric_Field_Ey.data
        ey = ey / np.max(ey)
        time = raw_data.Header["time"]
        ax.plot(X, ey)
        ax.set_xlabel("X")
        ax.set_ylabel("$E_y$")
        ax.set_title(f"t = {time*1e15:.2f} fs")

    def plot_fields_with_time_function():
        figs = 25
        n = int(np.sqrt(figs))
        fig, axes = plt.subplots(n, n, figsize=(n * 4, n * 4))
        ids = np.linspace(50, len(ALL_FILES) - 1, figs).astype(int)
        for i, ax in enumerate(axes.flatten()):
            plot_one_e_fileld(ids[i], ax)
            if i < figs - n:
                ax.set_xticks([])
                ax.set_xlabel("")
            if i % n > 0:
                ax.set_yticks([])
                ax.set_ylabel("")
        plt.tight_layout()
        if show_figs:
            plt.show()
        if save_figs:
            plt.savefig(get_image_file_name("field_with_time"))
        plt.close()

    if plot_fields_with_time:
        plot_fields_with_time_function()


if __name__ == "__main__":
    # data_dir = [f"run_{i}" for i in range(12, 21, 2)]
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fig_dir = "images_1"
    data_dir = ["run", "run_9"]

    # for d in data_dir:
    #     cprint("====" * 10, "red")
    #     cprint(f"Ruuning {d}", "green")
    #     os.chdir(os.path.join(file_dir, d))
    #     os.system("echo '.' | epoch1d")
    #     os.chdir(file_dir)
    #     cprint("====" * 10, "red")

    plot_density = False
    plot_ffts = True
    plot_fields2d = True
    plot_fields_with_time = True
    show_figs = False
    save_figs = True
    plot_density_2d = True
    return_data = False

    for dir in data_dir:
        cprint("====" * 10, "red")
        cprint(f"Processing {dir}", "green")
        main(
            data_dir=dir,
            save_figs=save_figs,
            show_figs=show_figs,
            plot_density=plot_density,
            plot_ffts=plot_ffts,
            plot_fields2d=plot_fields2d,
            plot_fields_with_time=plot_fields_with_time,
            fig_dir=fig_dir,
            plot_density_2d=plot_density_2d,
            return_data=return_data,
        )
        cprint("====" * 10, "red")