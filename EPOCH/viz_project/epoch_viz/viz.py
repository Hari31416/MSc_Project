import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import os
import sdf
import re
import glob
import tqdm

plt.rcParams["font.size"] = 14


class EpochException(Exception):
    """Base class for exceptions in this module."""

    pass


class EmptyDirectoryError(EpochException):
    """Exception raised for empty directories.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class InputFileNotFoundError(EpochException):
    """Exception raised for missing input.deck files.

    Attributes:
        message -- explanation of the error
    """

    def init(self, message):
        self.message = message


class NoSdfFilesError(EpochException):
    """Exception raised for directories without sdf files.

    Attributes:
        message -- explanation of the error
    """

    def init(self, message):
        self.message = message


class DataNotFoundError(EpochException):
    """Exception raised for missing data.

    Attributes:
        message -- explanation of the error
    """

    def init(self, message):
        self.message = message


class InvalidTimeError(EpochException):
    """Exception raised for missing time nodes.

    Attributes:
        message -- explanation of the error
    """

    def init(self, message):
        self.message = message


class InvalidSpaceError(EpochException):
    """Exception raised for missing space nodes.

    Attributes:
        message -- explanation of the error
    """

    def init(self, message):
        self.message = message


# universal constants
m = 9.10938356e-31  # mass of electron in kg
e = 1.60217662e-19  # charge of electron in C
c = 299792458  # speed of light in m/s
pi = np.pi  # pi
epsilon = 8.85418781e-12  # permittivity of free space in F/m
kb = 1.38064852e-23  # Boltzmann constant in J/K
na = 6.02214076e23  # Avogadro constant in mol^-1

transformation_dictionary = {
    "Ex": "Electric Field/Ex",
    "Ey": "Electric Field/Ey",
    "Ez": "Electric Field/Ez",
    "Bx": "Magnetic Field/Bx",
    "By": "Magnetic Field/By",
    "Bz": "Magnetic Field/Bz",
    "Px": "Particles/Px/Electron",
    "Py": "Particles/Py/Electron",
    "Pz": "Particles/Pz/Electron",
    "rho": "Derived/Charge_Density",
    "Ne": "Derived/Number_Density/Electron",
    "N": "Derived/Number_Density",
}

deck_info_map = {
    "LAMBD": "Wavelength (m)",
    "LAS_TIME": "Laser Width (tau)",
    "T_MAX": "Max Time (tau)",
    "DT": "Dump Time Step (s)",
    "A0": "Normalized Vector Potential",
    "FACTOR": "Density Factor",
    "NX": "Number of Grid Points",
    "X_MIN": "Minimum X (wavelength)",
    "X_MAX": "Maximum X (wavelength)",
    "THICKNESS": "Thickness of Plasma (wavelength)",
    "PPC": "Particles per Cell",
    "START": "Start Position of Plasma (wavelength)",
    "TEMP": "Temperature of Plasma (eV)",
}

calculated_parameters_map = {
    "omega0": "Laser Frequency (Hz)",
    "tau": "Laser Width (s)",
    "nc": "Critical Density (m^-3)",
    "pulse_width": "Pulse Width (s)",
    "ne": "Electron Plamsa Density (m^-3)",
    "temperature_ev": "Temperature (eV)",
    "temperature": "Temperature (K)",
    "lambdaD": "Debye Length (m)",
    "vth": "Thermal Velocity (m/s)",
    "box_size": "Box Size (m)",
    "dx": "Grid Spacing (m)",
    "dt": "Time Step (s)",
    "runtime": "Run Time (s)",
    "omega_max": "Maximum Resolvable Omega (omega0)",
}


class EpochViz:
    def __init__(self, directory, save_directory=os.curdir):
        self.directory = directory
        self.save_directory = save_directory
        self.__checks()
        self.files = glob.glob(os.path.join(self.directory, "*.sdf"))
        self.files.sort()
        self.__everything_calculated = False
        self.data = {}
        self.info()

    def __str__(self):
        return f"EpochViz object for {self.directory}"

    def __repr__(self):
        return f"EpochViz({self.directory})"

    def __checks(self):
        """
        Performs checks on the directory to make sure it is valid.
        """
        if not os.path.isdir(self.directory):
            raise ValueError(f"{self.directory} is not a directory")
        if len(os.listdir(self.directory)) == 0:
            raise EmptyDirectoryError(f"{self.directory} is empty")
        if not os.path.isfile(os.path.join(self.directory, "input.deck")):
            raise InputFileNotFoundError(
                f"{self.directory} does not contain an input.deck file"
            )
        if len(glob.glob(os.path.join(self.directory, "*.sdf"))) == 0:
            raise NoSdfFilesError(f"{self.directory} does not contain any sdf files")

    def __get_save_file_name(self, file_name, format="png"):
        """
        Gets the file name from the path.
        """
        image_formats = ["png", "jpg", "jpeg", "tiff", "bmp", "pdf", "svg"]
        if file_name.split(".")[-1] in image_formats:
            file_name = file_name
        else:
            file_name = file_name + "." + format
        return os.path.join(self.save_directory, file_name)

    def __find_value(self, info, text):
        regex = re.compile(rf"\s{info}\s*=\s*-?(\d+\.?\d*)")
        match = regex.search(text)
        if match:
            return float(match.group(1))
        else:
            return None

    def __find_available_data(self):
        """
        Finds the available data in the sdf files.
        """
        data = sdf.read(self.files[0], dict=True)

        found_data = []
        for key, value in transformation_dictionary.items():
            if value in data.keys():
                found_data.append(key)

        self.available_data = found_data
        return found_data

    def __get_run_info(self):
        with open(os.path.join(self.directory, "epoch1d.dat"), "r") as f:
            run_info = f.readlines()
            last_line = run_info[-1]

        iterations = int((last_line.split("  ")[-1]).strip())
        self.iterations = iterations
        return iterations

    def __get_input_deck_info(self):

        with open(os.path.join(self.directory, "input.deck"), "r") as f:
            text = f.read()

        LAMBD = self.__find_value(text=text, info="lambda0") * 1e-6
        LAS_TIME = int(self.__find_value(text=text, info="las_time"))
        T_MAX = int(self.__find_value(text=text, info="t_end"))
        DT = self.__find_value(text=text, info="dt_snapshot") * 1e-15
        A0 = self.__find_value(text=text, info="a0")
        FACTOR = int(self.__find_value(text=text, info="factor"))
        NX = int(self.__find_value(text=text, info="nx"))
        X_MIN = -int(self.__find_value(text=text, info="x_min"))
        try:
            X_MAX = int(self.__find_value(text=text, info="x_max"))
        except:
            X_MAX = -X_MIN
        THICKNESS = int(self.__find_value(text=text, info="thickness"))
        PPC = int(self.__find_value(text=text, info="nparticles_per_cell"))
        START = int(self.__find_value(text=text, info="start"))
        TEMP = int(self.__find_value(text=text, info="temp"))

        deck_info = {
            "LAMBD": LAMBD,
            "LAS_TIME": LAS_TIME,
            "T_MAX": T_MAX,
            "DT": DT,
            "A0": A0,
            "FACTOR": FACTOR,
            "NX": NX,
            "X_MIN": X_MIN,
            "X_MAX": X_MAX,
            "THICKNESS": THICKNESS,
            "PPC": PPC,
            "START": START,
            "TEMP": TEMP,
        }
        self.deck_info = deck_info
        return deck_info

    def __calculate_parameters(self):
        deck_info = self.__get_input_deck_info()
        iterations = self.__get_run_info()

        ## Parameters for laser
        # Wavelength of the laser
        lambd = deck_info["LAMBD"]
        # Angular freaquency of the laser
        omega0 = 2 * pi * c / lambd
        # Time period of the laser
        tau = 2 * pi / omega0
        # Critical density corresponding to the laser frequency
        nc = epsilon * m * omega0**2 / e**2
        # Laser pulse width
        pulse_width = deck_info["LAS_TIME"] * tau

        ## Parameters for plasma
        # Density of the plasma
        ne = nc * deck_info["FACTOR"]
        # temperature of the plasma in eV
        temperature_ev = deck_info["TEMP"]
        # Temperature of the plasma in SI units
        temperature = temperature_ev * e / kb
        # Debye length
        lambdaD = np.sqrt(epsilon * kb * temperature / (ne * e**2))
        # Thermal velocity
        vth = np.sqrt(kb * temperature / m)

        ## Some General Parameters
        # Box size
        box_size = (deck_info["X_MAX"] - deck_info["X_MIN"]) * lambd
        # Cell size
        dx = box_size / deck_info["NX"]
        # runtime
        runtime = deck_info["T_MAX"] * tau
        dt = runtime / iterations

        ## FFT Related
        dump_dt = self.deck_info["DT"]
        f_max = 1 / (dump_dt)
        omega_max = (2 * pi * f_max) / omega0

        parameters = {
            "box_size": box_size,
            "dx": dx,
            "dt": dt,
            "runtime": runtime,
            "omega0": omega0,
            "tau": tau,
            "nc": nc,
            "pulse_width": pulse_width,
            "ne": ne,
            "temperature_ev": temperature_ev,
            "temperature": temperature,
            "lambdaD": lambdaD,
            "vth": vth,
            "omega_max": omega_max,
        }
        self.calculated_parameters = parameters
        return parameters

    def __space_node_to_space(self, node):
        """
        Converts node to space.
        """
        NX = self.deck_info["NX"]
        box_size = self.deck_info["X_MAX"] - self.deck_info["X_MIN"]
        return node * box_size / NX

    def __space_to_space_node(self, lam):
        """
        Converts space to node.
        """
        NX = self.deck_info["NX"]
        box_size = self.deck_info["X_MAX"] - self.deck_info["X_MIN"]
        return int(lam * NX / box_size)

    def __time_node_to_time(self, time_node):
        """
        Converts time_node to time.
        """
        t_max = self.deck_info["T_MAX"]
        num_files = len(self.files)
        dt = t_max / num_files
        return time_node * dt

    def __time_to_time_node(self, time):
        """
        Converts time to time_node.
        """
        t_max = self.deck_info["T_MAX"]
        num_files = len(self.files)
        dt = t_max / num_files
        return int(time / dt)

    def info(self):
        """
        Prints information about the directory.
        """
        if not self.__everything_calculated:
            available_data = self.__find_available_data()
            deck_info = self.__get_input_deck_info()
            calculated_parameters = self.__calculate_parameters()
            self.__everything_calculated = True
        else:
            available_data = self.available_data
            deck_info = self.deck_info
            calculated_parameters = self.calculated_parameters

        ad = "\t".join(available_data)

        patter = "------"
        string = ""
        string += f"\033[95mHere are the some infomation about the data in the directory: \033[92m{self.directory}\033[0m\n\n"
        string += f"\033[96mTotal number of sdf files: \033[0m{str(len(self.files))}\n"
        string += f"\033[93m{patter * 10}\033[0m\n"
        string += f"\033[96mAvailable data inside the sdf files:\033[0m\n\t"
        string += ad
        string += "\n"
        string += f"\033[93m{patter * 10}\033[0m\n"
        string += f"\033[96mInput deck information:\033[0m\n"
        for key, value in deck_info.items():
            string += f"\t{deck_info_map[key]}: {value:.4e}\n"
        string += f"\033[93m{patter * 10}\033[0m\n"
        string += f"\033[96mCalculated Parameters:\033[0m\n"
        for key, value in calculated_parameters.items():
            string += f"\t{calculated_parameters_map[key]}: {value:.4e}\n"
        string += f"\033[93m{patter * 10}\033[0m"
        self.__everything_calculated = True
        return string

    def print_info(self):
        print(self.info())

    def get_data(self, data_type="Ey", time_node=0, normalize=False):
        """
        Gets data from the directory.
        """

        if data_type not in self.available_data:
            raise DataNotFoundError(
                f"Data {data_type} is not available in the sdf files. Please check the input.deck. Available data are: {self.available_data}"
            )

        if time_node >= len(self.files):
            raise InvalidTimeError(
                f"No sdf file with time_node {time_node} is available. Maximum time_node is {len(self.files) - 1}."
            )

        file = self.files[time_node]
        raw_data = sdf.read(file, dict=True)
        raw_data = raw_data[transformation_dictionary[data_type]]
        data = raw_data.data
        if normalize:
            if data_type in ["Ne", "N"]:
                data = data / (self.calculated_parameters["nc"] + 1e-10)
            else:
                data = data / (max(data) + 1e-10)
        return data

    def __get_correct_time_range(self, time_range, are_nodes):
        if time_range is None:
            time_range = (0, len(self.files))
            return time_range

        if isinstance(time_range, int):
            time_range = [time_range]
            if time_range[0] >= len(self.files):
                time_range[0] = len(self.files) - 1
            if time_range[0] < 0:
                time_range[0] = 0
            return time_range

        if isinstance(time_range, float):
            time_range = [self.__time_to_time_node(time_range)]
            if time_range[0] >= len(self.files):
                time_range[0] = len(self.files) - 1
            if time_range[0] < 0:
                time_range[0] = 0
            return time_range

        if isinstance(time_range, list):
            dtype = type(time_range[0])
            new_time_range = []
            for time in time_range:
                if not isinstance(time, dtype):
                    raise TypeError(
                        "All the elements of the time_range list should be of the same type."
                    )
                if isinstance(time, float):
                    new_time_range.append(self.__time_to_time_node(time))
                else:
                    new_time_range.append(time)
            return new_time_range

        if not are_nodes:
            time_range = (
                self.__time_to_time_node(time_range[0]),
                self.__time_to_time_node(time_range[1]),
            )

        if time_range[0] > time_range[1]:
            raise InvalidTimeError(
                f"Invalid time range. The first element of the time range should be less than the second element. You entered {time_range}."
            )
        max_time = len(self.files)
        if time_range[0] < 0:
            time_range = (0, time_range[1])
        if time_range[1] > max_time:
            time_range = (time_range[0], max_time)

        return time_range

    def __get_correct_space_range(self, space_range, are_nodes):

        if space_range is None:
            space_range = (0, self.deck_info["NX"])
            return space_range

        if isinstance(space_range, int):
            space_range = [space_range]
            if space_range[0] >= self.deck_info["NX"]:
                space_range[0] = self.deck_info["NX"] - 1
            if space_range[0] < 0:
                space_range[0] = 0
            return space_range

        if isinstance(space_range, float):
            space_range = [self.__space_to_space_node(space_range)]
            if space_range[0] >= self.deck_info["NX"]:
                space_range[0] = self.deck_info["NX"] - 1
            if space_range[0] < 0:
                space_range[0] = 0
            return space_range

        if isinstance(space_range, list):
            dtype = type(space_range[0])
            new_space_range = []
            for space in space_range:
                if not isinstance(space, dtype):
                    raise TypeError(
                        "All the elements of the space_range list should be of the same type."
                    )
                if isinstance(space, float):
                    new_space_range.append(self.__space_to_space_node(space))
                else:
                    new_space_range.append(space)
            return new_space_range

        if not are_nodes:
            space_range = (
                self.__space_to_space_node(space_range[0]),
                self.__space_to_space_node(space_range[1]),
            )

        if space_range[0] > space_range[1]:
            raise InvalidSpaceError(
                f"Invalid space range. The first element of the space range should be less than the second element. You entered {space_range}."
            )
        max_space = self.deck_info["NX"]
        if space_range[0] < 0:
            space_range = (0, space_range[1])
        if space_range[1] > max_space:
            space_range = (space_range[0], max_space)
        return space_range

    def __get_correct_time_nodes_to_return(self, time_nodes):
        start = time_nodes[0]
        end = time_nodes[-1]
        length = end - start + 1
        start_natural = self.__time_node_to_time(start)
        end_natural = self.__time_node_to_time(end)
        return np.linspace(start_natural, end_natural, length)

    def __get_correct_space_nodes_to_return(self, space_nodes):
        start = space_nodes[0]
        end = space_nodes[-1]
        length = end - start + 1
        start_natural = self.__space_node_to_space(start)
        end_natural = self.__space_node_to_space(end)
        return np.linspace(start_natural, end_natural, length)

    def __load_data(
        self,
        data_types,
        normalize,
        time_node,
        space_nodes,
    ):
        """
        Loads specified data for the particular time node and (list of) space range.
        """
        temp_df = {}
        for data_type in data_types:
            data = self.get_data(
                data_type=data_type, time_node=time_node, normalize=normalize
            )
            data = data[space_nodes]
            temp_df[data_type] = data
        return temp_df

    def __create_time_and_space_nodes(
        self,
        time_range,
        space_range,
        times_are_nodes,
        space_are_nodes,
    ):

        time_range = self.__get_correct_time_range(time_range, times_are_nodes)
        space_range = self.__get_correct_space_range(space_range, space_are_nodes)
        return_time_range = False
        return_space_range = False

        if isinstance(time_range, tuple):
            time_range = range(time_range[0], time_range[1])
            return_time_range = True
        if isinstance(space_range, tuple):
            space_range = range(space_range[0], space_range[1])
            return_space_range = True

        space_nodes = np.array(space_range)
        time_nodes = np.array(time_range)

        return (
            time_nodes,
            space_nodes,
            return_time_range,
            return_space_range,
        )

    def load_data(
        self,
        data_types=["Ey"],
        normalize=False,
        time_range=None,
        space_range=None,
        times_are_nodes=True,
        space_are_nodes=True,
        return_data=False,
        overwrite=False,
    ):
        """
        Loads data from the directory and saves as attribute which can be accessed later

        Parameters
        ----------
        data_types : list, optional
            List of data types to be loaded, by default ["Ey"]
        normalize : bool, optional
            Whether to normalize the data or not, by default False

            If True, the data is normalized as:
            - For field values, the data is normalized by the maximum value of the data.
            - For density values, the data is normalized by the critical density.

        time_range : int, float, tuple or list, optional
            Time range to be loaded, by default None which means all the time range.
            - If int is provided, just that time node is loaded.
            - If float is provided, the time node closest to the time is loaded.
            - if list is provided, the nodes in the list are loaded.
            - If tuple is provided, the range is loaded.

        space_range : int, float, tuple or list, optional
            Space range to be loaded, by default None which means all the space range.
            - If int is provided, just that space node is loaded.
            - If float is provided, the space node closest to the space is loaded.
            - If tuple is provided, the range is loaded.
            - If list is provided, the nodes in the list are loaded.

        times_are_nodes : bool, optional
            Whether to use time nodes or time in tau, by default True which means that use the nodes.
        space_are_nodes : bool, optional
            Whether to use space nodes or space in lambda, by default True which means that use the nodes.
        return_data : bool, optional
            Whether to return the data or not, by default False
        overwrite : bool, optional
            Whether to overwrite the data if it is already loaded, by default False
        Returns
        -------
        None or dict
            If return_data is True, returns the data as a dictionary.
        """
        for data_type in data_types:
            if data_type not in self.available_data:
                raise DataNotFoundError(
                    f"Data {data_type} is not available in the sdf files. Please check the input.deck. Available data are: {self.available_data}"
                )
        (
            time_nodes,
            space_nodes,
            return_time_range,
            return_space_range,
        ) = self.__create_time_and_space_nodes(
            time_range, space_range, times_are_nodes, space_are_nodes
        )
        data_dict = {}
        for data_type in data_types:
            data_dict[data_type] = np.zeros((len(time_nodes), len(space_nodes)))
        for i, time_node in tqdm.tqdm(
            enumerate(time_nodes), total=len(time_nodes), desc="Loading Data..."
        ):
            temp_df = self.__load_data(
                data_types=data_types,
                normalize=normalize,
                time_node=time_node,
                space_nodes=space_nodes,
            )
            for data_type in data_types:
                data_dict[data_type][i] = temp_df[data_type]

        if return_time_range:
            time_nodes_natural = self.__get_correct_time_nodes_to_return(time_nodes)
        else:
            time_nodes_natural = time_nodes

        if return_space_range:
            space_nodes_natural = self.__get_correct_space_nodes_to_return(space_nodes)
        else:
            space_nodes_natural = space_nodes

        if self.data == {} or overwrite:
            for key in data_dict.keys():
                self.data[key] = data_dict[key]
            self.time_nodes_natural = time_nodes_natural
            self.space_nodes_natural = space_nodes_natural
            self.time_nodes = time_nodes
            self.space_nodes = space_nodes

        if return_data:
            return data_dict, time_nodes_natural, space_nodes_natural

    def plot_density(
        self,
        normalize=False,
        time_range=None,
        space_range=None,
        times_are_nodes=True,
        space_are_nodes=True,
        file_name=None,
        format="png",
        show_fig=True,
        **kwargs,
    ):
        """
        Plots the elctron density as image plot

        Parameters
        ----------
        normalize : bool, optional
            Whether to normalize the data or not, by default False

            If True, the data is normalized by the critical density.

        time_range : tuple  optional
            Time range to be loaded, by default None which means all the time range.
        space_range : tuple, optional
            Space range to be loaded, by default None which means all the space range.
        times_are_nodes : bool, optional
            Whether to use time nodes or time in tau, by default True which means that use the nodes.
        space_are_nodes : bool, optional
            Whether to use space nodes or space in lambda, by default True which means that use the nodes.
        file_name : str, optional
            File name to save the plot, by default None which means that the plot is not saved.
        format : str, optional
            Format of the file to save the plot, by default "png"
            You can pas the format to the `file_name` as well.
        **kwargs : dict
            Keyword arguments for `plt.imshow`
        """
        time_nodes, space_nodes, _, _ = self.__create_time_and_space_nodes(
            time_range, space_range, times_are_nodes, space_are_nodes
        )

        # Check if the data is loaded and the range is compatible
        load_needed = False
        if self.data == {}:
            print("Data is not loaded. Loading data...")
            load_needed = True

        elif self.time_nodes[0] > time_nodes[0] or self.time_nodes[-1] < time_nodes[-1]:
            print("Time range is not compatible. Loading data...")
            load_needed = True

        elif (
            self.space_nodes[0] > space_nodes[0]
            or self.space_nodes[-1] < space_nodes[-1]
        ):
            print("Space range is not compatible. Loading data...")
            load_needed = True

        if load_needed:
            data, new_time_range, new_space_range = self.load_data(
                data_types=["Ne"],
                normalize=normalize,
                time_range=time_range,
                space_range=space_range,
                times_are_nodes=times_are_nodes,
                space_are_nodes=space_are_nodes,
                return_data=True,
            )
            final_data = data["Ne"]
            # Set the extent of the plot
            EXTENT = [
                new_space_range[0],
                new_space_range[-1],
                new_time_range[-1],
                new_time_range[0],
            ]
        else:
            data = self.data["Ne"]

            # Slice the data to the correct range
            lower_time = np.where(
                np.round(self.time_nodes_natural, 1) == time_range[0]
            )[0][0]
            upper_time = np.where(
                np.round(self.time_nodes_natural, 1) == time_range[-1]
            )[0][0]
            lower_space = np.where(
                np.round(self.space_nodes_natural, 1) == space_range[0]
            )[0][0]
            upper_space = np.where(
                np.round(self.space_nodes_natural, 1) == space_range[-1]
            )[0][0]
            final_data = data[
                lower_time : upper_time + 1, lower_space : upper_space + 1
            ]
            EXTENT = [
                self.space_nodes_natural[lower_space],
                self.space_nodes_natural[upper_space],
                self.time_nodes_natural[upper_time],
                self.time_nodes_natural[lower_time],
            ]

        # If data is normalized but user passes `normalize=False` then we need to multiply by the critical density
        if not normalize:
            if max(final_data.flatten()) < 1e10:
                final_data *= self.calculated_parameters["nc"]

        fig, ax = plt.subplots(figsize=(10, 10))
        im = ax.imshow(final_data, extent=EXTENT, **kwargs)
        plt.colorbar(im).set_label("$n_e \, [n_c]$")
        ax.set_xlabel("$X \, [\lambda]$")
        ax.set_ylabel("$T \, [\\tau]$")
        ax.set_title("Electron Density")

        if file_name is not None:
            file_name = self.__get_save_file_name(file_name, format)
            plt.tight_layout()
            print(f"Saving plot to {file_name}...")
            fig.savefig(file_name, dpi=200)
        if show_fig:
            plt.show()
        return fig, ax

    def plot_fft(
        self,
        field="Ey",
        node=None,
        xlim="max",
        ylim=None,
        file_name=None,
        format=None,
        ylog=True,
        plot_lines=False,
        show_fig=True,
        return_fig = False
    ):
        try:
            id_ = np.where(self.space_nodes == node)[0][0]
        except IndexError:
            raise InvalidSpaceError(
                f"The provided node {node} is invalid. Probably because you have provided the node in natural units or the corresponding data is not loaded. Available nodes are: {list(self.space_nodes)}"
            )

        F = self.data[field][:, id_]
        if F.max() > 10:
            F = F / (max(F) + 1e-10)
        y0 = np.fft.fft(F)
        y0_shift = np.fft.fftshift(y0)
        y0_f = np.abs(y0_shift)

        omega_max = self.calculated_parameters["omega_max"]
        omega = np.linspace(-omega_max / 2, omega_max / 2, len(y0_f))

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(omega, np.abs(y0_f) * 2)
        ax.set_xlabel("$\omega [\omega_0]$")
        ax.set_ylabel("$|FFT|^2$")
        ax.set_title(f"FFT at Node {node}")

        if ylog:
            ax.set_yscale("log")

        if xlim == "max":
            xlim = (0, omega_max / 2)
            xticks = np.arange(1, omega_max // 2 + 1, 2)
        elif xlim is not None:
            if xlim[0] // 2:
                xticks = np.arange(xlim[0] // 2, xlim[1], 2)
            else:
                xticks = np.arange(xlim[0] // 2 + 1, xlim[1], 2)
        else:
            xticks = None

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        if xticks is not None:
            ax.set_xticks(xticks)

        if plot_lines:
            points = np.arange(1, int(xlim[1]) + 1, 2)
            middle_y = (np.abs(y0_f) * 2).mean()
            for p in points:
                ax.axvline(p, color="red", linestyle="--")
                ax.annotate(f"{p}", (p, middle_y))

        if file_name is not None:
            file_name = self.__get_save_file_name(file_name, format)
            plt.tight_layout()
            print(f"Saving plot to {file_name}...")
            fig.savefig(file_name, dpi=200)
        if show_fig:
            plt.show()
        if return_fig:
            return fig, ax

    def plot_ffts(
        self,
        field="Ey",
        xlim="max",
        ylim=None,
        prefix=None,
        format="png",
        ylog=True,
        plot_lines=False,
        show_fig = False,
        return_fig = False,
    ):
        figures = []
        axes = []
        for node in self.space_nodes:
            if prefix:
                file_name = f"{prefix}_node_{node}.{format}"
            else:
                file_name = None
            fig, ax = self.plot_fft(
                field=field,
                node=node,
                xlim=xlim,
                ylim=ylim,
                ylog=ylog,
                file_name=file_name,
                plot_lines=plot_lines,
                show_fig=False,
                return_fig= True,
            )
            figures.append(fig)
            axes.append(ax)
        if show_fig:
            for i, fig in enumerate(figures):
                print(f"Figure for node {self.space_nodes[i]}")
                plt.show()
                plt.pause(0.5)
        if return_fig:
            return_list = [(fig, ax) for fig, ax in zip(figures, axes)]
            return return_list