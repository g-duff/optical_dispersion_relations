# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
import numpy as np
from src.optical_dispersion_relations import dielectric_waveguides


class TranscendentialSlabWaveguide(unittest.TestCase):
    '''Benchmarks from Online Mode Solver: 1-D mode solver for dielectric multilayer slab waveguides
    https://www.siio.eu/oms.html
    '''

    def test_TE_constants_benchmark(self):
        # pylint: disable = invalid-name

        # Given
        free_space_wavelength = 1.550
        waveguide_effective_refractive_index = 1.876691009

        free_space_wavenumber = 2*np.pi/free_space_wavelength
        waveguide_propagation_constant = free_space_wavenumber * \
            waveguide_effective_refractive_index

        waveguide_thickness = 0.5
        cover_refractive_index = 1.0
        guiding_layer_refractive_index = 2.1
        substrate_refractive_index = 1.5

        # When
        residual = dielectric_waveguides.transcendential_slab_waveguide_TE(
            waveguide_propagation_constant,
            free_space_wavenumber,
            waveguide_thickness,
            cover_refractive_index,
            guiding_layer_refractive_index,
            substrate_refractive_index,
        )

        # Then
        self.assertAlmostEqual(residual, 0)

    def test_TM_constants_benchmark(self):
        # pylint: disable = invalid-name

        # Given
        free_space_wavelength = 1.550
        waveguide_effective_refractive_index = 1.744774075

        free_space_wavenumber = 2*np.pi/free_space_wavelength
        waveguide_propagation_constant = free_space_wavenumber * \
            waveguide_effective_refractive_index

        waveguide_thickness = 0.5
        cover_refractive_index = 1.0
        guiding_layer_refractive_index = 2.1
        substrate_refractive_index = 1.5

        # When
        residual = dielectric_waveguides.transcendential_slab_waveguide_TM(
            waveguide_propagation_constant,
            free_space_wavenumber,
            waveguide_thickness,
            cover_refractive_index,
            guiding_layer_refractive_index,
            substrate_refractive_index,
        )

        # Then
        self.assertAlmostEqual(residual, 0)
