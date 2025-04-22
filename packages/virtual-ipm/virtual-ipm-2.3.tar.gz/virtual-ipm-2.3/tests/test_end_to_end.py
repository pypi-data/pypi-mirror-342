from functools import partial
import os
from pathlib import Path
import tempfile

import matplotlib.pyplot as plt
import numpy as np
import pytest

from virtual_ipm.auxiliaries import run_simulation


# Use a smaller number of bins than are contained in the reference profiles
# in order to decrease the probability of failure. Note that the probability
# of failure is `1 - (1 - 1/N)**B` (with N: number of profiles, B: number of bins).
N_BINS = dict(linac=40, lhc=50)


def _rebin(profiles, *, n_bins, method=np.sum):
    return method(profiles.reshape(*profiles.shape[:-1], n_bins, -1), axis=-1)


@pytest.mark.skipif(os.environ.get('VIPM_TEST_END_TO_END') != '1', reason='takes long to compute')
@pytest.mark.parametrize('prefix', ['linac', 'lhc'])
def test_case(prefix):
    out = run_simulation(Path(f'{prefix}.config.xml'), stdout=None)
    assert np.all(out['status'] == 'DETECTED')

    bin_edges = np.load(f'{prefix}.bin_edges.npy')
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    profiles = np.stack([
        np.histogram(out[f'{stage} x'], bins=bin_edges)[0]
        for stage in ('initial', 'final')
    ])
    ref = np.load(f'{prefix}.profiles.npy')

    _plot_profiles_and_ref_data(bin_centers*1e3, profiles, ref, save=prefix, ylog=False)
    _plot_profiles_and_ref_data(bin_centers*1e3, profiles, ref, save=prefix, ylog=True)

    _custom_rebin = partial(_rebin, n_bins=N_BINS[prefix])
    bin_centers = _custom_rebin(bin_centers, method=np.mean)
    profiles = _custom_rebin(profiles)
    ref = _custom_rebin(ref)

    _plot_profiles_and_ref_data(bin_centers*1e3, profiles, ref, save=prefix, ylog=False)
    _plot_profiles_and_ref_data(bin_centers*1e3, profiles, ref, save=prefix, ylog=True)

    for i, profile in enumerate(profiles):
        ref_min = ref[:,i].min(axis=0)
        ref_max = ref[:,i].max(axis=0)
        assert np.all(profile >= ref_min) and np.all(profile <= ref_max)


def _plot_profiles_and_ref_data(x, profiles, ref_data, *, save: str = None, ylog: bool = False):
    """Plot the given profiles with reference data as background.

    Args:
        x: array-like, shape: (B,)
            Positions of profile bins in [mm].
        profiles: array-like, shape: (2, B)
            Initial and final profile stacked along first axis.
        ref_data: array-like, shape: (N, 2, B)
            N reference profiles (initial and final stacked along second axis).
    """
    fig, axes = plt.subplots(ncols=2, figsize=(15,5))
    axes[0].set_title('initial')
    axes[1].set_title('final')
    for i, ax in enumerate(axes):
        profile = profiles[i]
        ref = ref_data[:,i]
        assert len(x) == len(profile) == ref.shape[1]
        ref_min = ref.min(axis=0)
        ref_max = ref.max(axis=0)
        bad = np.logical_or(profile < ref_min, profile > ref_max)
        ax.fill_between(x, ref_min, ref_max, color='tab:blue', alpha=0.3)
        ax.plot(x, profile, '-', color=f'tab:{"red" if bad.any() else "green"}')
        for pos in x[bad]:
            ax.axvline(pos, ls='--', lw=0.5, color='tab:red')
        if ylog:
            ax.set_yscale('log')
        ax.set(xlabel='x [mm]', ylabel='particle count [1]')
    if save:
        tmp = Path(tempfile.gettempdir())
        fig.savefig(tmp / f'vipm_test_end_to_end_{save}_N{len(ref_data)}_B{len(x)}_ylog{ylog!s}.png')
    return fig
