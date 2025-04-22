from pathlib import Path
from subprocess import run, DEVNULL
import tempfile

import numpy as np
import pandas as pd
import pytest


def test_zero_em_fields(read_template):
    result = _run_template(read_template('zero_em_fields.config.xml'))
    for p in ['x', 'y', 'z', 'px', 'py', 'pz']:
        assert np.array_equal(result[f'final {p}'], result[f'initial {p}'])


@pytest.mark.parametrize('dim', ['x', 'y', 'z'])
def test_electric_guiding_field(dim: str, read_template):
    template = read_template('zero_em_fields.config.xml')
    e_field = [0, 0, 0]
    e_field[ord(dim) - ord('x')] = 1e3
    template = template.replace(
        '<Model>NoElectricField</Model>',
        f'<Model>UniformElectricField</Model><Parameters><ElectricField unit="V/m">{e_field}</ElectricField></Parameters>'
    )
    result = _run_template(template)
    for p in ['x', 'y', 'z', 'px', 'py', 'pz']:
        unchanged = np.array_equal(result[f'final {p}'], result[f'initial {p}'])
        if p.endswith(dim):
            assert not unchanged
        else:
            assert unchanged


@pytest.mark.parametrize('dim', ['x', 'y', 'z'])
def test_magnetic_guiding_field(dim: str, read_template):
    template = read_template('zero_em_fields.config.xml')
    b_field = [0, 0, 0]
    b_field[ord(dim) - ord('x')] = 0.1
    template = template.replace(
        '<Model>NoMagneticField</Model>',
        f'<Model>UniformMagneticField</Model><Parameters><MagneticField unit="T">{b_field}</MagneticField></Parameters>'
    )
    template = template.replace('<Model>ZeroMomentum</Model>', '<Model>ThermalMotion</Model>')
    template = template.replace(
        '<ZPosition unit="m">0</ZPosition>',
        '<ZPosition unit="m">0</ZPosition><Mass unit="MeV/c^2">938</Mass><Temperature unit="K">300</Temperature>'
    )
    result = _run_template(template)
    for p in ['px', 'py', 'pz']:
        unchanged = np.array_equal(result[f'final {p}'], result[f'initial {p}'])
        if p.endswith(dim):
            assert unchanged
        else:
            assert not unchanged


def _run_template(template: str) -> pd.DataFrame:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        output = td / 'output.csv'
        config = td / 'config.xml'
        config.write_text(template.format(output_filename=str(output.resolve())))
        run(['virtual-ipm', str(config.resolve())], stdout=DEVNULL, stderr=DEVNULL, check=True)
        return pd.read_csv(output, index_col=0)
