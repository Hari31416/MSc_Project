import matplotlib.pyplot as plt
import numpy as np
import sdf
import glob
import tqdm
import os
import re
from tabulate import tabulate

plt.rcParams["font.size"] = 14
plt.rcParams["figure.figsize"] = (10, 8)


directory = "3run"
save_dir = "3run"

try:
    file_dir = os.path.dirname(os.path.realpath(__file__))
except NameError:
    file_dir = os.getcwd()
DATA_DIR = os.path.join(file_dir, directory)
SAVE_DIR = os.path.join(file_dir, save_dir)

ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
ALL_FILES.sort()
POINTS = len(ALL_FILES)
print(f"Found {POINTS} files")

main_info = {"SDF Files": POINTS}

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
    angle_reg = re.compile(
        "upper_theta\s+=\s+(\d{0,3})\s{0,3}\*?\s{0,3}pi\s{0,3}\/\s{0,3}(\d{0,3})"
    )
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
X = X / LAMBD
Y = Y / LAMBD
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
NX = int(find_value("cells_x"))
NY = int(find_value("cells_y"))
angle_pretty, angle_degree, ANGLE = find_angle(data)

main_info["Lambda"] = LAMBD
main_info["Extent"] = EXTENT
main_info["Cells in X"] = NX
main_info["Cells in Y"] = NY
main_info["Laser Time"] = LAS_TIME
main_info["Max Time"] = T_MAX
main_info["Delta T"] = DT
main_info["A0"] = A0
main_info["Angle in Degree"] = angle_degree
main_info["Angle"] = angle_pretty

# Calculating Parameters
omega0 = 2 * PI * c / LAMBD
tau = 2 * PI / omega0
nc = epsilon * m * omega0**2 / e**2
Er = m * omega0 * c / e
LAS_TIME = LAS_TIME * tau
f_max = 1 / (2 * DT)
omega_max = 2 * PI * f_max
omega_max_natural = omega_max / omega0
calculated_info = {
    "Omega0": omega0,
    "Tau": tau,
    "Critical Density": nc,
    "Electric Field": Er,
    "Laser Time": LAS_TIME,
    "Max Resolvable Frequency": f_max,
    "Max Resolvable Omega": omega_max_natural,
}

table_main = tabulate(main_info.items(), headers=["Parameter", "Value"])
table_calculated = tabulate(calculated_info.items(), headers=["Parameter", "Value"])
print(table_main)
print(table_calculated)

omega = np.linspace(-omega_max_natural, omega_max_natural, len(ALL_FILES))
X = np.linspace(X_MIN, -X_MIN, NX)
T = np.linspace(0, T_MAX, len(ALL_FILES))


def get_y_for_x(x):
    return x * np.tan(ANGLE)


def get_image_name(name):
    if name is not None:
        fig_name = os.path.join(SAVE_DIR, name)
        if "." not in fig_name:
            fig_name += ".png"
    else:
        fig_name = None
    return fig_name


def x_position_to_node(x):
    return int((x - X_MIN) / (X_MAX - X_MIN) * NX)


def y_position_to_node(y):
    return int((y - Y_MIN) / (Y_MAX - Y_MIN) * NY)


def get_y_for_x(x):
    return x * np.tan(ANGLE)


x_b = -6
y_b = -get_y_for_x(x_b)
x_a = -4
y_a = get_y_for_x(x_a)
x_c = -2
y_c = get_y_for_x(x_c)

x_b_node = x_position_to_node(x_b)
y_b_node = y_position_to_node(y_b)
x_a_node = x_position_to_node(x_a)
y_a_node = y_position_to_node(y_a)
x_c_node = x_position_to_node(x_c)
y_c_node = y_position_to_node(y_c)
point_a = (x_a_node, y_a_node)
point_b = (x_b_node, y_b_node)
point_c = (x_c_node, y_c_node)

print(f"Point A: {point_a}")
print(f"Point B: {point_b}")
print(f"Point C: {point_c}")
