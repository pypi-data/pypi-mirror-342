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

import abc
import os
import re

from anna import Bool, Filepath, parametrize
from anna.utils import use_docs_from
import numpy as np
import pandas
from scipy.interpolate import RegularGridInterpolator

from virtual_ipm.components import Model
from virtual_ipm.simulation.errors import ConfigurationError, InvalidExternalInputError


class GuidingFieldModel(Model):
    """
    (Abstract) Base class for guiding field models.
    """

    def __init__(self, configuration=None):
        super().__init__(configuration)

    @abc.abstractmethod
    def eval(self, position_four_vectors, progress):
        """
        Request the guiding field vectors at the specified positions and at the
        specified simulation progress.

        Parameters
        ----------
        position_four_vectors : :class:`~np.ndarray`, shape (4, N)
        progress : :class:`Progress`

        Returns
        -------
        field_vectors : :class:`~np.ndarray`, shape (3, N)

        See Also
        --------
        :method:`EMFieldsCollector.electric_field_at` : For arguments and return values.
        """
        raise NotImplementedError


class UniformGuidingField(GuidingFieldModel):
    """Mix-in class for a constant, uniform guiding field."""

    _field_vector = None

    def __init__(self, configuration):
        super().__init__(configuration)
        if self._field_vector is None:
            raise RuntimeError(
                '%s must define a `_field_vector` attribute'
                % self.__class__.__name__
            )

    def as_json(self):
        return dict(
            super().as_json(),
            field_vector=self._field_vector.tolist()
        )

    @use_docs_from(GuidingFieldModel)
    def eval(self, position_four_vector, progress):
        return self._field_vector[:, np.newaxis]


@parametrize(
    Filepath('Filename'),
)
class CSVAdaptor(GuidingFieldModel):
    """
    Base class for 2D and 3D CSV Adaptors.
    """

    @classmethod
    def _validate_columns(cls, df):
        columns_with_units = []
        for col in df.columns:
            columns_with_units.append(cls._match_column(col))
        cls.log.debug('Columns: %s', df.columns)
        cls.log.debug('Columns with units: %s', columns_with_units)

    @classmethod
    def _validate_cycling(cls, df):
        xs_unique, xs_indices = np.unique(df.iloc[:, 0].values, return_index=True)
        ys_unique, ys_indices = np.unique(df.iloc[:, 1].values, return_index=True)
        zs_unique, zs_indices = np.unique(df.iloc[:, 2].values, return_index=True)
        x_valid = np.all(xs_indices[1:] - xs_indices[:-1] == ys_unique.size * zs_unique.size)
        y_valid = np.all(ys_indices[1:] - ys_indices[:-1] == zs_unique.size)
        z_valid = np.all(zs_indices == np.arange(zs_unique.size))
        if not (x_valid and y_valid and z_valid):
            raise InvalidExternalInputError(
                'Positions must cycle in the order z, y, x (i.e., z cycles first).\n'
                'Similar to:\n'
                'for x in xs:\n'
                '  for y in ys:\n'
                '    for z in zs:\n'
                '      add_line_to_csv(x,y,z,...)'
            ) from None

    @classmethod
    def _get_unique_positions_by_index(cls, df, index):
        # pos = df[df.columns[index]].unique()
        pos = df.iloc[:, index].unique()
        if cls._match_column(df.columns[index])[-1] == 'mm':
            pos *= 1.0e-3
        return pos

    @classmethod
    def _match_column(cls, col):
        match = re.match(r'^([a-zA-Z]+) \[([a-zA-Z0-9/*]+)\]$', col)
        if match is None:
            raise InvalidExternalInputError(
                '"%s" is not a valid column name. Columns must have the format '
                '<id> [<unit>]'
                % col
            ) from None
        if match.groups()[-1] not in ('m', 'mm', 'V/m', 'T'):
            raise InvalidExternalInputError(
                "Unit must be one of {'m', 'mm', 'V/m', 'T'} (got '%s' instead)"
                % match.groups()[-1]
            ) from None
        return match.groups()

    def _verify_that_all_positions_are_inside_grid(self, position):
        outside = (
              (position[0] < self._x_min)
            | (position[0] > self._x_max)
            | (position[1] < self._y_min)
            | (position[1] > self._y_max)
            | (position[2] < self._z_min)
            | (position[2] > self._z_max)
        )
        if np.any(outside):
            raise ValueError(
                f'During evaluation of the {type(self).__name__} guiding field, a particle has been encountered '
                f'whose position (x,y,z) = {position[:, outside][:, 0].tolist()} lies outside of the xyz-grid that '
                f'is specified by the underlying CSV file. '
                f'The specified grid spans the following cubic region:\n'
                f'X [{self._x_min}, {self._x_max}]\n'
                f'Y [{self._y_min}, {self._y_max}]\n'
                f'Z [{self._z_min}, {self._z_max}]'
            )

    @abc.abstractmethod
    def eval(self, position_four_vectors, progress):
        raise NotImplementedError


