import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import colors
import sdf
import re
import glob
import tqdm
import sys

def main(DATA_DIR):
    plt.rcParams["font.size"] = 14
    plt.rcParams["figure.figsize"] = (10, 8)


    m = 9.10938356e-31
    e = 1.60217662e-19
    c = 299792458
    PI = np.pi
    epsilon = 8.85e-12

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

    # ## Calculated Constants

    omega0 = 2 * PI * c / LAMBD
    tau = 2 * PI / omega0
    nc = epsilon * m * omega0**2 / e**2
    Er = m * omega0 * c / e
    n0 = FACTOR * nc
    LAS_TIME = LAS_TIME * tau
    # print("Calculated Values for the simulation are:")
    # print("omega0 = ", omega0)
    # print("tau = ", tau)
    # print("nc = ", nc)
    # print("Er = ", Er)
    # print("n0 = ", n0)

    # ## Values for FT

    omega_to_resolve = 20 * omega0
    f_max_to_resolve = omega_to_resolve / (2 * PI)
    dt_max_to_resolve = 1 / (2 * f_max_to_resolve)
    # print(f"The maximum time step for resolution is {dt_max_to_resolve*1e15} femto seconds")

    f_max = 1 / (DT)
    omega_max = 2 * np.pi * f_max
    omega_max / omega0

    # ## Other Variables

    ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
    ALL_FILES.sort()

    Et0 = np.zeros(len(ALL_FILES))
    Et1 = np.zeros(len(ALL_FILES))
    Et2 = np.zeros(len(ALL_FILES))
    d = np.zeros((len(ALL_FILES), NX))
    for i in tqdm.tqdm(range(len(ALL_FILES)), desc="Getting Data..."):
        data = sdf.read(ALL_FILES[i])
        ey = data.Electric_Field_Ey.data
        Et0[i] = ey[7940]
        Et1[i] = ey[4000]
        Et2[i] = ey[8000]
        d[i] = data.Derived_Number_Density_Electron.data

    d = d / nc

    t_start = 1300
    t_end = 1500
    t_max = d.shape[0]
    x_max = d.shape[1]
    x_start = 2 * 3950
    x_end = 2 * 4100
    EXTENT = [
        -X_MIN * (x_start - NX // 2) / x_max,
        -X_MIN * (x_end - NX // 2) / x_max,
        T_MAX * t_end / t_max,
        T_MAX * t_start / t_max,
    ]
    print("Saving Density Plot")
    plt.figure()
    plt.imshow(d[t_start:t_end, x_start:x_end], aspect="auto", extent=EXTENT, cmap="jet", vmax=10, vmin=-10)
    cmap = colors.ListedColormap(["white", "black"])
    plt.colorbar(cmap=cmap)
    plt.savefig(f"images/density_{FACTOR}.png", dpi=300)

    Et0 = Et0 / np.max(Et0)
    Et1 = Et1 / np.max(Et1)
    Et2 = Et2 / np.max(Et2)
    y0 = np.fft.fft(Et0)
    y1 = np.fft.fft(Et1)
    y2 = np.fft.fft(Et2)
    y0_shift = np.fft.fftshift(y0)
    y1_shift = np.fft.fftshift(y1)
    y2_shift = np.fft.fftshift(y2)
    y0_f = np.abs(y0_shift)
    y1_f = np.abs(y1_shift)
    y2_f = np.abs(y2_shift)

    print("Saving plot 1")
    plt.figure()
    omega = np.linspace(-omega_max / 2, omega_max / 2, len(ALL_FILES))
    plt.plot(omega / omega0, 2 * np.abs(y0_f) * 2)
    plt.yscale("log")
    points = np.arange(1, 21, 2)
    for p in points:
        plt.axvline(p, color="red", linestyle="--")
        plt.annotate(f"{p}", (p, 1e-2))
    plt.xlim(0, 20)
    plt.grid()
    plt.title("Node 7940")
    plt.ylim(0.1, 1e3)
    plt.savefig(f"images/node7940_{FACTOR}.png", dpi=300)

    print("Saving plot 2")
    plt.figure()
    plt.plot(omega / omega0, 2 * np.abs(y1_f) * 2)
    plt.yscale("log")
    points = np.arange(1, 21, 2)
    for p in points:
        plt.axvline(p, color="red", linestyle="--")
        plt.annotate(f"{p}", (p, 1e-2))
    plt.xlim(0, 20)
    plt.grid()
    plt.ylim(0.1, 1e3)
    plt.title("Reflected Node 4000")
    plt.savefig(f"images/node4000_{FACTOR}.png", dpi=300)

    print("Saving plot 3")
    plt.figure()
    plt.plot(omega / omega0, 2 * np.abs(y2_f) * 2)
    plt.yscale("log")
    points = np.arange(1, 21, 2)
    for p in points:
        plt.axvline(p, color="red", linestyle="--")
        plt.annotate(f"{p}", (p, 1e-2))
    plt.xlim(0, 20)
    plt.grid()
    plt.title("Reflected Node 8000")
    plt.ylim(0.1, 1e3)
    plt.savefig(f"images/node8000_{FACTOR}.png", dpi=300)

if __name__ == "__main__":
    main(sys.argv[1])