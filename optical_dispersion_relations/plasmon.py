"""Plasmonics Dispersion Relations"""

import numpy as np
from numpy.lib import scimath

from optical_dispersion_relations import utilities


def surface_plasmon_polariton(
    dielectric_permittivity: float,
    metal_permittivity: complex
) -> complex:
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
    Maier SA. Plasmonics: Fundamentals and Applications, Chapter 2.2
    ISBN: 978-0-387-37825-1
    """
    numerator = dielectric_permittivity*metal_permittivity
    denominator = dielectric_permittivity+metal_permittivity
    effective_refractive_index = np.sqrt(numerator/denominator)
    return effective_refractive_index


def metal_dielectric_metal_collin_approximation(
    wavelength: float,
    thickness: float,
    dielectric_permittivity: float,
    metal_permittivity: complex,
) -> complex:
    """Approximate dispersion relation for a finite-thickness dielectric slab
    between two semi-infinite metal half-spaces. TM polarization.

    Parameters
    ----------
    wavelength, in any unit of distance: float
    thickness, in the same unit of distance as wavelength: float
    dielectric_permittivity: float or complex
    metal_permittivity: float or complex

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
        (np.pi*thickness*np.sqrt(-1*metal_permittivity))
    effective_refractive_index = np.sqrt(dielectric_permittivity) * \
        np.sqrt(1 + surface_plasmon_coupling_term)
    return effective_refractive_index


def metal_dielectric_metal_sondergaard_narrow_approximation(
    wavelength: float,
    thickness: float,
    dielectric_permittivity: float,
    metal_permittivity: complex,
) -> complex:
    """Approximate dispersion relation for a finite-thickness dielectric slab
    between two semi-infinite metal half-spaces. TM polarization.

    Parameters
    ----------
    wavelength: float, in any unit of distance
    thickness: float, of the insulatr layer in the same unit of distance as wavelength
    dielectric_permittivity: float or complex
    metal_permittivity: float or complex

    Returns
    -------
    effective_refractive_index of the light propagating in the wavevuide: complex

    Derivation
    ----------
    General properties of slow-plasmon resonant nanostructures: nano-antennas and resonators.
    https://doi.org/10.1364/OE.15.010869
    """
    freespace_wavenumber = utilities.wavelength_to_wavenumber(wavelength)

    narrow_gap_limit_propagation_constant = -2 * dielectric_permittivity \
        / (thickness * metal_permittivity)

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


def transcendential_trilayer_even_magnetic_field(
    propagation_constant: complex,
    wavelength: float,
    thickness: float,
    middle_layer_permittivity: 'float | complex',
    outer_layers_permittivity: 'float | complex',
) -> complex:
    """Describes a metal-dielectric-metal or dielectric-metal-dielectric symmetrical stack,
    odd vector parity modes / the magnetic field is an even function.

    Parameters
    ----------
    propagation_constant: float, unkown - vary to find the system solutions
    wavelength: float, at which the light propagates in free space
    thickness: float, of the middle layer
    middle_layer_permittivity: float or complex
    outer_layers_permittivity: float or complex

    Returns
    -------
    residual to be minimized: float

    Derivation
    ----------
    Maier SA. Plasmonics: Fundamentals and Applications, Chapter 2.3
    ISBN: 978-0-387-37825-1
    """
    freespace_wavenumber = utilities.wavelength_to_wavenumber(wavelength)

    middle_layer_wavevector_perpendicular_component = scimath.sqrt(
        propagation_constant**2 - middle_layer_permittivity*freespace_wavenumber**2
    )
    outer_layers_wavevector_perpendicular_component = scimath.sqrt(
        propagation_constant**2 - outer_layers_permittivity*freespace_wavenumber**2
    )

    transcendential_function_value = np.tanh(
        middle_layer_wavevector_perpendicular_component * thickness / 2
    )

    algebraic_function_value = -1 * \
        (outer_layers_wavevector_perpendicular_component * middle_layer_permittivity) / \
        (middle_layer_wavevector_perpendicular_component * outer_layers_permittivity)

    return transcendential_function_value - algebraic_function_value


def transcendential_trilayer_odd_magnetic_field(
    propagation_constant: complex,
    wavelength: float,
    thickness: float,
    middle_layer_permittivity: 'float | complex',
    outer_layers_permittivity: 'float | complex',
) -> complex:
    """Describes a metal-dielectric-metal or dielectric-metal-dielectric symmetrical stack,
    even vector parity modes / the magnetic field is an odd function.

    Parameters
    ----------
    propagation_constant: float, unkown - vary to find the system solutions
    wavelength: float, at which the light propagates in free space
    thickness: float, of the middle layer
    middle_layer_permittivity: float or complex
    outer_layers_permittivity: float or complex

    Returns
    -------
    residual to be minimized: float

    Derivation
    ----------
    Maier SA. Plasmonics: Fundamentals and Applications, Chapter 2.3
    ISBN: 978-0-387-37825-1
    """
    freespace_wavenumber = utilities.wavelength_to_wavenumber(wavelength)

    middle_layer_wavevector_perpendicular_component = scimath.sqrt(
        propagation_constant**2 - middle_layer_permittivity*freespace_wavenumber**2
    )
    outer_layers_wavevector_perpendicular_component = scimath.sqrt(
        propagation_constant**2 - outer_layers_permittivity*freespace_wavenumber**2
    )

    transcendential_function_value = np.tanh(
        middle_layer_wavevector_perpendicular_component * thickness / 2
    )

    algebraic_function_value = -1 * \
        (middle_layer_wavevector_perpendicular_component * outer_layers_permittivity) / \
        (outer_layers_wavevector_perpendicular_component * middle_layer_permittivity)

    return transcendential_function_value - algebraic_function_value
