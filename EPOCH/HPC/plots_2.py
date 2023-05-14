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
    plot_field_progress = True,
    with_factor = True,
    save_data = True,
    save_data_dir = "output_data",
):
    try:
        file_dir = os.path.dirname(os.path.realpath(__file__))
    except NameError:
        file_dir = os.getcwd()
    DATA_DIR = os.path.join(file_dir, directory)
    SAVE_DIR = os.path.join(file_dir, save_dir)
    DIR = DATA_DIR.split(os.sep)[-1]
    # print(file_dir, save_data_dir)
    SAVE_DATA_DIR = os.path.join(file_dir, save_data_dir)


    ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
    ALL_FILES.sort()

    POINTS = len(ALL_FILES)
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
        try:
            a, b = angle_reg.search(data).groups()
        except AttributeError:
            angle_pretty = 0
            angle_rad = 0
            angle_degree = 0
            return angle_pretty, angle_degree, angle_rad

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
    
    
    raw_data = sdf.read(ALL_FILES[0])

    LAMBD = find_value("lambda0") * 1e-6
    X, Y = raw_data.Grid_Grid.data
    X = X/LAMBD
    Y = Y/LAMBD
    X_MIN = X.min()
    X_MAX = X.max()
    Y_MIN = Y.min()
    Y_MAX = Y.max()
    NX = int(find_value("cells_x"))
    NY = int(find_value("cells_y"))
    EXTENT = [X_MIN, X_MAX, Y_MIN, Y_MAX]
    LAS_TIME = int(find_value("las_time"))
    T_MAX = int(find_value("simulation_end"))
    DT = find_value("snapshot_freq") * 1e-15
    A0 = find_value("a0")
    FACTOR = int(find_value("factor"))
    NX = int(find_value("cells_x"))
    NY = int(find_value("cells_y"))
    TEMPERATURE = find_value("temp")
    angle_pretty, angle_degree, ANGLE = find_angle(data)
    print("Values from input.deck:")
    print("\tlambda0 = ", LAMBD)
    print("\tlaser_time = ", LAS_TIME)
    print("\tt_end = ", T_MAX)
    print("\tdt_snapshot = ", DT)
    print("\ta0 = ", A0)
    print("\tfactor = ", FACTOR)
    print("\tnx = ", NX)
    print("\tny = ", NY)
    print("\tx_min = ", X_MIN)
    print("\ty_min = ", Y_MIN)
    print("\tx_max = ", X_MAX)
    print("\ty_max = ", Y_MAX)
    print("\ttemp = ", TEMPERATURE)
    print("\tangle = ", angle_pretty)
    print("\tangle (degrees) = ", angle_degree)

    def x_position_to_node(x):
        return int((x - X_MIN)/(X_MAX - X_MIN)*NX)

    def y_position_to_node(y):
        return int((y - Y_MIN)/(Y_MAX - Y_MIN)*NY)

    def get_y_for_x(x):
        return x*np.tan(ANGLE)

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
    print(f"\tomega0 = {omega0:.4e}")
    print(f"\ttau = {tau:.4e}")
    print(f"\tnc = {nc:.4e}")
    print(f"\tEr = {Er:.4e}")
    print(f"\tn0 = {n0:.4e}")
    print(f"\tlambdaD = {lambdaD:.4e}")
    print(f"\tvth = {vth:.4e}")
    print(f"\tf_max = {f_max:.4e}")
    print(f"\tomega_max = {omega_max:.4e}")
    print(f"\tomega_max_natural = {omega_max_natural:.4e}")

    HALF = POINTS//2

    if with_factor:
        omega = np.linspace(-omega_max_natural, omega_max_natural, len(ALL_FILES))/np.cos(ANGLE)
        omega_b = np.linspace(-omega_max_natural, omega_max_natural, HALF)/np.cos(ANGLE)
        SAVE_DIR+="_m"
        if not os.path.exists(SAVE_DIR):
            os.mkdir(SAVE_DIR)
    else:
        omega = np.linspace(-omega_max_natural, omega_max_natural, POINTS)
        omega_b = np.linspace(-omega_max_natural, omega_max_natural, HALF)
    T = np.linspace(0, T_MAX, len(ALL_FILES))
    
    def get_image_name(name):
        if name is not None:
            fig_name = os.path.join(SAVE_DIR, name)
            if "." not in fig_name:
                fig_name += ".png"
        else:
            fig_name = None
        return fig_name

    if plot_density:
        raw_data = sdf.read(ALL_FILES[100])
        plt.figure()
        plt.imshow(raw_data.Derived_Number_Density_Electron.data.T / nc)
        plt.colorbar()
        plt.xlabel("$x \, [\mu m]$")
        plt.ylabel("$y \, [\mu m]$")
        plt.title("Electron Density")
        plt.tight_layout()
        if save_plots:
            density_name = get_image_name(f"{DIR}_density")
        else:
            density_name = None
        if density_name is not None:
            plt.savefig(density_name)
        if show_plots:
            plt.show()
        plt.close()

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
        )
        ax.set_xlabel("$x \, [\mu m]$")
        ax.set_ylabel("$y \, [\mu m]$")
        ax.set_title(f"t = {t:.1f} fs")

    def equat_shape(A, B):
        "Creates the shape of A and B equal by indexing"
        if A.shape == B.shape:
            return A, B

        if len(A) > len(B):
            length = len(B)
            return A[:length], B
        else:
            length = len(A)
            return A, B[:length]

    x_b = -5
    y_b = -get_y_for_x(x_b)
    x_a = -2
    y_a = get_y_for_x(x_a)
    x_0 = 0
    y_0 = get_y_for_x(x_0)

    x_b_node = x_position_to_node(x_b)
    y_b_node = y_position_to_node(y_b)
    x_a_node = x_position_to_node(x_a)
    y_a_node = y_position_to_node(y_a)
    x_0_node = x_position_to_node(x_0)
    y_0_node = y_position_to_node(y_0)
    point_a = (x_a_node, y_a_node)
    point_b = (x_b_node, y_b_node)
    point_0 = (x_0_node, y_0_node)
    print(point_a, point_b, point_0)
    # print(x_b, x_a, x_0)
    # print(y_b, y_a, y_0)
    # return 


    point1 = point_b
    point2 = point_a
    points3 = point_0

    Ex1 = np.zeros(POINTS)
    Ex2 = np.zeros(POINTS)
    Ex3 = np.zeros(POINTS)
    Ey1 = np.zeros(POINTS)
    Ey2 = np.zeros(POINTS)
    Ey3 = np.zeros(POINTS)
    Ez1 = np.zeros(POINTS)
    Ez2 = np.zeros(POINTS)
    Ez3 = np.zeros(POINTS)


    for i in tqdm.tqdm(
        range(POINTS),
        desc="Calculating fields",
        unit="files",
        file=sys.stdout,
    ):
        raw_data = sdf.read(ALL_FILES[i])
        Ex = raw_data.Electric_Field_Ex.data
        Ey = raw_data.Electric_Field_Ey.data
        Ez = raw_data.Electric_Field_Ez.data

        Ex1[i] = Ex[point1]
        Ex2[i] = Ex[point2]
        Ex3[i] = Ex[points3]

        Ey1[i] = Ey[point1]
        Ey2[i] = Ey[point2]
        Ey3[i] = Ey[points3]

        Ez1[i] = Ez[point1]
        Ez2[i] = Ez[point2]
        Ez3[i] = Ez[points3]

    def plot_one_field(fields, component="x", fig_name=None, show=True):
        if fields[0].max() > 0:
            Es = fields
            titles = [
                f"$E_{component}$ at ({point1[0]}, {point1[1]})",
                f"$E_{component}$ at ({point2[0]}, {point2[1]})",
                f"$E_{component}$ at ({points3[0]}, {points3[1]})",
            ]
            plt.figure()
            for i, E in enumerate(Es):
                plt.plot(T, E/np.max(E), label=titles[i])
            plt.legend()
            plt.xlabel(r"$t \;[\tau]$")
            plt.ylabel(f"$E_{component}$")
            fig_name = get_image_name(fig_name)
            print(f"Figure name for field {component} is {fig_name}")
            if fig_name:
                plt.savefig(fig_name)
            if show:
                plt.show()
            plt.close()
        else:
            print(f"E{component} is zero. Skipping plot.")
        

    def plot_e_fields(save_fig=True, prefix="", show=True):

        if save_fig:
            fig_name_x = f"{prefix}_Ex"
            fig_name_y = f"{prefix}_Ey"
            fig_name_z = f"{prefix}_Ez"
        else:
            fig_name_x = None
            fig_name_y = None
            fig_name_z = None

        fields = [Ex1, Ex2, Ex3]
        plot_one_field(fields, component="x", fig_name=fig_name_x, show=show)
        fields = [Ey1, Ey2, Ey3]
        plot_one_field(fields, component="y", fig_name=fig_name_y, show=show)
        fields = [Ez1, Ez2, Ez3]
        plot_one_field(fields, component="z", fig_name=fig_name_z, show=show)

    def plot_one_fft(
        ax,
        E,
        type_ = "b",
        component="y",
        title="",
        plot_lines=True,
    ):
        
        if type_ == "b":
            print("Type b")
            omega_ = omega_b
            E = E[:HALF]
            if len(omega_)!=len(E):
                omega_, E = equat_shape(omega_, E)
        elif type_ == "a":
            print("Type a")
            omega_ = omega_b
            if len(omega_)!=len(E):
                E = E[HALF+1:]
            else:
                E = E[HALF:]
            if len(omega_)!=len(E):
                omega_, E = equat_shape(omega_, E)
        else:
            print("Type All")
            omega_ = omega
        print(omega_.shape, E.shape)
        fft = np.fft.fft(E)
        fft = np.fft.fftshift(fft)
        fft = np.abs(fft)
        fft = fft / (fft.max() + 1e-10)
        

        ax.plot(omega_, fft**2, label=f"$E_{component}$")
        ax.set_yscale("log")
        ax.set_xlim(
            0,
        )
        ax.set_xlabel("$\omega$")
        ax.set_ylabel("$\mathcal{|E|}^2$")
        ax.set_title(title, fontdict={"fontsize": 12})
        ax.legend()
        if with_factor:
            xticks = np.arange(1, int(omega_max_natural/np.cos(ANGLE)) + 3, 2)
        else:
            xticks = np.arange(1, int(omega_max_natural) + 3, 2)
        ax.set_xticks(xticks)

        if plot_lines:
            for x in xticks:
                ax.axvline(x, color="k", alpha=0.7, linewidth=0.5)
        return fft, omega_

    def plot_ffts_func(save_fig=True, prefix="", show=True):
        if save_fig:
            fig_name_x = f"{prefix}_Ex_fft"
            fig_name_y = f"{prefix}_Ey_fft"
            fig_name_z = f"{prefix}_Ez_fft"
        else:
            fig_name_x = None
            fig_name_y = None
            fig_name_z = None

        if Ez1.max() > 0:
            fig, axes = plt.subplots(3, 1, figsize=(5, 15))
            Es = [Ez1, Ez2, Ez3]
            #types = ["b", "a", "all"]
            types = ["all", "all", "all"]
            titles = [
                f"$E_z$ at ({point1[0]}, {point1[1]})",
                f"$E_z$ at ({point2[0]}, {point2[1]})",
                f"$E_z$ at ({points3[0]}, {points3[1]})",
            ]
            for i, ax in enumerate(axes):
                fft, omega_ = plot_one_fft(
                    ax,
                    Es[i],
                    type_= types[i],
                    component="z",
                    title=titles[i],
                )
                if save_data:
                    with open(os.path.join(SAVE_DATA_DIR, f"{directory}_fft_z_{i}.npy"), "wb") as f:
                        np.save(f, fft)
                    with open(os.path.join(SAVE_DATA_DIR, f"{directory}_omega_z_{i}.npy"), "wb") as f:
                        np.save(f, omega_)
            fig_name = get_image_name(fig_name_z)
            print(f"Figure name for z fft is {fig_name}")
            if fig_name:
                fig.savefig(fig_name)
            if show:
                plt.show()
            plt.close()
        else:
            print("Ez is zero. Skipping plot.")

        if Ex1.max() > 0:
            fig, axes = plt.subplots(3, 1, figsize=(5, 15))
            Es = [Ex1, Ex2, Ex3]
            types = ["all", "all", "all"]
            titles = [
                f"$E_x$ at ({point1[0]}, {point1[1]})",
                f"$E_x$ at ({point2[0]}, {point2[1]})",
                f"$E_x$ at ({points3[0]}, {points3[1]})",
            ]
            for i, ax in enumerate(axes):
                fft, omega_ = plot_one_fft(
                    ax,
                    Es[i],
                    type_= types[i],
                    component="x",
                    title=titles[i],
                )
                if save_data:
                    with open(os.path.join(SAVE_DATA_DIR, f"{directory}_fft_x_{i}.npy"), "wb") as f:
                        np.save(f, fft)
                    with open(os.path.join(SAVE_DATA_DIR, f"{directory}_omega_x_{i}.npy"), "wb") as f:
                        np.save(f, omega_)
            fig_name = get_image_name(fig_name_x)
            print(f"Figure name for x fft is {fig_name}")
            if fig_name:
                fig.savefig(fig_name)
            if show:
                plt.show()
            plt.close()
        else:
            print("Ex is zero. Skipping plot.")

        if Ey1.max() > 0:
            fig, axes = plt.subplots(3, 1, figsize=(5, 15))
            Es = [Ey1, Ey2, Ey3]
            types = ["all", "all", "all"]
            titles = [
                f"$E_y$ at ({point1[0]}, {point1[1]})",
                f"$E_y$ at ({point2[0]}, {point2[1]})",
                f"$E_y$ at ({points3[0]}, {points3[1]})",
            ]
            for i, ax in enumerate(axes):
                fft, omega_ = plot_one_fft(
                    ax,
                    Es[i],
                    type_= types[i],
                    component="y",
                    title=titles[i],
                )
                if save_data:
                    with open(os.path.join(SAVE_DATA_DIR, f"{directory}_fft_y_{i}.npy"), "wb") as f:
                        np.save(f, fft)
                    with open(os.path.join(SAVE_DATA_DIR, f"{directory}_omega_y_{i}.npy"), "wb") as f:
                        np.save(f, omega_)
            fig_name = get_image_name(fig_name_y)
            print(f"Figure name for y fft is {fig_name}")
            if fig_name:
                fig.savefig(fig_name)
            if show:
                plt.show()
            plt.close()
        else:
            print("Ey is zero. Skipping plot.")

    if plot_fields:
        if save_plots:
            prefix = DIR
            save_fig = True
        else:
            save_fig = False
            prefix = None
        plot_e_fields(save_fig=save_fig, prefix=prefix, show=show_plots)

    if plot_ffts:
        if save_plots:
            prefix = DIR
            save_fig = True
        else:
            save_fig = False
            prefix = None
        plot_ffts_func(save_fig=save_fig, prefix=prefix, show=show_plots)

    if plot_field_progress:
        fig, ax = plt.subplots(4, 4, figsize=(35, 35))
        ax = ax.flatten()
        i = 0
        for j in tqdm.tqdm(range(100, len(ALL_FILES), 70), desc="Plotting Fields...", file=sys.stdout):
            plot_field(ALL_FILES[j], ax[i], component="y")
            i += 1
            if i == 16:
                break
        plt.tight_layout()
        if save_plots:
            fields_name = get_image_name(f"{DIR}_fields")
        else:
            fields_name = None
        if fields_name is not None:
            plt.savefig(fields_name, dpi=300)
        if show_plots:
            plt.show()
        plt.close()


if __name__ == "__main__":
    print(f"Current Directory: {os.curdir}")
    # directories = "13run 14run".split(" ")
    directories = ["22run"]
    # print(directories)
    save_dir = "images_4"
    plot_fields = True
    plot_ffts = True
    plot_density = True
    show_plots = False
    save_plots = True
    plot_field_progress = True
    save_data = True
    save_data_dir = "output_data"

    for directory in directories:
        print()
        print("====================================================")
        print("----------------------------------------------------")
        print(f"\nGoing to {directory}\n")
        print()
        main(
            directory=directory,
            save_dir=save_dir,
            plot_fields=plot_fields,
            plot_ffts=plot_ffts,
            plot_density=plot_density,
            show_plots=show_plots,
            save_plots=save_plots,
            plot_field_progress=plot_field_progress,
            with_factor=False,
            save_data=save_data,
            save_data_dir=save_data_dir
        )
        print()
        print("----------------------------------------------------")
        print("====================================================")
        print()
