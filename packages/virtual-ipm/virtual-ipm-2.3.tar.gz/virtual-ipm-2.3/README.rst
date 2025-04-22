|PyPI status| |Maintenance yes| |Documentation Status| |PyPI pyversions| |PyPI version| |GPLv3 license|

|
|
|

.. image:: https://gitlab.com/IPMsim/Virtual-IPM/-/raw/develop/logo.svg
   :align: center
   :width: 100%


Virtual-IPM
===========

Virtual-IPM is a software for simulating the electron/ion transport in Ionization Profile Monitors (IPM)
and other related devices, such as Beam Induced Fluorescence Monitors (BIF).
It can simulate quite general setups involving the space-charge fields from one or multiple particle beams
as well as the presence of external electric/magnetic guiding fields.
The application can be used from the command line but it offers a rich graphical user interface (GUI) as well.

The software has a modular structure which allows for great flexibility in terms of combining the various
different realizations of beam fields, external fields, detector geometry, etc.


Use cases
---------

The following list is a brief overview of possible `use cases <https://ipmsim.gitlab.io/Virtual-IPM/use-cases.html>`__:

* Beam profile deformation due to beam space-charge
* Beam profile deformation due to guiding field non-uniformities
* Gas-jet for IPM and BIF
* Simulating the effect of multiple beams on electron/ion transport


Components
----------

The following is an overview of the available implementations for the various modules:

+--------------+----------------+-----------------+-----------------------------------------+----------------------------+
| Bunch shapes | Bunch fields   | External fields | Devices                                 | Particle generation        |
+==============+================+=================+=========================================+============================+
| Uniform      | Uniform        | Uniform         | Ionization Profile Monitor (IPM)        | Ionization via beam (IPM): |
|              |                |                 |                                         |                            |
|              |                |                 |                                         | * at rest                  |
|              |                |                 |                                         | * parametrized DDCS        |
|              |                |                 |                                         | * DDCS by Voitkiv et al.   |
+--------------+----------------+-----------------+-----------------------------------------+----------------------------+
| Gaussian     | Gaussian       | 2D field maps   | Beam Induced Fluorescence Monitor (BIF) | Excitation via beam (BIF)  |
+--------------+----------------+-----------------+-----------------------------------------+----------------------------+
| Gaussian DC  | Gaussian DC    | 3D field maps   | Arbitrary CAD models (via .STL files)   | Thermal motion             |
+--------------+----------------+-----------------+-----------------------------------------+----------------------------+
| Generalized  | Generalized    | Thin Wire       |                                         | Gas jets                   |
| Gaussian     | Gaussian       | electric field  |                                         |                            |
+--------------+----------------+-----------------+-----------------------------------------+----------------------------+
| QGaussian    | QGaussian      |                 |                                         | Custom CSV files           |
+--------------+----------------+-----------------+-----------------------------------------+----------------------------+
| Hollow DC    | Hollow DC      |                 |                                         |                            |
+--------------+----------------+-----------------+-----------------------------------------+----------------------------+
| Parabolic    | Parabolic      |                 |                                         |                            |
| Ellipsoid    | Ellipsoid      |                 |                                         |                            |
+--------------+----------------+-----------------+-----------------------------------------+----------------------------+
|              | Poisson 2D SOR |                 |                                         |                            |
+--------------+----------------+-----------------+-----------------------------------------+----------------------------+
|              | Poisson 3D     |                 |                                         |                            |
+--------------+----------------+-----------------+-----------------------------------------+----------------------------+


Installation
------------

Virtual-IPM can be installed via ``pip`` with or without GUI components. ``pip install Virtual-IPM[GUI]`` installs
the application together with the graphical user interface while ``pip install Virtual-IPM`` just installs the command
line version. For more information see `the documentation <https://ipmsim.gitlab.io/Virtual-IPM/installation.html>`__.


Graphical User Interface
------------------------

`The GUI <https://ipmsim.gitlab.io/Virtual-IPM/usage.html#via-the-gui>`__
can be started via ``virtual-ipm-gui``. At the top, it offers buttons for various functionality:

* Create, save and load configuration files
* Run configurations
* Analyze simulation output
* `Create parameter sweeps <https://ipmsim.gitlab.io/Virtual-IPM/parameter-sweeps.html>`__


Command Line Usage
------------------

`The application <https://ipmsim.gitlab.io/Virtual-IPM/usage.html#via-the-command-line>`__
can be run from the command line via ``virtual-ipm path/to/config.xml``.
For customization and options see ``virtual-ipm --help``.

The application also ships with a number of other
`command line utilities <https://ipmsim.gitlab.io/Virtual-IPM/usage.html#command-line-tools>`__,
e.g. for plotting beam fields from configuration files.


Contributing
------------

Please contact `the maintainers <https://gitlab.com/IPMsim/Virtual-IPM/-/blob/develop/setup.py#L38>`__.


Relevant links
--------------

* `Documentation <https://ipmsim.gitlab.io/Virtual-IPM/>`__
* `Changelog / Release notes <https://ipmsim.gitlab.io/Virtual-IPM/changelog.html>`__
* `Examples <https://ipmsim.gitlab.io/Virtual-IPM/examples.html>`__
* `Issue tracker <https://gitlab.com/IPMsim/Virtual-IPM/-/issues>`__
* `Virtual-IPM on PyPI <https://pypi.org/project/virtual-ipm/>`__



.. |Maintenance yes| image:: https://img.shields.io/badge/maintained-yes-success.svg
   :target: https://gitlab.com/IPMsim/Virtual-IPM/-/releases

.. |PyPI version| image:: https://img.shields.io/pypi/v/virtual-ipm.svg
   :target: https://pypi.org/project/virtual-ipm/

.. |GPLv3 license| image:: https://img.shields.io/badge/license-AGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/virtual-ipm.svg
   :target: https://pypi.org/project/virtual-ipm/

.. |PyPI status| image:: https://img.shields.io/badge/status-stable-success.svg
   :target: https://pypi.org/project/virtual-ipm/

.. |Documentation Status| image:: https://img.shields.io/badge/documentation-yes-success.svg
   :target: https://ipmsim.gitlab.io/Virtual-IPM/