@parametrize(
    Bool(
        'UseColumnNames',
        default=False,
        info=(
            'If this parameter is activated, the columns of the CSV file will be '
            'interpreted by their names rather than by their positions. For more '
            'information see the documentation of this model.'
        ),
    ),
)
class CSVAdaptor2D(CSVAdaptor):
    """
    Adaptor for an external CSV file which contains the values of the guiding field (either
    electric of magnetic) in two dimensions ``x`` and ``y``.

    The CSV file must have at least five columns where the first three refer to the ``x``, ``y``, and
    ``z`` coordinates (in that order). The next two columns must provide the field values for ``x``-
    and ``y``-direction (in that order). Additional columns may follow and are ignored. The file
    must not contain an index column. It shall provide a header line which denotes the column names
    in the following format::

        ``<name> [<unit>]``

    The names can be arbitrarily chosen (however the above mentioned order of columns must be
    respected; only lower- and uppercase letters are allowed), the unit must be one of
    ``{'m', 'mm'}`` for positions and ``'V/m'`` for electric field values or ``'T'`` for magnetic
    field values. The positions need to cycle first through ``z`` then ``y`` then ``x``.

    For example, consider the three values ``[1,2,3]`` for each dimension ``x``, ``y``, and ``z``.
    Then the columns need to be like (for an electric field map; a magnetic field map would indicate ``[T]`` as unit)::

        x [mm], y [mm], z [mm], Ex [V/m], Ey [V/m]
        1     , 1     , 1     , ...     , ...     
        1     , 1     , 2     , ...     , ...     
        1     , 1     , 3
        1     , 2     , 1
        1     , 2     , 2
        1     , 2     , 3
        1     , 3     , 1
        1     , 3     , 2
        1     , 3     , 3
        2     , 1     , 1
        2     , 1     , 2
        2     , 1     , 3
        ... and so on ...

    That is, ``z`` cycles first through the three values ``[1,2,3]``, then cycles ``y``, and finally ``x``.
    The columns ``Ex``, ``Ey`` are just the electric field values for the given position at ``(x,y,z)`` in each row.

    Using field dimensions other than ``x`` and ``y``
    -------------------------------------------------

    It is possible to use field dimensions that are different from the ``x,y`` combination by setting the
    advanced parameter `UseColumnNames` to true (it's false by default). When this parameter is activated,
    the columns of the CSV file will be interpreted by their names rather than by their position (as has
    been described above). In that case, the columns may appear in an arbitrary order and for the field
    values also ``Ez [V/m]`` (or, ``Bz [T]``) may be used. Any 2-tuple of field dimensions is allowed in
    this case: ``(Ex,Ey)`` or ``(Ex,Ez)`` or ``(Ey,Ez)`` (and similar for the B-field).
    """

    def __init__(self, configuration):
        super().__init__(configuration)
        if not os.path.isfile(self._filename):
            raise ConfigurationError('%s does not point to a valid file' % self._filename) from None
        if os.path.splitext(self._filename)[-1] != '.csv':
            self.log.warning(
                '%s does not have ending ".csv" however this class can only process csv files. '
                'Are you sure this is the right file?'
                % self._filename
            )

    def prepare(self):
        df = pandas.read_csv(self._filename, dtype=float, index_col=None)
        self.log.debug('Data frame:\n%s', df.head())
        self._validate_columns(df)
        self._validate_cycling(df)

        self.log.debug('Using column names: %s', self._use_column_names)
        if self._use_column_names:
            pos_col_idx = {}
            field_col_idx = {}
            field_vector_idx = []
            _keys = iter(['1st', '2nd'])
            for idx, col in enumerate(df.columns):
                name = col.split(' ', maxsplit=1)[0]
                if name in ('x', 'y', 'z'):
                    pos_col_idx[name] = idx
                elif name in ('Ex', 'Bx'):
                    field_col_idx[next(_keys)] = idx
                    field_vector_idx.append(0)
                elif name in ('Ey', 'By'):
                    field_col_idx[next(_keys)] = idx
                    field_vector_idx.append(1)
                elif name in ('Ez', 'Bz'):
                    field_col_idx[next(_keys)] = idx
                    field_vector_idx.append(2)
                else:
                    raise InvalidExternalInputError(
                        f'Invalid column name: {col}'
                    ) from None
            if field_col_idx.keys() != {'1st', '2nd'}:
                raise InvalidExternalInputError(
                        f'Exactly two field value columns must be given'
                    ) from None
            _missing = {0, 1, 2} - set(field_vector_idx)
            assert len(_missing) == 1
            field_vector_idx.append(next(iter(_missing)))
        else:
            pos_col_idx = dict(x=0, y=1, z=2)
            field_col_idx = {'1st': 3, '2nd': 4}
            field_vector_idx = [0, 1, 2]  # x- and y-component

        self.log.debug(
            'pos_col_idx: %s, field_col_idx: %s, field_vector_idx: %s',
            pos_col_idx, field_col_idx, field_vector_idx,
        )

        self._field_vector_idx = field_vector_idx

        xs = self._get_unique_positions_by_index(df, pos_col_idx['x'])
        ys = self._get_unique_positions_by_index(df, pos_col_idx['y'])
        zs = self._get_unique_positions_by_index(df, pos_col_idx['z'])

        # We call it in the following Ex, Ey however this is similarly valid for magnetic field
        # values.
        E1 = df[df.columns[field_col_idx['1st']]].values.reshape((len(xs), len(ys), len(zs)))
        E2 = df[df.columns[field_col_idx['2nd']]].values.reshape((len(xs), len(ys), len(zs)))

        # Default method is 'linear' (piecewise linear interpolation), another option is 'nearest'
        # (nearest neighbour interpolation).
        # Default behaviour is to raise a ValueError for values outside of bounds but we will cover
        # this check manually in `eval`; optionally one can choose a value to be used outside of
        # the boundaries.
        self._E1_interpolator = RegularGridInterpolator((xs, ys, zs), E1)
        self._E2_interpolator = RegularGridInterpolator((xs, ys, zs), E2)

        self._x_min = np.min(xs)
        self._x_max = np.max(xs)
        self._y_min = np.min(ys)
        self._y_max = np.max(ys)
        self._z_min = np.min(zs)
        self._z_max = np.max(zs)

        self.log.debug(
            'Grid: x{%e, %e}, y{%e, %e}, z{%e, %e}'
            % (self._x_min, self._x_max, self._y_min, self._y_max, self._z_min, self._z_max)
        )

    def eval(self, position_four_vectors, progress):
        # Different possibilities how to deal with positions outside of the grid are possible:
        #   1. Add additional grid points at chamber boundaries. Question is which field values?
        #      This has to do with boundary conditions of field calculation and actually the field
        #      should cover the whole regime! But positions out of the grid could also happen due
        #      to numerical issues (distance would be very small) and in case the field is not zero
        #      at the boundaries this would introduce a large bias.
        #      ( -> This solution assumes zero field strength outside of the grid.)
        #   2. Consider position outside of the grid to be at the nearest grid point (i.e.
        #      virtually move them on the grid for the request). For small margins this is an
        #      appropriate solution. (np.min, np.max for grid positions.)
        #      ( -> This solution does not allow positions outside of the grid.)
        #   3. Measure distance to nearest grid point, also when positions are out of the grid.
        #      Instead of two neighbouring grid points positions outside of the grid would use
        #      the same grid point twice for interpolation. Appropriate rescaling with respect
        #      to distance would lead to the field value of that grid point.
        #      ( -> This solution assumes the field to be constant outside of the grid and the
        #           field strength equals to the nearest boundary point for the respective
        #           dimension.
        position = position_four_vectors[1:]
        self._verify_that_all_positions_are_inside_grid(position)
        transposed_positions = np.transpose(position)
        E1 = self._E1_interpolator(transposed_positions)
        E2 = self._E2_interpolator(transposed_positions)
        E3 = np.zeros(len(transposed_positions), dtype=float)
        E_field = np.empty(shape=(3, len(E1)), dtype=float)
        E_field[self._field_vector_idx, :] = np.stack((E1, E2, E3))
        return E_field


