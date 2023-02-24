
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams["font.size"] = 24
import glob
import sdf
import tqdm
from scipy.integrate import quad
from epoch_viz.viz import EpochViz


def prepare(p):
    c = 3*1e8
    e = 1.6*1e-19
    m=9.1*1e-31
    lambda0 = 1e-6
    tau=lambda0/c
    las_time = 20*tau
    omega0 = 2*np.pi*c/lambda0
    Er = m * omega0 * c / e
    nx = 16000
    t_end =40*tau
    dt_snapshot = 0.08e-15
    x_min = -20*lambda0
    x_max = 20*lambda0
    factor =4
    epsilon = 8.85418782e-12
    nc = epsilon*m*omega0**2/e**2
    n0 = factor*nc


    las_time = 20
    DIR = f"SG_{p}"


    def super_gaus(t,p):
        mu=las_time/2
        sigma=las_time*0.15
        n = (t-mu)**p
        d = sigma**p
        e_0 = np.sin(2*np.pi*t)
        res = np.exp(-n/d)*e_0
        return res
    
    ez = EpochViz(DIR) 

    samples = len(ez.files)
    t_max = las_time
    t = np.linspace(0, t_max, samples)
    t2 = np.linspace(0, 2*t_max, samples)


    # gaus_ps = {}
    # ps = [2, 4, 6, 8, 10, 12]
    # for p_ in ps:
    #     gaus_ps[p_] = super_gaus(t, p_)


    Ey,T,X = ez.load_data(['Ey'],
    normalize=False,
    space_range=[0, 8000],
    time_range=None,
    overwrite=True,
    return_data=True
        ) 

    # Et0 = Ey['Ey'][:, 0]
    # Et1 = Ey['Ey'][:, 1]

    # Et0 = Et0/np.max(Et0)
    # Et1 = Et1/np.max(Et1)

    # plt.figure()
    # plt.plot(t2,Et0,label='Simulation')
    # plt.plot(t,gaus_ps[p],label=f'p={p}')
    # plt.legend()
    # plt.xlabel(r'Time $[\tau]$')
    # plt.ylabel(r'Normalized Electric Field')
    # plt.title(f'Electric Field at $x=0$ for $p={p}$')
    # plt.xlim(0, 20)
    # plt.savefig(f"images/{DIR}.png")
    # plt.close()

    # fig, ax = ez.plot_fft(node = 8000, plot_lines=True, return_fig=True, show_fig=False)
    # ax.set_title(f"FFT of Electric Field for $p={p}$")
    # fig.savefig(f"images/{DIR}_fft.png")
    # plt.close()
    omega, fy = ez.plot_fft(node = 8000, return_data=True, show_fig=False)
    return omega, fy

if __name__ == "__main__":
    # ps = [2, 4, 6, 8, 10, 12]
    # for p in ps:
    #     prepare(p)
    # omega, fy = prepare(2)
    plt.figure()
    ps = [2, 4, 6, 8]



    font = {
        'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 24,
    }
    for p in ps:
        omega, fy = prepare(p)
        plt.plot(omega, fy, label=f'$p={p}$')
        plt.xlabel(r'Frequency $[\omega_0]$', fontdict=font)
        plt.ylabel(r'Normalized Electric Field', fontdict=font)
        plt.yscale('log')
        plt.xlim(0, 20)
        plt.ylim(1e-2, )
        plt.legend()
    plt.savefig(f"images/SG_ffts_2-8.png")
    # for p in ps:
    #     omega, fy = prepare(p)
    #     plt.plot(omega, fy, label=f'p={p}')
    #     plt.xlabel(r'Frequency $[\omega_0]$')
    #     plt.ylabel(r'Normalized Electric Field')
    #     plt.yscale('log')
    #     plt.xlim(0, 20)
    #     plt.ylim(1e-2,1e+2 )
    #     plt.legend()
    # plt.savefig(f"images/SG_ffts_2-8.png")
    plt.show()
