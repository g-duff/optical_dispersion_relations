# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
import numpy as np
from src.dispersion_relations import drude_lorentz


class SinglePole(unittest.TestCase):

    def test_large_frequency(self):
        # Given
        dielectric_constant = 2
        angular_frequency = 1e2
        plasma_frequency = 1e-2
        damping_rate = 1e-2

        expected_permittivity = dielectric_constant

        # When
        actual_permittivity = drude_lorentz.single_pole(
            angular_frequency=angular_frequency,
            plasma_frequency=plasma_frequency,
            damping_rate=damping_rate,
            dielectric_constant=dielectric_constant,
        )

        # Then
        self.assertAlmostEqual(expected_permittivity, actual_permittivity)

    def test_plasma_frequency(self):
        # Given
        angular_frequency = 1e2
        plasma_frequency = 5e2
        damping_rate = 1e-2

        expected_permittivity = 1 - plasma_frequency**2/angular_frequency**2

        # When
        actual_permittivity = drude_lorentz.single_pole(
            angular_frequency=angular_frequency,
            plasma_frequency=plasma_frequency,
            damping_rate=damping_rate
        )

        # Then
        self.assertAlmostEqual(expected_permittivity,
                               actual_permittivity, places=2)
