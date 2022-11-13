# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
from src.dispersion_relations import utilities


class Utilities(unittest.TestCase):

    def test_refractive_index_to_permittivity(self):
        # Given
        refractive_index = 2.0+0.5j
        expected_permittivity_real = 3.75
        expected_permittivity_imaginary = 2.0

        # When
        actual_permittivity = utilities.refractive_index_to_permittivity(
            refractive_index)

        # Then
        self.assertAlmostEqual(expected_permittivity_real,
                               actual_permittivity.real)
        self.assertAlmostEqual(
            expected_permittivity_imaginary, actual_permittivity.imag)
