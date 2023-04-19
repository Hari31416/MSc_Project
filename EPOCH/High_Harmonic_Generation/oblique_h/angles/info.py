import numpy as np
import os
import re
import glob
from style import *
from tabulate import tabulate

c = 299792458
PI = np.pi
pi = PI


def info(data_dir):
    DATA_DIR = data_dir
    ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
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
    text_info = f"""Values from input.deck of: {DATA_DIR}
Number of Files: {POINTS}
Angle: {ANGLE*180/(PI):.1f}
Polarisation: {POL_TYPE}
Polarization Angle: {POL_ANGLE}
{table}

"""
    return text_info


if __name__ == "__main__":
    file_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(file_dir)
    dirs = glob.glob("*/*")
    dirs = [x for x in dirs if "images" not in x]
    dirs = sorted(dirs)
    all_info = ""
    for dir in dirs:
        inf = info(dir)
        all_info += inf
    with open("info.txt", "w") as f:
        f.write(all_info)
    print(all_info)
