# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
import numpy as np
from optical_dispersion_relations import drude_lorentz


class Builder(unittest.TestCase):

    def test_silver_parameters(self):
        """Test against "Rigorous modal analysis of Plasmonic Nanoresonators",
        Phys. Rev. B 97, 205422 (2018)
        DOI: https://doi.org/10.1103/PhysRevB.97.205422
        """
        # Given
        angular_frequency = np.array([4.18879020e+15, 3.42719199e+15,
                                      2.89993168e+15, 2.51327412e+15,
                                      2.21759481e+15, 1.98416378e+15])
        expected_permittivity = np.array([-9.38643376+0.07699091j, - 14.51511588+0.14056532j,
                                          - 20.66916708+0.232015j, - 27.84838702+0.35640458j,
                                          - 36.05254204+0.51879695j, - 45.28136515+0.72425291j])

        dispersion = drude_lorentz.DrudeLorentz().with_plasma_frequency(1.35e16).add_pole(
            damping_constant=0.0023*1.35e16).with_angular_frequency(angular_frequency)

        # When
        actual_permittivity = dispersion.permittivity()

        # Then
        self.assertTrue(np.allclose(
            expected_permittivity, actual_permittivity))

    def test_gold_parameters(self):
        """Test against "Rigorous modal analysis of Plasmonic Nanoresonators",
        Phys. Rev. B 97, 205422 (2018)
        DOI: https://doi.org/10.1103/PhysRevB.97.205422
        """
        # Given
        angular_frequency = np.array([4.18879020e+15, 3.42719199e+15,
                                      2.89993168e+15, 2.51327412e+15,
                                      2.21759481e+15, 1.98416378e+15])
        expected_permittivity = np.array([-1.42598986+4.18957409j, -6.03831464+1.60681497j,
                                          -12.31997339+1.1348564j, -19.3739092+1.13632031j,
                                          -27.29686535+1.32888338j, -36.13732434+1.65090681j])

        dispersion_builder = drude_lorentz.DrudeLorentz()

        dispersion_builder.with_dielectric_constant(6).with_plasma_frequency(1).add_pole(
            peak_strength=6*5.37e15**2,
            damping_constant=6.216e13,
            peak_position=0
        ).add_pole(
            peak_strength=6*2.263e15**2,
            damping_constant=1.332e15,
            peak_position=4.572e15
        ).with_angular_frequency(angular_frequency)

        # When
        actual_permittivity = dispersion_builder.permittivity()

        # Then
        self.assertTrue(np.allclose(
            expected_permittivity, actual_permittivity))


class SinglePole(unittest.TestCase):

    def test_large_frequency(self):
        """Test against section 1.2, Maier SA. Plasmonics: fundamentals and applications.
        ISBN: 978-0-387-37825-1
        """
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
            damping_constant=damping_rate,
            dielectric_constant=dielectric_constant,
        )

        # Then
        self.assertAlmostEqual(expected_permittivity, actual_permittivity)

    def test_plasma_frequency(self):
        """Test against section 1.2, Maier SA. Plasmonics: fundamentals and applications.
        ISBN: 978-0-387-37825-1
        """
        # Given
        angular_frequency = 1e2
        plasma_frequency = 5e2
        damping_rate = 1e-2

        expected_permittivity = 1 - plasma_frequency**2/angular_frequency**2

        # When
        actual_permittivity = drude_lorentz.single_pole(
            angular_frequency=angular_frequency,
            plasma_frequency=plasma_frequency,
            damping_constant=damping_rate
        )

        # Then
        self.assertAlmostEqual(expected_permittivity,
                               actual_permittivity, places=2)

    def test_silver_parameters(self):
        """Test against "Rigorous modal analysis of Plasmonic Nanoresonators",
        Phys. Rev. B 97, 205422 (2018)
        DOI: https://doi.org/10.1103/PhysRevB.97.205422
        """
        # Given
        silver_drude_parameters = {
            'plasma_frequency': 1.35e16,
            'damping_constant': 0.0023*1.35e16,
        }
        angular_frequency = np.array([4.18879020e+15, 3.42719199e+15,
                                      2.89993168e+15, 2.51327412e+15,
                                      2.21759481e+15, 1.98416378e+15])
        expected_permittivity = np.array([-9.38643376+0.07699091j, - 14.51511588+0.14056532j,
                                          - 20.66916708+0.232015j, - 27.84838702+0.35640458j,
                                          - 36.05254204+0.51879695j, - 45.28136515+0.72425291j])

        # When
        actual_permittivity = drude_lorentz.single_pole(angular_frequency,
                                                        **silver_drude_parameters)

        # Then
        self.assertTrue(np.allclose(
            expected_permittivity, actual_permittivity))


class DoublePole(unittest.TestCase):

    def test_gold_parameters(self):
        """Test against "Rigorous modal analysis of Plasmonic Nanoresonators",
        Phys. Rev. B 97, 205422 (2018)
        DOI: https://doi.org/10.1103/PhysRevB.97.205422
        """
        # Given
        gold_drude_parameters = {
            'dielectric_constant': 6,
            'plasma_frequency': 1,
            'first_pole': {
                'peak_strength': 5.37e15**2,
                'damping_constant': 6.216e13,
                'peak_position': 0,
            },
            'second_pole': {
                'peak_strength': 2.263e15**2,
                'damping_constant': 1.332e15,
                'peak_position': 4.572e15
            }
        }
        angular_frequency = np.array([4.18879020e+15, 3.42719199e+15,
                                      2.89993168e+15, 2.51327412e+15,
                                      2.21759481e+15, 1.98416378e+15])
        expected_permittivity = np.array([-1.42598986+4.18957409j, -6.03831464+1.60681497j,
                                          -12.31997339+1.1348564j, -19.3739092+1.13632031j,
                                          -27.29686535+1.32888338j, -36.13732434+1.65090681j])

        # When
        actual_permittivity = drude_lorentz.double_pole(angular_frequency,
                                                        **gold_drude_parameters)

        # Then
        self.assertTrue(np.allclose(
            expected_permittivity, actual_permittivity))
