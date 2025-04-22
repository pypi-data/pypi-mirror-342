from argparse import ArgumentParser
from ast import literal_eval
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import elementary_charge

from anna import load_from_file
from virtual_ipm.control.threading import SimulationThread
from virtual_ipm.simulation.particle_generation.models import DirectPlacement


parser = ArgumentParser(
    usage=(
        'This tool can be used to plot the energy–scattering angle distribution of '
        'initial particles directly from an XML configuration file.'
    ),
)
parser.add_argument('config', type=Path, help='Path to XML configuration file.')
parser.add_argument('--n-particles', type=int, default=10**5, help='The number of particles to be generated.')
parser.add_argument('--n-bins-energy', type=int, default=100, help='The number of bins for the energy dimension of the histogram.')
parser.add_argument('--n-bins-theta', type=int, default=100, help='The number of bins for the scattering angle dimension of the histogram.')
parser.add_argument(
    '--energy-axis-limits', type=str,
    help=(
        'The axis limits for the energy dimension of the histogram as a list literal '
        '(e.g., "[0.1, 100]").'
    ),
)
parser.add_argument(
    '--theta-axis-limits', type=str,
    help=(
        'The axis limits for the scattering angle dimension of the histogram as a list literal '
        '(e.g., "[0.2, 0.8]"). Note that the scattering angle axis is plotted in units of pi.'
    ),
)
parser.add_argument('--figsize', type=str, help='Figure width and height in inches separated by \'x\' (e.g., "8x6").')
parser.add_argument('--cmap', type=str, help='The color map to be used for the histogram.')
parser.add_argument(
    '--hist2d-kwargs', type=str,
    help=(
        'Any keyword arguments for the matplotlib hist2d function as a dictionary literal '
        '(e.g., "{\'density\': True}").'
    ),
)
parser.add_argument('--save', type=Path, help='File path for saving the figure.')
parser.add_argument(
    '--savefig-kwargs', type=str,
    help=(
        'Any keyword arguments for the Matplotlib savefig function as a dictionary literal '
        '(e.g., "{\'dpi\': 600}").'
    ),
)
parser.add_argument('--no-show', action='store_true', help='Don\'t show the figure.')


def main():
    args = parser.parse_args()

    simulation = SimulationThread()
    simulation.setup(load_from_file(f'{args.config.resolve()}'))
    simulation.prepare()

    model = simulation._simulation._particle_generation._model
    if model is DirectPlacement:
        momenta = model._data_frame[['vx', 'vy', 'vz']].to_numpy().T * model._mass
    else:
        model.compute_number_of_particles_to_be_created = lambda _: args.n_particles
        momenta = model.generate_momenta(None)  

    energy = (momenta**2).sum(axis=0) / (2*simulation._simulation._setup.particle_type.mass)
    energy /= elementary_charge  # [J] --> [eV]

    theta = np.arctan2(momenta[0], momenta[2])
    theta /= np.pi  # [rad] --> [pi]

    subplots_kwargs = {}
    if args.figsize:
        try:
            w, h = args.figsize.split('x')
        except ValueError:
            raise RuntimeError('Figure size must be given in the format WxH.')
        subplots_kwargs['figsize'] = (float(w), float(h))
    fig, ax = plt.subplots(**subplots_kwargs)
    hist2d_kwargs = {}
    if args.cmap:
        hist2d_kwargs['cmap'] = args.cmap
    if args.hist2d_kwargs:
        hist2d_kwargs.update(literal_eval(args.hist2d_kwargs))
    ax.hist2d(
        energy,
        theta,
        bins=(
            np.logspace(np.log10(energy.min()), np.log10(energy.max()), args.n_bins_energy),
            np.linspace(0, 1, args.n_bins_theta),
        ),
        **hist2d_kwargs,
    )
    ax.set(xlabel='Energy [eV]', ylabel='Scattering angle [$\\pi$]')
    ax.set_xscale('log')
    if args.energy_axis_limits:
        xlim = literal_eval(args.energy_axis_limits)
    else:
        xlim = [energy.min(), energy.max()]
    if args.theta_axis_limits:
        ylim = literal_eval(args.theta_axis_limits)
    else:
        ylim = [0, 1]
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    if args.save:
        fig.savefig(args.save, **(literal_eval(args.savefig_kwargs or '{}')))
    if not args.no_show:
        plt.show()
    return 0


if __name__ == '__main__':
    sys.exit(main())
