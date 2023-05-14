import matplotlib.pyplot as plt
import numpy as np
import sdf
import glob
import tqdm
import os
import re
import sys

plt.rcParams["font.size"] = 14
plt.rcParams["figure.figsize"] = (10, 8)


def main(
    directory,
    save_dir="images",
    plot_fields=False,
    plot_ffts=True,
    plot_density=False,
    show_plots=False,
    save_plots=True,
):
    try:
        file_dir = os.path.dirname(os.path.realpath(__file__))
    except NameError:
        file_dir = os.getcwd()
    DATA_DIR = os.path.join(file_dir, directory)
    SAVE_DIR = os.path.join(file_dir, save_dir)
    DIR = DATA_DIR.split(os.sep)[-1]

    ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
    ALL_FILES.sort()

    ALL_FILES = ALL_FILES[:-10]
    POINTS = len(ALL_FILES)
    EXTENT = [-10, 10, -10, 10]
    print(f"Found {POINTS} files")

    # Constants
    m = 9.10938356e-31
    e = 1.60217662e-19
    c = 299792458
    PI = np.pi
    epsilon = 8.85e-12
    kb = 1.38064852e-23

    # Loading Parameters
    with open(os.path.join(DATA_DIR, "input.deck"), "r") as myfile:
        data = myfile.read()

    def find_value(info):
        regex = re.compile(rf"\s{info}\s*=\s*-?(\d+\.?\d*)")
        match = regex.search(data)
        if match:
            return float(match.group(1))
        else:
            return None
        
    def find_angle(data):
        angle_reg = re.compile("upper_theta\s+=\s+(\d{0,3})\s{0,3}\*?\s{0,3}pi\s{0,3}\/\s{0,3}(\d{0,3})")
        a, b = angle_reg.search(data).groups()
        angle_pretty = f"{a}π/{b}"
        if not a and not b:
            raise ValueError("Angle is not parsed correctly.")
        if not a:
            a = 1
        if not b:
            b = 1
        angle_rad = int(a) * PI / int(b)
        angle_degree = angle_rad * 180 / PI
        angle_degree = round(angle_degree, 1)
        return angle_pretty, angle_degree, angle_rad

    LAMBD = find_value("lambda0") * 1e-6
    LAS_TIME = int(find_value("las_time"))
    T_MAX = int(find_value("simulation_end"))
    DT = find_value("snapshot_freq") * 1e-15
    A0 = find_value("a0")
    FACTOR = int(find_value("factor"))
    NX = int(find_value("cells_x"))
    NY = int(find_value("cells_y"))
    X_MIN = -int(find_value("max_x"))
    Y_MIN = -int(find_value("max_y"))
    TEMPERATURE = find_value("temp")
    angle_pretty, angle_degree, ANGLE = find_angle(data)
    print("Values from input.deck:")
    print("lambda0 = ", LAMBD)
    print("laser_time = ", LAS_TIME)
    print("t_end = ", T_MAX)
    print("dt_snapshot = ", DT)
    print("a0 = ", A0)
    print("factor = ", FACTOR)
    print("nx = ", NX)
    print("ny = ", NY)
    print("x_min = ", X_MIN)
    print("y_min = ", Y_MIN)
    print("temp = ", TEMPERATURE)
    print("angle = ", angle_pretty)
    print("angle (degrees) = ", angle_degree)

    # Calculating Parameters
    omega0 = 2 * PI * c / LAMBD
    tau = 2 * PI / omega0
    nc = epsilon * m * omega0**2 / e**2
    Er = m * omega0 * c / e
    n0 = FACTOR * nc
    LAS_TIME = LAS_TIME * tau
    lambdaD = np.sqrt(epsilon * kb * TEMPERATURE / (n0 * e**2))
    vth = np.sqrt(kb * TEMPERATURE / m)
    f_max = 1 / (2 * DT)
    omega_max = 2 * PI * f_max
    omega_max_natural = omega_max / omega0
    print("Calculated Values for the simulation are:")
    print(f"omega0 = {omega0:.4e}")
    print(f"tau = {tau:.4e}")
    print(f"nc = {nc:.4e}")
    print(f"Er = {Er:.4e}")
    print(f"n0 = {n0:.4e}")
    print(f"lambdaD = {lambdaD:.4e}")
    print(f"vth = {vth:.4e}")
    print(f"f_max = {f_max:.4e}")
    print(f"omega_max = {omega_max:.4e}")
    print(f"omega_max_natural = {omega_max_natural:.4e}")

    # Calculating Grids
    omega = np.linspace(-omega_max_natural, omega_max_natural, len(ALL_FILES))/np.cos(ANGLE)
    X = np.linspace(X_MIN, -X_MIN, NX)
    T = np.linspace(0, T_MAX, len(ALL_FILES))

    def get_image_name(name):
        if name is not None:
            fig_name = os.path.join(SAVE_DIR, name)
            if "." not in fig_name:
                fig_name += ".png"
        else:
            fig_name = None
        return fig_name
    
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
    fig, ax = plt.subplots(4, 4, figsize=(35, 35))
    ax = ax.flatten()
    i = 0
    for j in tqdm.tqdm(range(100, len(ALL_FILES), 50), desc="Plotting..."):
        plot_field(ALL_FILES[j], ax[i], component="y")
        i += 1
        if i == 16:
            break
    plt.tight_layout()
    fig.savefig("Field.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    print(f"Current Directory: {os.curdir}")
    directory = "1run"
    save_dir = "images"
    plot_fields = True
    plot_ffts = True
    plot_density = True
    show_plots = False
    save_plots = True
    print(f"Going to {directory}")
    main(
        directory=directory,
        save_dir=save_dir,
        plot_fields=plot_fields,
        plot_ffts=plot_ffts,
        plot_density=plot_density,
        show_plots=show_plots,
        save_plots=save_plots,
    )

