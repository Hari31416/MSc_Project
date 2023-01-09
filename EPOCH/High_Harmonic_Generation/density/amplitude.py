import matplotlib.pyplot as plt
import numpy as np
import os
import sdf
import re
import glob
import tqdm
import sys

def main(DATA_DIR):
    if "run_1/" in DATA_DIR:
        return 
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

    omega0 = 2 * PI * c / LAMBD
    tau = 2 * PI / omega0
    nc = epsilon * m * omega0**2 / e**2
    Er = m * omega0 * c / e
    n0 = FACTOR * nc
    LAS_TIME = LAS_TIME * tau


    # ## Other Variables

    ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
    ALL_FILES.sort()
    T = np.linspace(0, T_MAX, len(ALL_FILES))

    d = np.zeros((len(ALL_FILES), NX))
    for i in tqdm.tqdm(range(len(ALL_FILES)), desc="Getting Data..."):
        data = sdf.read(ALL_FILES[i])
        d[i] = data.Derived_Number_Density_Electron.data

    d = d / nc

    first = np.zeros(d.shape[0])
    last = np.zeros(d.shape[0])
    for i in range(d.shape[0]):
        nonzeros = np.where(d[i]>1)[0]
        if len(nonzeros) > 0:
                
            first[i] = nonzeros[0]
            last[i] = nonzeros[-1]

    print("Saving Images...")
    plt.figure()
    plt.plot(T, first)
    plt.xlabel(r"Time $[\tau]$")
    plt.ylabel("Node")
    plt.title("First Node with $n=n_c$")
    plt.ylim(7960, 8040)
    plt.savefig(f"images/first_node_{FACTOR}.png", dpi=300)

    plt.figure()
    plt.plot(T, last)
    plt.xlabel(r"Time $[\tau]$")
    plt.ylabel("Node")
    plt.title("Last Node with $n=n_c$")
    plt.ylim(7960, 8040)
    plt.savefig(f"images/last_node_{FACTOR}.png", dpi=300)

if __name__ == "__main__":
    main(sys.argv[1])