# noinspection PyPep8Naming,PyAttributeOutsideInit
class CSVAdaptor3D(CSVAdaptor):
    """
    Adaptor for an external CSV file which contains the values of the guiding field (either
    electric of magnetic) in three dimensions ``x``, ``y``, and ``z``.
    
    The CSV file must have at least six columns where the first three refer to the ``x``, ``y``, and ``z``
    coordinates (in that order). The next three columns must provide the field values for ``x``-,
    ``y``-, and ``z``-direction (in that order). Additional columns may follow and are ignored. The file
    must not contain an index column. It shall provide a header line which denotes the column names
    in the following format::
    
        ``<name> [<unit>]``
        
    The name can be arbitrarily chosen (however the above mentioned order of columns must be
    respected; only lower- and uppercase letters are allowed), the unit must be one of
    ``{'m', 'mm'}`` for positions and ``'V/m'`` for electric field values or ``'T'`` for magnetic
    field values. The positions need to cycle first through ``z`` then ``y`` then ``x``.

    For example, consider the three values ``[1,2,3]`` for each dimension ``x``, ``y``, and ``z``.
    Then the columns need to be like (for an electric field map; a magnetic field map would indicate ``[T]`` as unit)::

        x [mm], y [mm], z [mm], Ex [V/m], Ey [V/m], Ez [V/m]
        1     , 1     , 1     , ...     , ...     , ...
        1     , 1     , 2     , ...     , ...     , ...
        1     , 1     , 3
        1     , 2     , 1
        1     , 2     , 2
        1     , 2     , 3
        1     , 3     , 1
        1     , 3     , 2
        1     , 3     , 3
        2     , 1     , 1
        2     , 1     , 2
        2     , 1     , 3
        ... and so on ...

    That is, ``z`` cycles first through the three values ``[1,2,3]``, then cycles ``y``, and finally ``x``.
    The columns ``Ex``, ``Ey``, ``Ez`` are just the electric field values for the given position at ``(x,y,z)`` in each row.
    """

    def __init__(self, configuration):
        super().__init__(configuration)
        if not os.path.isfile(self._filename):
            raise ConfigurationError('%s does not point to a valid file' % self._filename) from None
        if os.path.splitext(self._filename)[-1] != '.csv':
            self.log.warning(
                '%s does not have ending ".csv" however this class can only process csv files. '
                'Are you sure this is the right file?'
                % self._filename
            )

    def prepare(self):
        df = pandas.read_csv(self._filename, dtype=float, index_col=None)
        self.log.debug('Data frame:\n%s', df.head())
        self._validate_columns(df)
        self._validate_cycling(df)

        xs = self._get_unique_positions_by_index(df, 0)
        ys = self._get_unique_positions_by_index(df, 1)
        zs = self._get_unique_positions_by_index(df, 2)

        # We call it in the following Ex, Ey, Ez however this is similarly valid for magnetic
        # field values.
        Ex = df[df.columns[3]].values.reshape((len(xs), len(ys), len(zs)))
        Ey = df[df.columns[4]].values.reshape((len(xs), len(ys), len(zs)))
        Ez = df[df.columns[5]].values.reshape((len(xs), len(ys), len(zs)))

        # Default method is 'linear' (piecewise linear interpolation), another option is 'nearest'
        # (nearest neighbour interpolation).
        # Default behaviour is to raise a ValueError of values outside of bounds but we will cover
        # this check manually in `eval`; optionally one can choose a value to be used outside of
        # the boundaries.
        self._Ex_interpolator = RegularGridInterpolator((xs, ys, zs), Ex)
        self._Ey_interpolator = RegularGridInterpolator((xs, ys, zs), Ey)
        self._Ez_interpolator = RegularGridInterpolator((xs, ys, zs), Ez)

        self._x_min = np.min(xs)
        self._x_max = np.max(xs)
        self._y_min = np.min(ys)
        self._y_max = np.max(ys)
        self._z_min = np.min(zs)
        self._z_max = np.max(zs)

        self.log.debug(
            'Grid: x{%e, %e}, y{%e, %e}, z{%e, %e}'
            % (self._x_min, self._x_max, self._y_min, self._y_max, self._z_min, self._z_max)
        )

    def eval(self, position_four_vectors, progress):
        # Different possibilities how to deal with positions outside of the grid are possible:
        #   1. Add additional grid points at chamber boundaries. Question is which field values?
        #      This has to do with boundary conditions of field calculation and actually the field
        #      should cover the whole regime! But positions out of the grid could also happen due
        #      to numerical issues (distance would be very small) and in case the field is not zero
        #      at the boundaries this would introduce a large bias.
        #      ( -> This solution assumes zero field strength outside of the grid.)
        #   2. Consider position outside of the grid to be at the nearest grid point (i.e.
        #      virtually move them on the grid for the request). For small margins this is an
        #      appropriate solution. (np.min, np.max for grid positions.)
        #      ( -> This solution does not allow positions outside of the grid.)
        #   3. Measure distance to nearest grid point, also when positions are out of the grid.
        #      Instead of two neighbouring grid points positions outside of the grid would use
        #      the same grid point twice for interpolation. Appropriate rescaling with respect
        #      to distance would lead to the field value of that grid point.
        #      ( -> This solution assumes the field to be constant outside of the grid and the
        #           field strength equals to the nearest boundary point for the respective
        #           dimension.
        position = position_four_vectors[1:]
        self._verify_that_all_positions_are_inside_grid(position)
        transposed_positions = np.transpose(position)
        Ex = self._Ex_interpolator(transposed_positions)
        Ey = self._Ey_interpolator(transposed_positions)
        Ez = self._Ez_interpolator(transposed_positions)
        return np.stack((Ex, Ey, Ez))
