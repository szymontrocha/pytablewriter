# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import typepy

from ._python import PythonCodeTableWriter


class NumpyTableWriter(PythonCodeTableWriter):
    """
    A table writer class for ``NumPy`` source code format.

        :Example:
            :ref:`example-numpy-table-writer`

    .. py:method:: write_table

        |write_table| with ``NumPy`` format.
        The tabular data are written as a variable definition of
        ``numpy.array``.

        :raises pytablewriter.EmptyTableNameError:
            If the |table_name| is empty.
        :raises pytablewriter.EmptyTableDataError:
            If the |headers| and the |value_matrix| is empty.
        :Example:
            :ref:`example-numpy-table-writer`

        .. note::
            Specific values in the tabular data are converted when writing:

            - |None|: written as ``None``
            - |inf|: written as ``numpy.inf``
            - |nan|: written as ``numpy.nan``
            - |datetime| instances determined by |is_datetime_instance_formatting| attribute:
                - |True|: written as `dateutil.parser <https://dateutil.readthedocs.io/en/stable/parser.html>`__
                - |False|: written as |str|

            .. seealso::
                :ref:`example-type-hint-python`
    """

    FORMAT_NAME = "numpy"

    @property
    def format_name(self):
        return self.FORMAT_NAME

    def __init__(self):
        super(NumpyTableWriter, self).__init__()

        self.import_numpy_as = "np"
        self._dp_extractor.type_value_map[typepy.Typecode.INFINITY] = "{:s}.inf".format(
            self.import_numpy_as
        )
        self._dp_extractor.type_value_map[typepy.Typecode.NAN] = "{:s}.nan".format(
            self.import_numpy_as
        )

    def _get_opening_row_items(self):
        array_def = "{:s}.array([".format(self.import_numpy_as)

        if typepy.is_not_null_string(self.table_name):
            return ["{} = {}".format(self.variable_name, array_def)]

        return [array_def]

    def _get_closing_row_items(self):
        return ["])"]
