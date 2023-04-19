import matplotlib.pyplot as plt
import numpy as np
import os
import sdf
import re
import glob
import tqdm

plt.rcParams["font.size"] = 14
plt.rcParams["figure.figsize"] = (10, 8)

m = 9.10938356e-31
e = 1.60217662e-19
c = 299792458
PI = np.pi
epsilon = 8.85e-12


DATA_DIR = "1run"
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

print("Values from input.deck:")
print("lambda0 = ", LAMBD)
print("laser_time = ", LAS_TIME)
print("t_end = ", T_MAX)
print("dt_snapshot = ", DT)
print("a0 = ", A0)
print("factor = ", FACTOR)
print("nx = ", NX)
print("x_min = ", X_MIN)

omega0 = 2 * PI * c / LAMBD
tau = 2 * PI / omega0
nc = epsilon * m * omega0**2 / e**2
Er = m * omega0 * c / e
n0 = FACTOR * nc
LAS_TIME = LAS_TIME * tau
print("Calculated Values for the simulation are:")
print("omega0 = ", omega0)
print("tau = ", tau)
print("nc = ", nc)
print("Er = ", Er)
print("n0 = ", n0)

ALL_FILES = glob.glob(f"{DATA_DIR}/*sdf")
ALL_FILES.sort()
X = np.linspace(X_MIN, -X_MIN, NX)
T = np.linspace(0, T_MAX, len(ALL_FILES))


def get_field(id, component="y"):
    raw_data = sdf.read(ALL_FILES[id])
    comp = {
        # "x": raw_data.Electric_Field_Ex,
        "y": raw_data.Electric_Field_Ey,
        # "z": raw_data.Electric_Field_Ez,
    }
    field = comp[component].data
    return field


# Ey = get_field(500)
# plt.plot(X, Ey)
# plt.axvline(0, color="red")
# plt.show()

Et0 = np.zeros(len(ALL_FILES))
Et1 = np.zeros(len(ALL_FILES))
Et2 = np.zeros(len(ALL_FILES))
d = np.zeros((len(ALL_FILES), NX))
for i in tqdm.tqdm(range(len(ALL_FILES)), desc="Getting Data..."):
    data = sdf.read(ALL_FILES[i])
    ey = data.Electric_Field_Ey.data
    # Et0[i] = ey[0]
    # Et1[i] = ey[4000]
    Et2[i] = ey[6000]
    # d[i] = data.Derived_Number_Density_Electron.data

Et_fft = np.fft.fft(Et2)
y = np.fft.fftshift(Et_fft)
y_f = np.abs(y)

f_max = 1 / (DT)
omega_max = 2 * np.pi * f_max
omega_max / omega0

omega = np.linspace(-omega_max / 2, omega_max / 2, len(ALL_FILES))

plt.plot(omega / omega0, y_f**2)
plt.yscale("log")
points = np.arange(1, 21, 2)
for p in points:
    plt.axvline(p, color="red", linestyle="--")
    plt.annotate(f"{p}", (p, 1e-2))
plt.xlim(0, 20)
plt.grid()
plt.title("Node 0")
plt.show()
# plt.ylim(0.1)
