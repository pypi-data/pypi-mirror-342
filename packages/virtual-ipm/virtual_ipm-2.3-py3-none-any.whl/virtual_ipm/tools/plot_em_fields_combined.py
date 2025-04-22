from argparse import ArgumentParser
from ast import literal_eval
from collections import deque
from pathlib import Path
import re
import sys

from anna import load_from_file as load_configuration_from_file
import matplotlib.pyplot as plt
import numpy as np
from rich import print
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rx.concurrency import current_thread_scheduler
from scipy.constants import speed_of_light

from virtual_ipm.control.threading import SimulationThread
from virtual_ipm.log import add_handler, SubjectHandler


USAGE_INFO = '''\
This command line tool can be used to plot electric or magnetic fields
from an XML configuration file. It can be used to plot the combined fields
from beam(s) and guiding fields, or, by beams of modifying the configuration
file, only one of these fields (see below for more info).

The electric/magnetic fields are evaluated exactly as they are defined in the
given XML configuration. Hence, it is up to the user to correctly update the
configuration file in order to control what quantities enter in the evaluated
fields.

Plotting only beam fields
-------------------------

If only the beam fields are to be plotted, the configuration file should contain
the `NoElectricField` or `NoMagneticField` guiding fields models. This will
eliminate the contribution of guiding fields.

Plotting only guiding fields
----------------------------

If only the guiding fields are to be plotted, the configuration file should set
the `ElectricFieldOFF` or `MagneticFieldOFF` parameters to `true` for each of the
beam instances. This will eliminate the contribution of beam fields.
\N{NO-BREAK SPACE}
'''

XYZ_INFO = '''\
The grid points in {dim}-dimension for evaluating the fields (in units of meters). \
Must be given in one of the following formats:
* "linspace(<start>, <stop>, <step>)", where <start> and <stop> must be \
  the boundary coordinates as floating point numbers and <step> must be \
  the number of grid points along that dimension. This format directly \
  translates to the corresponding `numpy.linspace` function call.\
* "[<p1>, <p2>, ..., <pn>]" where <p1>, <p2>, ..., <pn> are floating point \
  numbers representing the individual grid points along that dimension. \
  This format directly translates to a `numpy.array`.
'''

