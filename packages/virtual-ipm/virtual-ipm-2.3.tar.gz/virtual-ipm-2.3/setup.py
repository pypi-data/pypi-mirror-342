from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


def version():
    with open('virtual_ipm/VERSION') as f:
        return f.read()


setup(
    name='virtual-ipm',
    version=f'{version()}',
    description=(
        'Virtual-IPM is a software for simulating transverse profile monitors '
        'under the influence of beam space-charge and external fields.'
    ),
    long_description=readme(),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords=['IPM', 'BGI', 'BIF', 'beam instrumentation', 'beam diagnostics',
              'transverse profile monitor', 'simulation', 'framework',
              'ionization profile monitor', 'beam gas ionization profile monitor',
              'beam induced fluorescence monitor', 'space charge', 'particle accelerator'],
    url='https://gitlab.com/IPMsim/Virtual-IPM',
    author='Dominik Vilsmeier',
    author_email='dominik.vilsmeier1123@gmail.com',
    license='AGPL-3.0',
    packages=[
        'virtual_ipm',
        'virtual_ipm.control',
        'virtual_ipm.data',
        'virtual_ipm.di',
        'virtual_ipm.frontends',
        'virtual_ipm.frontends.gui',
        'virtual_ipm.frontends.gui.simulation',
        'virtual_ipm.frontends.gui.analysis',
        'virtual_ipm.frontends.gui.sweeps',
        'virtual_ipm.simulation',
        'virtual_ipm.simulation.beams',
        'virtual_ipm.simulation.beams.bunches',
        'virtual_ipm.simulation.devices',
        'virtual_ipm.simulation.devices.obstacles',
        'virtual_ipm.simulation.particle_generation',
        'virtual_ipm.simulation.particle_generation.ionization',
        'virtual_ipm.simulation.particle_tracking',
        'virtual_ipm.simulation.particle_tracking.em_fields',
        'virtual_ipm.simulation.particle_tracking.em_fields.guiding_fields',
        'virtual_ipm.simulation.particle_tracking.em_fields.guiding_fields.models',
        'virtual_ipm.tools',
        'virtual_ipm.utils',
        'virtual_ipm.utils.mathematics',
    ],
    entry_points={
        'console_scripts': [
            'virtual-ipm = virtual_ipm.run:main',
            'virtual-ipm-settle = virtual_ipm.settle:main',
            'vipm-cst-to-csv = virtual_ipm.tools.convert_cst_file_to_csv:main',
            'vipm-csv-to-xml = virtual_ipm.tools.convert_csv_output_to_xml_data_file:main',
            'vipm-out-to-in = virtual_ipm.tools.convert_output_to_input:main',
            'vipm-plot-beam-fields = virtual_ipm.tools.plot_beam_em_fields:main',
            'vipm-plot-em-fields = virtual_ipm.tools.plot_beam_em_fields:main',
            'vipm-plot-em-fields-combined = virtual_ipm.tools.plot_em_fields_combined:main',
            'vipm-plot-ddcs = virtual_ipm.tools.plot_ddcs:main',
        ],
        'gui_scripts': [
            'virtual-ipm-gui = virtual_ipm.start_gui:main',
        ],
    },
    install_requires=[
        'anna>=0.5.2',
        'injector==0.12.1',
        'ionics',
        'numpy>=1.18',
        'pandas',
        'pyhocon',
        'rich>=13.8',
        'rx<3.0',
        'scipy',
        'six',
    ],
    extras_require={
        'GUI': ['PyQt5', 'matplotlib>=3.2'],
        'Obstacles': ['trimesh[easy]'],
        'Tests': ['pytest', 'matplotlib'],
    },
    python_requires='>=3.9',
    include_package_data=True,
    zip_safe=False,
)
