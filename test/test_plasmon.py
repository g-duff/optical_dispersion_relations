# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
import numpy as np
from src.dispersion_relations import plasmon


class SurfacePlasmonPolariton(unittest.TestCase):

    def test_constants_from_textbook(self):
        '''Test against fig 2.3 in Maier SA. Plasmonics: fundamentals and applications.
        ISBN: 978-0-387-37825-1'''
        # Given
        dielectric_permittivity = 1
        metal_permittivity = np.array([-99. + 0.j,
                                       -24. + 0.j,
                                       -10.11111111 + 0.j,
                                       -5.25 + 0.j,
                                       -3. + 0.j,
                                       -1.77777778 + 0.j,
                                       -1.04081633 + 0.j,
                                       -0.5625 + 0.j,
                                       -0.2345679 + 0.j,
                                       0. + 0.j,
                                       0.17355372 + 0.j])

        expected_refractive_index = np.array([1.00508909-0.j,
                                              1.02150784-0.j,
                                              1.05344962-0.j,
                                              1.11143786-0.j,
                                              1.22474487-0.j,
                                              1.51185789-0.j,
                                              5.04975247-0.j,
                                              0. + 1.13389342j,
                                              0. + 0.55358072j,
                                              0. + 0.j,
                                              0.38456121+0.j])

        # When
        actual_refractive_index = plasmon.surface_plasmon_polariton(
            dielectric_permittivity=dielectric_permittivity, metal_permittivity=metal_permittivity)

        # Then
        self.assertTrue(np.allclose(
            expected_refractive_index, actual_refractive_index))


class MetalInsulatorMetalCollinApproximation(unittest.TestCase):

    def test_thick_insulator(self):
        # Given
        dielectric_permittivity = 1
        metal_permittivity = -50
        insulator_thickness = 10
        wavelength = 1

        expected_effective_refractive_index = 1

        # When
        actual_effective_refractive_index = plasmon.metal_insulator_metal_collin_approximation(
            dielectric_permittivity=dielectric_permittivity,
            metal_permittivity=metal_permittivity,
            wavelength=wavelength,
            insulator_thickness=insulator_thickness,
        )

        # Then
        self.assertAlmostEqual(expected_effective_refractive_index,
                               actual_effective_refractive_index,
                               places=2)

    def test_thin_insulator(self):
        # Given
        dielectric_permittivity = 1
        metal_permittivity = -50
        insulator_thickness = 0.01
        wavelength = 1

        expected_effective_refractive_index = 2.355

        # When
        actual_effective_refractive_index = plasmon.metal_insulator_metal_collin_approximation(
            dielectric_permittivity=dielectric_permittivity,
            metal_permittivity=metal_permittivity,
            wavelength=wavelength,
            insulator_thickness=insulator_thickness,
        )

        # Then
        self.assertAlmostEqual(expected_effective_refractive_index,
                               actual_effective_refractive_index,
                               places=3)
