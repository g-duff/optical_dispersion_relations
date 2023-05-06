#  pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
import numpy as np
from optical_dispersion_relations import plasmon


class SurfacePlasmonPolariton(unittest.TestCase):

    def test_constants_from_textbook(self):
        """Test against fig 2.3 in Maier SA. Plasmonics: fundamentals and applications.
        ISBN: 978-0-387-37825-1
        """
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
    """Test against fig 2 in Waveguiding in nanoscale metallic apertures.
    https://doi.org/10.1364/OE.15.004310
    """

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


class MetalInsulatorMetalSondergaardNarrowApproximation(unittest.TestCase):
    """Test against fig 4 in
    General properties of slow-plasmon resonant nanostructures: nano-antennas and resonators.
    https://doi.org/10.1364/OE.15.010869
    """

    def test_insulator_constants(self):
        # Given
        dielectric_permittivity = 1
        metal_permittivity = -23.6+1.69j
        wavelength = 775
        insulator_thickness = np.array([100, 200, 300, 400, 500])

        expected_effective_refractive_index = np.array([1.23403843+0.00811681j,
                                                        1.12252228+0.00437417j,
                                                        1.08308215+0.00300229j,
                                                        1.062867+0.00228691j,
                                                        1.05056857+0.00184725j])

        # When
        actual_effective_refractive_index = \
            plasmon.metal_insulator_metal_sondergaard_narrow_approximation(
                dielectric_permittivity=dielectric_permittivity,
                metal_permittivity=metal_permittivity,
                wavelength=wavelength,
                insulator_thickness=insulator_thickness,
            )

        # Then
        self.assertTrue(np.allclose(
            expected_effective_refractive_index, actual_effective_refractive_index))

    def test_thick_insulator(self):
        # Given
        dielectric_permittivity = 1
        metal_permittivity = -50
        insulator_thickness = 10
        wavelength = 1

        expected_effective_refractive_index = 1

        # When
        actual_effective_refractive_index = \
            plasmon.metal_insulator_metal_sondergaard_narrow_approximation(
                dielectric_permittivity=dielectric_permittivity,
                metal_permittivity=metal_permittivity,
                wavelength=wavelength,
                insulator_thickness=insulator_thickness,
            )

        # Then
        self.assertAlmostEqual(expected_effective_refractive_index,
                               actual_effective_refractive_index,
                               places=2)
