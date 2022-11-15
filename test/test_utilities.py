# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
from src.dispersion_relations import utilities


class Utilities(unittest.TestCase):

    def test_permittivity_to_extinction_coefficient(self):
        # Given
        complex_permittivity = 3.75 + 2.0j
        expected_extinction_coefficient = 0.5

        # When
        actual_extinction_coefficient = utilities.permittivity_to_extinction_coefficient(
            complex_permittivity)

        # Then
        self.assertAlmostEqual(
            expected_extinction_coefficient, actual_extinction_coefficient)

    def test_permittivity_to_refractive_index(self):
        # Given
        complex_permittivity = 3.75 + 2.0j
        expected_refractive_index = 2.0
        expected_extinction_coefficient = 0.5

        # When
        actual_refractive_index = utilities.permittivity_to_refractive_index(
            complex_permittivity)

        # Then
        self.assertAlmostEqual(expected_refractive_index,
                               actual_refractive_index.real)
        self.assertAlmostEqual(
            expected_extinction_coefficient, actual_refractive_index.imag)

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