"""Plasmonics Dispersion Relations"""

import numpy as np


def surface_plasmon_polariton(dielectric_permittivity: float,
                              metal_permittivity: complex) -> complex:
    """Exact surface plasmon dispersion relation for TM polarization.
    Surface plasmons only exist for TM polarization.

    Parameters
    ----------
    dielectric_permittivity: float, complex number or numpy array
    metal_permittivity: float, complex number or numpy array

    Returns
    -------
    effective_refractive_index of surface plasmon polariton: complex number or numpy array

    Derivation
    ----------
    Maier SA. Plasmonics: Fundamentals and Applications.
    ISBN: 978-0-387-37825-1
    """
    numerator = dielectric_permittivity*metal_permittivity
    denominator = dielectric_permittivity+metal_permittivity
    effective_refractive_index = np.sqrt(numerator/denominator)
    return effective_refractive_index


def metal_insulator_metal_collin_approximation(dielectric_permittivity: float,
                                               metal_permittivity: complex,
                                               wavelength: float,
                                               insulator_thickness: float) -> complex:
    """Approximate metal-insulator-metal waveguide dispersion relation for TM polarization.

    Parameters
    ----------
    dielectric_permittivity: float or complex
    metal_permittivity: float or complex
    wavelength, in any unit of distance: float
    insulator_thickness, in the same unit of distance as wavelength: float

    Returns
    -------
    effective_refractive_index of the light propagating in the waveguide: complex

    Derivation
    ----------
    Waveguiding in nanoscale metallic apertures.
    https://doi.org/10.1364/OE.15.004310
    """
    surface_plasmon_coupling_term = wavelength * \
        np.sqrt(1-dielectric_permittivity/metal_permittivity) / \
        (np.pi*insulator_thickness*np.sqrt(-1*metal_permittivity))
    effective_refractive_index = np.sqrt(dielectric_permittivity) * \
        np.sqrt(1 + surface_plasmon_coupling_term)
    return effective_refractive_index


def metal_insulator_metal_sondergaard_narrow_approximation(dielectric_permittivity: float,
                                                           metal_permittivity: complex,
                                                           wavelength: float,
                                                           insulator_thickness: float) -> complex:
    """Approximate metal-insulator-metal waveguide dispersion relation for TM polarization.

    Parameters
    ----------
    dielectric_permittivity: float or complex
    metal_permittivity: float or complex
    wavelength: float, in any unit of distance
    insulator_thickness: float, in the same unit of distance as wavelength

    Returns
    -------
    effective_refractive_index of the light propagating in the wavevuide: complex

    Derivation
    ----------
    General properties of slow-plasmon resonant nanostructures: nano-antennas and resonators.
    https://doi.org/10.1364/OE.15.010869"""
    freespace_wavenumber = 2 * np.pi / wavelength

    narrow_gap_limit_propagation_constant = -2 * dielectric_permittivity \
        / (insulator_thickness * metal_permittivity)

    narrow_gap_limit_effective_refractive_index = narrow_gap_limit_propagation_constant \
        / freespace_wavenumber

    narrow_gap_limit_effective_permittivity = narrow_gap_limit_effective_refractive_index**2

    effective_permittivity = dielectric_permittivity \
        + 0.5 * narrow_gap_limit_effective_permittivity \
        + np.sqrt(
            narrow_gap_limit_effective_permittivity * (
                dielectric_permittivity
                - metal_permittivity
                + 0.25 * narrow_gap_limit_effective_permittivity
            )
        )
    effective_refractive_index = np.sqrt(effective_permittivity)
    return effective_refractive_index
