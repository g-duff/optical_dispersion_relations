'''Plasmonics Dispersion Relations'''
import numpy as np


def surface_plasmon_polariton(dielectric_permittivity, metal_permittivity):
    '''Exact surface plasmon dispersion relation for TM polarization.
    Surface plasmons only exist for TM polarization.

    Parameters:
        dielectric_permittivity: float, complex number or numpy array
        metal_permittivity: float, complex number or numpy array

    Returns:
        effective_refractive_index of surface plasmon polariton: complex number or numpy array

    Derivation in:
    Maier SA. Plasmonics: fundamentals and applications.
    ISBN: 978-0-387-37825-1
    '''
    numerator = dielectric_permittivity*metal_permittivity
    denominator = dielectric_permittivity+metal_permittivity
    effective_refractive_index = np.sqrt(numerator/denominator)
    return effective_refractive_index


def metal_insulator_metal_collin_approximation(dielectric_permittivity: float,
                                               metal_permittivity: complex,
                                               wavelength: float,
                                               insulator_thickness: float) -> complex:
    '''Approximate metal-insulator-metal waveguide dispersion relation for TM polarization.

    Parameters:
        dielectric_permittivity: float or complex
        metal_permittivity: float or complex
        wavelength, in any unit of distance: float
        insulator_thickness, in the same unit of distance as wavelength: float

    Returns:
        effective_refractive_index of the light propagating in the wavevuide: complex
    '''
    surface_plasmon_coupling_term = wavelength * \
        np.sqrt(1-dielectric_permittivity/metal_permittivity) / \
        (np.pi*insulator_thickness*np.sqrt(-1*metal_permittivity))
    effective_refractive_index = np.sqrt(dielectric_permittivity) * \
        np.sqrt(1 + surface_plasmon_coupling_term)
    return effective_refractive_index