parser = ArgumentParser(usage=USAGE_INFO)
parser.add_argument('config', type=Path, help='Path to an XML configuration file.')
parser.add_argument('--x', type=str, help=XYZ_INFO)
parser.add_argument('--y', type=str, help=XYZ_INFO)
parser.add_argument('--z', type=str, help=XYZ_INFO)
parser.add_argument(
    '--t-offset', type=float, default=0,
    help='The time offset for the field evaluation in units of seconds.',
)
parser.add_argument(
    '--x-offset', type=float, default=0,
    help=(
        'The x-position offset for the field evaluation in units of meters. '
        'If --x is given, this parameter has no effect.'
    ),
)
parser.add_argument(
    '--y-offset', type=float, default=0,
    help=(
        'The y-position offset for the field evaluation in units of meters. '
        'If --y is given, this parameter has no effect.'
    ),
)
parser.add_argument(
    '--z-offset', type=float, default=0,
    help=(
        'The z-position offset for the field evaluation in units of meters. '
        'If --z is given, this parameter has no effect.'
    ),
)
parser.add_argument(
    '--fields', type=str, required=True,
    help='Up to two fields from Ex,Ey,Ez or Bx,By,Bz separated by a comma.',
)
parser.add_argument(
    '--position-axis-unit', choices=('m', 'mm', 'um'), default='mm',
    help='The unit to use for the position axis/axes.',
)
parser.add_argument(
    '--field-axis-unit', choices=('V/m', 'kV/m', 'MV/m'), default='V/m',
    help='The unit to use for the field axis.',
)
parser.add_argument('--simulation-logs-n-keep', type=int, default=20)
parser.add_argument('--figsize', type=str, help='Figure width and height in inches separated by \'x\' (e.g., "8x6").')
parser.add_argument(
    '--plot-kwargs', type=str,
    help=(
        'Any keyword arguments for the underlying matplotlib plotting function as a dictionary literal '
        '(e.g., "{\'color\': \'gray\'}"). The plotting functions are:\n'
        '* ax.plot for 1d plots (i.e., grid points for one spatial dimension were specified),\n'
        '* ax.pcolormesh for 2d plots with one field component (i.e., grid points for two spatial '
        'dimensions were defined and one field component),\n'
        '* ax.quiver for 2d plots with two field components (i.e., grid points for two spatial '
        'dimensions were defined and two field components)'
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


FIELD_AXIS_UNIT_CONVERSION_FACTOR = {
    'V/m': 1.0,
    'kV/m': 1e-3,
    'MV/m': 1e-6,
}
POSITION_AXIS_UNIT_CONVERSION_FACTOR = {
    'm': 1.0,
    'mm': 1e3,
    'um': 1e6,
}


class InputError(Exception):
    pass


class FakeProgress:
    def __init__(self, time):
        self.time = time


def parse_xyz(s):
    if s.startswith('linspace(') and s.endswith(')'):
        try:
            args_as_tuple = literal_eval(s.removeprefix('linspace'))
        except SyntaxError as err:
            raise InputError(
                f'Cannot parse grid point specification {s!r} '
                f'({err})'
            )
        else:
            if len(args_as_tuple) != 3:
                raise InputError(
                    f'When using the format "linspace(<start>, <stop>, <step>)" '
                    f'all three arguments <start>, <stop>, <step> must be given '
                    f'(received only {len(args_as_tuple)})'
                )
            return np.linspace(*args_as_tuple)
    elif s.startswith('[') and s.endswith(']'):
        try:
            result = literal_eval(s)
        except SyntaxError as err:
            raise InputError(
                f'Cannot parse grid point specification {s!r} '
                f'({err})'
            )
        else:
            if invalid := [x for x in result if not isinstance(x, float)]:
                raise InputError(
                    f'When using the format "[<p1>, <p2>, ..., <pn>]" all specified grid points '
                    f'must be floating point numbers '
                    f'(found {invalid[0]!r} which is of type {type(invalid[0])}).'
                )
            return np.array(result)


x2i = dict(x=1, y=2, z=3)
f2i = dict(x=0, y=1, z=2)


def plot_1d(
    positions,
    fields,
    *,
    grid_shape,
    plot_config,
    plot_kwargs,
    ax,
):
    ax.plot(
        positions[x2i[plot_config['x1']]],
        fields[f2i[plot_config['F1']]],
        **plot_kwargs,
    )
    ax.set_xlabel(_generate_position_axis_label(plot_config, 'x1'))
    ax.set_ylabel(_generate_field_axis_label(plot_config, 'F1'))


def plot_2d_heatmap(
    positions,
    fields,
    *,
    grid_shape,
    plot_config,
    plot_kwargs,
    ax,
):
    im = ax.pcolormesh(
        positions[x2i[plot_config['x1']]].reshape(grid_shape).squeeze().T,
        positions[x2i[plot_config['x2']]].reshape(grid_shape).squeeze().T,
        fields[f2i[plot_config['F1']]].reshape(grid_shape).squeeze().T,
        shading='nearest',
        **plot_kwargs,
    )
    ax.set_xlabel(_generate_position_axis_label(plot_config, 'x1'))
    ax.set_ylabel(_generate_position_axis_label(plot_config, 'x2'))
    ax.get_figure().colorbar(im).set_label(_generate_field_axis_label(plot_config, 'F1'))


def plot_2d_quiver(
    positions,
    fields,
    *,
    grid_shape,
    plot_config,
    plot_kwargs,
    ax,
):
    F1 = fields[f2i[plot_config['F1']]].reshape(grid_shape).squeeze()
    F2 = fields[f2i[plot_config['F2']]].reshape(grid_shape).squeeze()
    ax.quiver(
        positions[x2i[plot_config['x1']]].reshape(grid_shape).squeeze(),
        positions[x2i[plot_config['x2']]].reshape(grid_shape).squeeze(),
        F1,
        F2,
        np.sqrt(F1**2 + F2**2),
        angles='uv',
    )
    ax.set_xlabel(_generate_position_axis_label(plot_config, 'x1'))
    ax.set_ylabel(_generate_position_axis_label(plot_config, 'x2'))


def _generate_position_axis_label(plot_config, key):
    unit = dict(m='m', mm='mm', um='$\\mu m$')[plot_config["position_axis_unit"]]
    return f'${plot_config[key]}$ [{unit}]'


def _generate_field_axis_label(plot_config, key):
    symbol = dict(electric='E', magnetic='B')[plot_config["em_choice"]]
    unit = plot_config["field_axis_unit"]
    return f'${symbol}_{plot_config[key]}$ [{unit}]'


def main():
    args = parser.parse_args()

    console = Console()
    layout = Layout(size=console.size.height//2)  # TODO: somehow, this is not effective.
    layout.split_row(
        Layout(name='main'),
        Layout(name='simulation'),
    )

    info_messages = deque(maxlen=20)

    def _process_info_message(msg):
        info_messages.append(msg)
        layout['main'].update(
            Panel(
                '\n'.join(info_messages),
                title='Info',
            ),
        )

    log_messages = deque(maxlen=args.simulation_logs_n_keep)

    def _process_simulation_log_message(msg):
        log_messages.append(msg)
        layout['simulation'].update(
            Panel(
                '\n'.join(log_messages),
                title='Simulation Logs',
            ),
        )

    log_handler = SubjectHandler()
    log_subscription = (
        log_handler.records
            .observe_on(current_thread_scheduler)
            .subscribe(on_next=_process_simulation_log_message)
    )
    add_handler(log_handler)

    plot_config = {
        'F1': None, 'F2': None, 'em_choice': None,
        'position_axis_unit': args.position_axis_unit,
        'field_axis_unit': args.field_axis_unit,
    }

    fields = [s.strip() for s in args.fields.split(',')]
    if invalid := [s for s in fields if not re.match('[EB][xyz]', s)]:
        raise InputError(
            f'Fields must be specified as one of `Ex,Ey,Ez` or `Bx,By,Bz` '
            f'(found {invalid[0]!r}.'
        )
    first, *others = fields
    if len(others) > 1:
        raise InputError(
            'At maximum two fields may be specified.'
        )
    for s in others:
        if s == first:
            raise InputError(
                f'Each field may only be specified once but {first} was '
                f'specified multiple times.'
            )
        if not re.match(f'{first[0]}[xyz]', s):
            raise InputError(
                f'All specified fields must be either electric (E) or magnetic (B). '
                f'Found {first!r} and {s!r}.'
            )
    for i, s in enumerate([first, *others], start=1):
        plot_config[f'F{i}'] = s[1:]
    plot_config['em_choice'] = dict(E='electric', B='magnetic')[first[0]]

    t = args.t_offset
    if args.x and args.y and args.z:
        raise InputError(
            'Only one- or two-dimensional grids are supported. '
            'That is, only one or two out of `--x, --y, --z` may be specified.'
        )
    elif args.x and args.y:
        x = parse_xyz(args.x)
        y = parse_xyz(args.y)
        z = args.z_offset
        plot_config['x1'] = 'x'
        plot_config['x2'] = 'y'
    elif args.x and args.z:
        x = parse_xyz(args.x)
        y = args.y_offset
        z = parse_xyz(args.z)
        plot_config['x1'] = 'x'
        plot_config['x2'] = 'z'
    elif args.y and args.z:
        x = args.x_offset
        y = parse_xyz(args.y)
        z = parse_xyz(args.z)
        plot_config['x1'] = 'y'
        plot_config['x2'] = 'z'
    elif args.x:
        x = parse_xyz(args.x)
        y = args.y_offset
        z = args.z_offset
        plot_config['x1'] = 'x'
        plot_config['x2'] = None
    elif args.y:
        x = args.x_offset
        y = parse_xyz(args.y)
        z = args.z_offset
        plot_config['x1'] = 'y'
        plot_config['x2'] = None
    elif args.z:
        x = args.x_offset
        y = args.y_offset
        z = parse_xyz(args.z)
        plot_config['x1'] = 'z'
        plot_config['x2'] = None
    else:
        raise InputError(
            'At least one of `--x, --y, --z` must be specified.'
        )
    x = np.atleast_1d(x)
    y = np.atleast_1d(y)
    z = np.atleast_1d(z)

    if plot_config['x2'] is None:
        assert plot_config['F1']
        if plot_config['F2']:
            raise InputError(
                'For 1d plots with one spatial grid dimension also only one '
                'field comonent may be specified.'
            )
        plot_func = plot_1d
    elif plot_config['F2'] is None:
        plot_func = plot_2d_heatmap
    else:
        plot_func = plot_2d_quiver

    eval_em_fields_method_name = f'{plot_config["em_choice"]}_field_at'

    _process_info_message(f'Time set to {t:.3e} seconds')
    _process_info_message(f'Using a {len(x)}x{len(y)}x{len(z)} xyz-grid with the following boundaries:')
    _process_info_message(f'X: {np.array(sorted({min(x), max(x)}))} meters')
    _process_info_message(f'Y: {np.array(sorted({min(y), max(y)}))} meters')
    _process_info_message(f'Z: {np.array(sorted({min(z), max(z)}))} meters')
    _process_info_message(f'Field evaluation via: {eval_em_fields_method_name}')
    _process_info_message(f'Plot function: {plot_func.__name__}')

    x_grid, y_grid, z_grid = np.meshgrid(x, y, z)
    positions = np.stack(
        [
            np.full_like(x_grid.ravel(), speed_of_light*t),
            x_grid.ravel(),
            y_grid.ravel(),
            z_grid.ravel(),
        ],
        axis=0,
    )

    with Live(layout, refresh_per_second=4):
        simulation = SimulationThread()
        simulation.setup(load_configuration_from_file(f'{args.config.resolve()}'))
        simulation.prepare()
        em_fields_component = simulation._simulation._particle_tracking._em_fields
        fields = getattr(em_fields_component, eval_em_fields_method_name)(positions, FakeProgress(t))

    fields *= FIELD_AXIS_UNIT_CONVERSION_FACTOR[plot_config['field_axis_unit']]

    subplots_kwargs = {}
    if args.figsize:
        try:
            w, h = args.figsize.split('x')
        except ValueError:
            raise RuntimeError('Figure size must be given in the format WxH.')
        subplots_kwargs['figsize'] = (float(w), float(h))
    fig, ax = plt.subplots(**subplots_kwargs)
    plot_func(
        positions*POSITION_AXIS_UNIT_CONVERSION_FACTOR[args.position_axis_unit],
        fields,
        grid_shape=x_grid.shape,
        plot_config=plot_config,
        plot_kwargs=literal_eval(args.plot_kwargs or '{}'),
        ax=ax,
    )
    if args.save:
        fig.savefig(args.save, **(literal_eval(args.savefig_kwargs or '{}')))
    if not args.no_show:
        plt.show()
    return 0


if __name__ == '__main__':
    sys.exit(main())
