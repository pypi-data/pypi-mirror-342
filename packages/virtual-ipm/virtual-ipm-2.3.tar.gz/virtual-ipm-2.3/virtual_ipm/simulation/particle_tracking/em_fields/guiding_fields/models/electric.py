#    Virtual-IPM is a software for simulating IPMs and other related devices.
#    Copyright (C) 2021  The IPMSim collaboration <https://ipmsim.gitlab.io/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from anna import PhysicalQuantity, Triplet, parametrize
from anna.input import Unit
from anna.utils import use_docs_from
import injector
import numpy as np
import scipy.constants as constants

import virtual_ipm.di as di

from .mixin import GuidingFieldModel, CSVAdaptor2D, CSVAdaptor3D, UniformGuidingField


ONE_OVER_FOUR_PI_EPSILON_0 = 1 / (4*np.pi * constants.epsilon_0)



# noinspection PyAbstractClass,PyOldStyleClasses
class ElectricGuidingFieldModel(GuidingFieldModel):
    """
    (Abstract) Base class for electric guiding field models.
    """

    CONFIG_PATH_TO_IMPLEMENTATION = 'GuidingFields/Electric/Model'
    CONFIG_PATH = 'GuidingFields/Electric/Parameters'

    def __init__(self, configuration=None):
        super().__init__(configuration)

Interface = ElectricGuidingFieldModel


@parametrize(
    _field_vector=Triplet[PhysicalQuantity](
        'ElectricField', 'V/m'
    ).use_container(np.array)
)
class UniformElectricField(UniformGuidingField, ElectricGuidingFieldModel):
    """
    Constant, uniform electric field.
    """

    CONFIG_PATH = ElectricGuidingFieldModel.CONFIG_PATH

    @injector.inject(
        configuration=di.components.configuration
    )
    def __init__(self, configuration):
        super().__init__(configuration)


class NoElectricField(UniformElectricField):
    """
    Use this model if no electric field is present (zero electric field).
    """
    _field_vector = np.zeros(3, dtype=float)

    @injector.inject(
        configuration=di.components.configuration
    )
    def __init__(self, configuration=None):
        super().__init__(configuration=configuration)


class ElectricCSVAdaptor2D(CSVAdaptor2D, ElectricGuidingFieldModel):
    __doc__ = CSVAdaptor2D.__doc__.replace(
        'guiding field (either\n    electric of magnetic)',
        'electric guiding field',
    )

    CONFIG_PATH = ElectricGuidingFieldModel.CONFIG_PATH

    @injector.inject(
        configuration=di.components.configuration
    )
    def __init__(self, configuration):
        super().__init__(configuration)

    @use_docs_from(ElectricGuidingFieldModel)
    def eval(self, position_four_vector, progress):
        return super().eval(position_four_vector, progress)


class ElectricCSVAdaptor3D(CSVAdaptor3D, ElectricGuidingFieldModel):
    __doc__ = CSVAdaptor3D.__doc__.replace(
        'guiding field (either\n    electric of magnetic)',
        'electric guiding field',
    )

    CONFIG_PATH = ElectricGuidingFieldModel.CONFIG_PATH

    @injector.inject(
        configuration=di.components.configuration
    )
    def __init__(self, configuration):
        super().__init__(configuration)

    @use_docs_from(ElectricGuidingFieldModel)
    def eval(self, position_four_vector, progress):
        return super().eval(position_four_vector, progress)


Unit.register_dimension('line density', 'C/m')


@parametrize(
    PhysicalQuantity('LineChargeDensity', unit='C/m'),
    PhysicalQuantity(
        'Length', unit='m',
        info='The length of the wire along x-dimension.',
    ),
    PhysicalQuantity('YPosition', unit='m'),
    PhysicalQuantity(
        'XPosition', unit='m', default=0.,
        info='The position of the wire\'s center along x-dimension.',
    ),
    PhysicalQuantity('ZPosition', unit='m', default=0.),
)
class ThinWire(ElectricGuidingFieldModel):
    """
    The electric field of a thin, straight wire. By convention, the
    wire is positioned such that it extends along x-dimension and
    it is pointlike in y- and z-dimension. The specific position
    of the wire can be chosen via the parameters.

    The parameter ``LineChargeDensity`` :math:`\\lambda` serves as a
    scaling factor for the electric field. The resulting electric field
    is proportional to:
    
    .. math::

        \\vec{E} \\propto \\frac{\\lambda}{4\\pi\\epsilon_0}
    
    """

    @injector.inject(
        configuration=di.components.configuration
    )
    def __init__(self, configuration=None):
        super().__init__(configuration=configuration)

    @use_docs_from(ElectricGuidingFieldModel)
    def eval(self, position_four_vector, progress):
        # The implementation follows:
        # https://www.usna.edu/Users/physics/mungan/_files/documents/Scholarship/RodElectricField.pdf
        x_pos = position_four_vector[1] - self._x_position
        y_pos = position_four_vector[2] - self._y_position
        z_pos = position_four_vector[3] - self._z_position

        R = np.sqrt(y_pos**2 + z_pos**2)
        theta_L = -1*np.arctan2(self._length/2 + x_pos, R)
        theta_R =    np.arctan2(self._length/2 - x_pos, R)

        R_gt_0 = R > 0
        x_beyond_wire = np.abs(x_pos) > self._length/2
        R_eq_0_and_x_beyond_wire = ~R_gt_0 & x_beyond_wire
        prefactor = np.zeros_like(R)
        prefactor[R_gt_0] = ONE_OVER_FOUR_PI_EPSILON_0 * self._line_charge_density / R[R_gt_0]
        prefactor[R_eq_0_and_x_beyond_wire] = ONE_OVER_FOUR_PI_EPSILON_0 * self._line_charge_density
        # Technically, the field at `~mask_R_gt_0 & ~mask_x_beyond_wire` would diverge but we leave it
        # at zero to be computable.

        Ex  = np.zeros_like(prefactor)
        Eyz = np.zeros_like(prefactor)

        # Since R_gt_0 will be True for practically every particle, we perform the computation on
        # the entire array and only select on the result. All computed quantities are well defined
        # in all cases.
        Ex [R_gt_0] = (prefactor * (np.cos(theta_R) - np.cos(theta_L)))[R_gt_0]
        Eyz[R_gt_0] = (prefactor * (np.sin(theta_R) - np.sin(theta_L)))[R_gt_0]

        if R_eq_0_and_x_beyond_wire.any():
            # The implementation of this special case follows
            # http://online.cctt.org/physicslab/content/phyapc/lessonnotes/Efields/EchargedRods.asp
            b = np.abs(x_pos[R_eq_0_and_x_beyond_wire]) - self._length/2
            assert np.all(b > 0)
            Ex[R_eq_0_and_x_beyond_wire] = (
                prefactor[R_eq_0_and_x_beyond_wire]
                * np.sign(x_pos[R_eq_0_and_x_beyond_wire])
                * (1/b - 1/(self._length + b))
            )

        # Angle measured in yz-plane where theta_yz==0 implies that y==0 and z>0.
        theta_yz = np.arctan2(y_pos, z_pos)
        Ey = Eyz * np.sin(theta_yz)
        Ez = Eyz * np.cos(theta_yz)

        return np.stack((Ex, Ey, Ez), axis=0)
