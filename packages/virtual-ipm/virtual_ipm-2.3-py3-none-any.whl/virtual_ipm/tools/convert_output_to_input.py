import argparse
import sys

import pandas as pd
from scipy.constants import physical_constants

from virtual_ipm.simulation.particle_generation.models import DirectPlacement
from virtual_ipm.simulation.output import BasicRecorder


parser = argparse.ArgumentParser(
    description='Converts output to input files, so they can be reused in subsequent simulations. '
                'Only works for non-relativistic particle data.'
)
parser.add_argument('from')
parser.add_argument('to')
parser.add_argument('--mass', default='electron mass',
                    help='The mass of the tracked particles. This is required because momenta '
                         'need to be converted to velocities. Can be a string which denotes a '
                         'constant in scipy.constants.physical_constants or a number specifying '
                         'the mass in [kg].')
parser.add_argument('--stage', default='initial', choices=('initial', 'final'),
                    help='Since the given output file contains both, initial and final particle data, '
                         'the --stage parameter can be used to select between the two stages. '
                         'When "final" is selected, the simulation step data in the generated input file '
                         'is set to zero.')

pd.options.mode.chained_assignment = None


def main():
    args = parser.parse_args()
    df = pd.read_csv(getattr(args, 'from'))

    columns = [BasicRecorder.possible_column_names[x] for x in [
        f'{args.stage} sim. step',
        f'{args.stage} x',
        f'{args.stage} y',
        f'{args.stage} z',
        f'{args.stage} px',
        f'{args.stage} py',
        f'{args.stage} pz'
    ]]
    if not (set(columns) < set(df.columns)):
        print('Error: The following columns are required {}'.format(columns))
        sys.exit(1)

    # Select only the required columns.
    df = df[columns]

    # Rename the columns as required by the `DirectPlacementModel`.
    df.columns = DirectPlacement.column_names

    # Because the `DirectPlacementModel` expects velocities we need
    # to convert the momenta from the output file.
    try:
        particle_mass = float(args.mass)
    except ValueError:
        particle_mass = physical_constants[args.mass][0]
    df[['vx', 'vy', 'vz']] /= particle_mass

    if args.stage == 'final':
        df['simulation step'] = 0

    df.to_csv(args.to, index=False)

    return 0


if __name__ == '__main__':
    sys.exit(main())
