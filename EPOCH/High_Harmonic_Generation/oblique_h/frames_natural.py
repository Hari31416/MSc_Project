import matplotlib.pyplot as plt
import numpy as np
import os
import sdf
import re
import glob
from tqdm import tqdm
import sys
from style import *
from tabulate import tabulate

plt.rcParams["font.size"] = 14
plt.rcParams["figure.figsize"] = (10, 8)


def main(DATA_DIR, angle):

    # m = 9.10938356e-31
    # e = 1.60217662e-19
    c = 299792458
    PI = np.pi
    # epsilon = 8.85e-12

    with open(os.path.join(DATA_DIR, "input.deck"), "r") as myfile:
        data = myfile.read()

    def find_value(info):
        regex = re.compile(rf"\s{info}\s*=\s*-?(\d+\.?\d*)")
        match = regex.search(data)
        if match:
            return float(match.group(1))
        else:
            return None

    beta = np.cos(np.deg2rad(angle))

    LAMBD = find_value("lambda0") * 1e-6
    LAS_TIME = int(find_value("las_time"))
    T_MAX = int(find_value("t_end"))
    DT = find_value("dt_snapshot") * 1e-15
    A0 = find_value("a0")
    FACTOR = int(find_value("factor"))
    NX = int(find_value("nx"))
    X_MIN = -int(find_value("x_min"))

    lambda_0 = LAMBD
    omega_0 = 2 * PI * c / lambda_0
    tau_0 = 2 * PI / omega_0

    lambda_m = LAMBD / beta
    omega_m = 2 * PI * c / lambda_m
    tau_m = 2 * PI / omega_m
    dt_m = DT / beta

    lambda_l = lambda_0
    omega_l = omega_0
    tau_l = tau_0
    dt_l = DT

    LAS_TIME_L = LAS_TIME * tau_l
    LAS_TIME_M = LAS_TIME * tau_m
    T_MAX_L = T_MAX * tau_l
    T_MAX_M = T_MAX * tau_m

    L_frame_info = {
        "lambda": lambda_l,
        "tau": tau_l,
        "omega": omega_l,
        "laser_time": LAS_TIME_L,
        "t_end": T_MAX_L,
        "dt_snapshot": dt_l,
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
        "dt_snapshot": dt_m,
        "a0": A0,
        "factor": FACTOR,
        "nx": NX,
        "x_min_natural": X_MIN * lambda_m,
        "x_min": X_MIN,
    }

    table = tabulate(
        [
            ["L Frame", *L_frame_info.values()],
            ["M Frame", *M_frame_info.values()],
        ],
        headers=["Frame", *L_frame_info.keys()],
        tablefmt="fancy_grid",
    )
    cprint("Values from input.deck:", "bold")
    print(table)

    def field_M(t):
        env = np.sin((PI * t) / LAS_TIME_M) ** 2
        E = np.sin(omega_m * t)
        if t < LAS_TIME_M:
            return E * env
        else:
            return 0

    def field_L(t):
        env = np.sin((PI * t) / LAS_TIME_L) ** 2
        E = np.sin(omega_l * t)
        if t < LAS_TIME_L:
            return E * env
        else:
            return 0

    ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
    ALL_FILES.sort()

    Ts_M = np.linspace(0, T_MAX_M, len(ALL_FILES))
    Ts_L = np.linspace(0, T_MAX_L, len(ALL_FILES))

    Es_M = [field_M(t) for t in Ts_M]
    Es_L = [field_L(t) for t in Ts_L]

    Ety = np.zeros(len(ALL_FILES))
    Etz = np.zeros(len(ALL_FILES))
    for i in tqdm(range(len(ALL_FILES)), "Loading Data..."):
        data = sdf.read(ALL_FILES[i])
        Ety[i] = data.Electric_Field_Ey.data[0]
        Etz[i] = data.Electric_Field_Ez.data[0]

    cprint("Saving M Frame", "warning")
    plt.figure()
    plt.plot(Ts_M / tau_0, Ety / max(Ety), label="Simulation Ety")
    plt.plot(Ts_M / tau_0, Es_M, label="Function")
    plt.title("Ety M Frame")
    plt.xlim(0, T_MAX_M / tau_0)
    plt.legend()
    plt.savefig(f"images/{DATA_DIR}_Ety_M_N.png")
    plt.close()
    # plt.show()

    plt.figure()
    plt.plot(Ts_M / tau_0, Etz / max(Etz), label="Simulation Etz")
    plt.plot(Ts_M / tau_0, Es_M, label="Function")
    plt.title("Etz M Frame")
    plt.xlim(0, T_MAX_M / tau_0)
    plt.legend()
    plt.savefig(f"images/{DATA_DIR}_Etz_M_N.png")
    plt.close()

    cprint("Saving L Frame", "warning")
    plt.figure()
    plt.plot(Ts_L / tau_0, Ety / max(Ety), label="Simulation Ety")
    plt.plot(Ts_L / tau_0, Es_L, label="Function")
    plt.title("Ety L Frame")
    plt.xlim(0, T_MAX_M / tau_0)
    plt.legend()
    plt.savefig(f"images/{DATA_DIR}_Ety_L_N.png")
    plt.close()

    plt.figure()
    plt.plot(Ts_L / tau_0, Etz / max(Etz), label="Simulation Etz")
    plt.plot(Ts_L / tau_0, Es_L, label="Function")
    plt.title("Etz L Frame")
    plt.xlim(0, T_MAX_M / tau_0)
    plt.legend()
    plt.savefig(f"images/{DATA_DIR}_Etz_L_N.png")
    plt.close()


if __name__ == "__main__":
    dirs = glob.glob("run_*")
    angles = [60, 0, 30, 60, 45, 45]
    # angle = int(sys.argv[2])
    for dir, angle in zip(dirs, angles):
        cprint(f"DIRECTORY: {dir.upper()}", option="green")
        main(dir, angle)
