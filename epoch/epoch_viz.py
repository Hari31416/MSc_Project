import sdf_helper as sh
import sdf
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors


plt.rcParams["font.size"] = 13


class EpochViz:
    def __init__(self, extent, data_dir=os.curdir):
        self.extent = extent
        self.data_dir = data_dir
        self.all_files = [f for f in os.listdir(self.data_dir) if f.endswith(".sdf")]

    def _implot_variable(
        self,
        variable,
        power=1,
        notmalize=False,
        ax=plt.gca(),
        cmap="jet",
        origin="lower",
        extent=EXTENT,
        aspect="auto",
        interpolation="nearest",
        xlabel="",
        ylabel="",
        title="",
        **kwargs,
    ):
        if normalize:
            variable = variable / (np.max(variable)+1e-10)
        variable = variable**power
        ax.imshow(
            variable,
            cmap=cmap,
            origin=origin,
            extent=extent,
            aspect=aspect,
            interpolation=interpolation,
            **kwargs,
        )
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

    def plot_field(self, data_id,ax=plt.gca(), component="y", single=False,**kwargs):
        raw_data = sdf.read(self.all_files[data_id], dict=True)
        comp = {
        "x":raw_data.Electric_Field_Ex,
        "y":raw_data.Electric_Field_Ey,
        "z":raw_data.Electric_Field_Ez,
        }
        t = raw_data.Header['time']*1e15
        if single:
            plt.figure(figsize=(15,8))
            title = f'$E_{component}$, $t={t:.0f}$ fs'
        else:
            title = f'$t={t:.0f}$ fs'
        variable = comp[component].data
        x_label = '$y \, [\mu m]$'
        y_label = '$x \, [\mu m]$'
        self._implot_variable(variable,ax=ax,xlabel=x_label,ylabel=y_label,title=title,**kwargs)