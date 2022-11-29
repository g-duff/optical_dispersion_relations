'''Dielectric Waveduide dispersions'''

import numpy as np


def transcendential_slab_waveguide_TE(
    waveguide_propagation_constant,
    free_space_wavenumber,
    waveguide_thickness,
    cover_refractive_index,
    guiding_layer_refractive_index,
    substrate_refractive_index,
):
    # pylint: disable = invalid-name, too-many-arguments
    '''Transcendential equation for a slab waveguide with TE polarization.
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
    '''

    cover_wavenumber = cover_refractive_index * free_space_wavenumber
    guiding_layer_wavenumber = guiding_layer_refractive_index * free_space_wavenumber
    substrate_wavenumber = substrate_refractive_index * free_space_wavenumber

    cover_parameter = np.sqrt(
        waveguide_propagation_constant**2 - cover_wavenumber**2)
    substrate_parameter = np.sqrt(
        waveguide_propagation_constant**2 - substrate_wavenumber**2)

    guiding_layer_parameter = np.sqrt(
        guiding_layer_wavenumber**2 - waveguide_propagation_constant**2)

    algebraic_function_value = algebraic_function(cover_parameter,
                                                  guiding_layer_parameter,
                                                  substrate_parameter)

    transcendential_function_value = np.tan(
        guiding_layer_parameter*waveguide_thickness)

    return transcendential_function_value - algebraic_function_value


def transcendential_slab_waveguide_TM(
    waveguide_propagation_constant,
    free_space_wavenumber,
    waveguide_thickness,
    cover_refractive_index,
    guiding_layer_refractive_index,
    substrate_refractive_index,
):
    # pylint: disable = invalid-name, too-many-arguments
    '''Transcendential equation for a slab waveguide with TM polarization.
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
    '''

    cover_wavenumber = cover_refractive_index * free_space_wavenumber
    guiding_layer_wavenumber = guiding_layer_refractive_index * free_space_wavenumber
    substrate_wavenumber = substrate_refractive_index * free_space_wavenumber

    cover_parameter = np.sqrt(waveguide_propagation_constant**2 - cover_wavenumber**2) \
        * (guiding_layer_refractive_index/cover_refractive_index)**2
    substrate_parameter = np.sqrt(waveguide_propagation_constant**2 - substrate_wavenumber**2) \
        * (guiding_layer_refractive_index/substrate_refractive_index)**2

    guiding_layer_parameter = np.sqrt(
        guiding_layer_wavenumber**2 - waveguide_propagation_constant**2)

    algebraic_function_value = algebraic_function(cover_parameter,
                                                  guiding_layer_parameter,
                                                  substrate_parameter)

    transcendential_function_value = np.tan(
        guiding_layer_parameter*waveguide_thickness)

    return transcendential_function_value - algebraic_function_value


def algebraic_function(cover_parameter,
                       guiding_layer_parameter,
                       substrate_parameter):
    # pylint: disable = missing-function-docstring
    algebraic_function_value = guiding_layer_parameter \
        * (substrate_parameter + cover_parameter) \
        / (guiding_layer_parameter**2 - substrate_parameter*cover_parameter)

    return algebraic_function_value
