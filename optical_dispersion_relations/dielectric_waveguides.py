"""Dielectric Waveduide dispersions"""

import numpy as np
from numpy.lib import scimath


def transcendential_slab_waveguide_te(
    waveguide_propagation_constant: float,
    free_space_wavenumber: float,
    waveguide_thickness: float,
    cover_refractive_index: float,
    guiding_layer_refractive_index: float,
    substrate_refractive_index: float,
) -> float:
    # pylint: disable = too-many-arguments
    """Transcendential equation for a slab waveguide with TE polarization.
    Find the value of waveguide_propagation_constant for which the function equals zero
    to solve the system.

    Parameters
    ----------
    waveguide_propagation_constant: float, unkown - vary to find the system solutions.
    free_space_wavenumber: float
    waveguide_thickness: float
    cover_refractive_index: float
    guiding_layer_refractive_index: float
    substrate_refractive_index: float

    Returns
    -------
    residual to be minimized: float

    Derivation
    ----------
    Yariv, A. Optical Electronics.
    ISBN-10: 0030474442
    ISBN-13: 9780030474446
    """

    cover_wavenumber = cover_refractive_index * free_space_wavenumber
    guiding_layer_wavenumber = guiding_layer_refractive_index * free_space_wavenumber
    substrate_wavenumber = substrate_refractive_index * free_space_wavenumber

    cover_parameter = scimath.sqrt(
        waveguide_propagation_constant**2 - cover_wavenumber**2)
    substrate_parameter = scimath.sqrt(
        waveguide_propagation_constant**2 - substrate_wavenumber**2)

    guiding_layer_parameter = scimath.sqrt(
        guiding_layer_wavenumber**2 - waveguide_propagation_constant**2)

    algebraic_function_value = algebraic_function(cover_parameter,
                                                  guiding_layer_parameter,
                                                  substrate_parameter)

    transcendential_function_value = np.tan(
        guiding_layer_parameter*waveguide_thickness)

    return np.abs(transcendential_function_value - algebraic_function_value)


def transcendential_slab_waveguide_tm(
    waveguide_propagation_constant: float,
    free_space_wavenumber: float,
    waveguide_thickness: float,
    cover_refractive_index: float,
    guiding_layer_refractive_index: float,
    substrate_refractive_index: float,
) -> float:
    # pylint: disable = too-many-arguments
    """Transcendential equation for a slab waveguide with TM polarization.
    Find the value of waveguide_propagation_constant for which the function equals zero
    to solve the system.

    Parameters
    ----------
    waveguide_propagation_constant: float, unkown - vary to find the system solutions.
    free_space_wavenumber: float
    waveguide_thickness: float
    cover_refractive_index: float
    guiding_layer_refractive_index: float
    substrate_refractive_index: float

    Returns
    -------
    residual to be minimized: float

    Derivation
    ----------
    Yariv, A. Optical Electronics.
    ISBN-10: 0030474442
    ISBN-13: 9780030474446
    """

    cover_wavenumber = cover_refractive_index * free_space_wavenumber
    guiding_layer_wavenumber = guiding_layer_refractive_index * free_space_wavenumber
    substrate_wavenumber = substrate_refractive_index * free_space_wavenumber

    cover_parameter = scimath.sqrt(waveguide_propagation_constant**2 - cover_wavenumber**2) \
        * (guiding_layer_refractive_index/cover_refractive_index)**2
    substrate_parameter = scimath.sqrt(
        waveguide_propagation_constant**2 - substrate_wavenumber**2
    ) * (guiding_layer_refractive_index/substrate_refractive_index)**2

    guiding_layer_parameter = scimath.sqrt(
        guiding_layer_wavenumber**2 - waveguide_propagation_constant**2)

    algebraic_function_value = algebraic_function(cover_parameter,
                                                  guiding_layer_parameter,
                                                  substrate_parameter)

    transcendential_function_value = np.tan(
        guiding_layer_parameter*waveguide_thickness)

    return np.abs(transcendential_function_value - algebraic_function_value)


def algebraic_function(cover_parameter: complex,
                       guiding_layer_parameter: complex,
                       substrate_parameter) -> complex:
    # pylint: disable = missing-function-docstring
    algebraic_function_value = guiding_layer_parameter \
        * (substrate_parameter + cover_parameter) \
        / (guiding_layer_parameter**2 - substrate_parameter*cover_parameter)

    return algebraic_function_value
