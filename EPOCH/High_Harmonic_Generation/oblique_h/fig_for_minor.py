import matplotlib.pyplot as plt
import numpy as np
import os
import sdf
import re
import glob
from tqdm import tqdm
from style import *
from tabulate import tabulate

plt.rcParams["font.size"] = 20
plt.rcParams["figure.figsize"] = (10, 8)

c = 299792458
PI = np.pi
pi = PI
m = 9.10938356e-31
e = 1.60217662e-19
C1 = "#067802"
C2 = "#1c84c9"


def plot(data_dir, save_dir=".", show_fig=True, file_name=None):
    DATA_DIR = data_dir
    SAVE_DIR = save_dir
    ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
    ALL_FILES.sort()
    POINTS = len(ALL_FILES)

    with open(os.path.join(DATA_DIR, "input.deck"), "r") as myfile:
        data = myfile.read()

    def find_value(info):
        regex = re.compile(rf"\s{info}\s*=\s*-?(\d+\.?\d*)")
        regex2 = re.compile(rf"\s*{info}\s*=\s*(.*)\n")
        match = regex.search(data)
        match2 = regex2.search(data)

        if match:
            return float(match.group(1))

        if match2:
            return float(eval(match2.group(1)))
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
    ANGLE = find_value("alpha")
    pol = find_value("polarisation")

    if pol is None:
        POL_TYPE = "p"
        POL_ANGLE = 0
    else:
        if float(pol) == 90.0:
            POL_ANGLE = 90
            POL_TYPE = "s"
        else:
            POL_ANGLE = float(pol)
            POL_TYPE = "p"

    beta = np.cos((ANGLE))
    tan_factor = np.tan((ANGLE))

    lambda_0 = LAMBD
    omega_0 = 2 * PI * c / lambda_0
    tau_0 = 2 * PI / omega_0

    lambda_m = LAMBD / beta
    omega_m = 2 * PI * c / lambda_m
    tau_m = 2 * PI / omega_m
    dt_m = DT
    dt_l = DT

    lambda_l = lambda_0
    omega_l = omega_0
    tau_l = tau_0

    LAS_TIME_L = LAS_TIME * tau_l
    LAS_TIME_M = LAS_TIME * tau_m
    T_MAX_L = T_MAX * tau_l
    T_MAX_M = T_MAX * tau_m

    ErM = (m * omega_m * c) / e
    ErL = (m * omega_l * c) / e

    L_frame_info = {
        "lambda": lambda_l,
        "tau": tau_l,
        "omega": omega_l,
        "laser_time": LAS_TIME_L,
        "t_end": T_MAX_L,
        "dt_dump": dt_l,
        "a0": A0,
        "factor": FACTOR,
        "nx": NX,
        "x_min_natural": X_MIN * lambda_l,
        "x_min": X_MIN,
    }

    M_frame_info = {
        "lambda": lambda_m,
        "tau": tau_m,
        "omega": omega_m,
        "laser_time": LAS_TIME_M,
        "t_end": T_MAX_M,
        "dt_dump": dt_m,
        "a0": A0,
        "factor": FACTOR,
        "nx": NX,
        "x_min_natural": X_MIN * lambda_m,
        "x_min": X_MIN,
    }

    table = tabulate(
        [
            ["L", *L_frame_info.values()],
            ["M", *M_frame_info.values()],
        ],
        headers=["Frame", *L_frame_info.keys()],
        tablefmt="fancy_grid",
    )
    cprint(f"Values from input.deck of: {DATA_DIR}", "green")
    print("Number of Files:", POINTS)
    print(
        f"Angle: {ANGLE*180/(PI):.1f}",
    )
    print("Polarisation: ", POL_TYPE)
    print("Polarization Angle: ", POL_ANGLE)
    print(table)
    # return

    def plot_p(file_name, show_fig):
        omega_max_m = 2 * np.pi / dt_m
        omegas = np.linspace(-omega_max_m / 2, omega_max_m / 2, POINTS)
        omegas_l = omegas / beta

        Ety = np.zeros(POINTS)
        Etx = np.zeros(POINTS)
        for i in tqdm(range(POINTS), "Loading Data..."):
            data = sdf.read(ALL_FILES[i])
            Ety[i] = data.Electric_Field_Ey.data[8000]
            Etx[i] = data.Electric_Field_Ex.data[8000]

        fft_x = np.fft.fftshift(np.fft.fft(Etx * tan_factor))
        fft_x = np.abs(fft_x) / max(np.abs(fft_x))
        fft_y = np.fft.fftshift(np.fft.fft(Ety / ErL))
        fft_y = np.abs(fft_y) / max(np.abs(fft_y))

        plt.figure()
        plt.plot(omegas / omega_m, fft_y / np.max(fft_y), color=C1, label="$E_y (p)$")
        plt.plot(omegas / omega_m, fft_x / np.max(fft_x), color=C2, label="$E_x (p)$")
        plt.xlabel(r"$\omega [\omega_0]$")
        plt.ylabel(r"Amplitude")
        plt.legend()
        plt.yscale("log")
        plt.xlim(0, 20)
        x_ticks = np.arange(1, 21, 1)
        plt.xticks(x_ticks)
        plt.ylim(
            1e-3,
        )

        if file_name:
            plt.savefig(os.path.join(SAVE_DIR, f"{file_name}.png"))

        if show_fig:
            plt.show()
        else:
            plt.close()

    def plot_s(file_name, show_fig):
        omega_max_m = 2 * np.pi / dt_m
        omegas = np.linspace(-omega_max_m / 2, omega_max_m / 2, POINTS)
        omegas_l = omegas / beta

        Etz = np.zeros(POINTS)
        Etx = np.zeros(POINTS)
        for i in tqdm(range(POINTS), "Loading Data..."):
            data = sdf.read(ALL_FILES[i])
            Etz[i] = data.Electric_Field_Ez.data[8000]
            Etx[i] = data.Electric_Field_Ex.data[8000]

        fft_z = np.fft.fftshift(np.fft.fft(Etz / (ErL * beta)))
        fft_z = np.abs(fft_z)
        fft_x = np.fft.fftshift(np.fft.fft(Etx * tan_factor / ErL))
        fft_x = np.abs(fft_x)

        plt.figure()
        plt.plot(omegas / omega_m, fft_z / np.max(fft_z), color=C1, label="$E_z (s)$")
        plt.plot(omegas / omega_m, fft_x / np.max(fft_x), color=C2, label="$E_x (p)$")
        plt.xlabel(r"$\omega [\omega_0]$")
        plt.ylabel(r"Amplitude")
        plt.legend()
        plt.yscale("log")
        plt.xlim(0, 20)
        x_ticks = np.arange(1, 21, 1)
        plt.xticks(x_ticks)
        plt.ylim(
            1e-3,
        )

        if file_name:
            plt.savefig(os.path.join(SAVE_DIR, f"{file_name}.png"))

        if show_fig:
            plt.show()
        else:
            plt.close()

    print(f"This is a {POL_TYPE}-polarized wave")
    if POL_TYPE == "p":
        plot_p(file_name=file_name, show_fig=show_fig)
    else:
        plot_s(file_name=file_name, show_fig=show_fig)


if __name__ == "__main__":
    file_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(file_dir)
    dirs = glob.glob("run_*")
    dirs = [dir for dir in dirs if os.path.isdir(dir)]
    dirs = sorted(dirs)
    for dir in ["run_3", "run_5"]:
        cprint(f"Plotting {dir}", "red")
        if dir == "run_3":
            f_name = "p_fft"
        else:
            f_name = "s_fft"
        plot(
            data_dir=dir,
            show_fig=False,
            file_name=f_name,
            save_dir="/media/hari31416/Hari_SSD/Users/harik/Desktop/MSc_Project/Presentations/Reports/Sem_4_Major/images",
        )
    # plot(
    #     data_dir=dirs[-1],
    #     show_fig=False,
    #     file_name=f"f_fft_{dirs[-1]}",
    #     save_dir="images",
    # )
    # plot(dirs[0])
