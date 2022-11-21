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

    Parameters:
        waveguide_propagation_constant: unknown, vary to find the system solutions.
        free_space_wavenumber
        waveguide_thickness
        cover_refractive_index
        guiding_layer_refractive_index
        substrate_refractive_index

    Returns:
        residual to be minimized

    Derivation in:
        Yariv, A. Optical Electronics.
        ISBN-10: 0030474442
        ISBN-13: 9780030474446
    '''

    cover_wavenumber = cover_refractive_index * free_space_wavenumber
    guiding_layer_wavenumber = guiding_layer_refractive_index * free_space_wavenumber
    substrate_wavenumber = substrate_refractive_index * free_space_wavenumber

    cover_propagation_constant = np.sqrt(
        waveguide_propagation_constant**2 - cover_wavenumber**2)
    guiding_layer_propagation_constant = np.sqrt(
        guiding_layer_wavenumber**2 - waveguide_propagation_constant**2)
    substrate_propagation_constant = np.sqrt(
        waveguide_propagation_constant**2 - substrate_wavenumber**2)

    algebraic_function_value = algebraic_function(cover_propagation_constant,
                                                  guiding_layer_propagation_constant,
                                                  substrate_propagation_constant)

    transcendential_function_value = np.tan(
        guiding_layer_propagation_constant*waveguide_thickness)

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

    Parameters:
        waveguide_propagation_constant: unknown, vary to find the system solutions.
        free_space_wavenumber
        waveguide_thickness
        cover_refractive_index
        guiding_layer_refractive_index
        substrate_refractive_index

    Returns:
        residual to be minimized

    Derivation in:
        Yariv, A. Optical Electronics.
        ISBN-10: 0030474442
        ISBN-13: 9780030474446
    '''

    cover_wavenumber = cover_refractive_index * free_space_wavenumber
    guiding_layer_wavenumber = guiding_layer_refractive_index * free_space_wavenumber
    substrate_wavenumber = substrate_refractive_index * free_space_wavenumber

    cover_propagation_constant = np.sqrt(
        waveguide_propagation_constant**2 - cover_wavenumber**2)
    guiding_layer_propagation_constant = np.sqrt(
        guiding_layer_wavenumber**2 - waveguide_propagation_constant**2)
    substrate_propagation_constant = np.sqrt(
        waveguide_propagation_constant**2 - substrate_wavenumber**2)

    adjusted_cover_propagation_constant = cover_propagation_constant * \
        (guiding_layer_refractive_index/cover_refractive_index)**2
    adjusted_substrate_propagation_constant = substrate_propagation_constant * \
        (guiding_layer_refractive_index/substrate_refractive_index)**2

    algebraic_function_value = algebraic_function(adjusted_cover_propagation_constant,
                                                  guiding_layer_propagation_constant,
                                                  adjusted_substrate_propagation_constant)

    transcendential_function_value = np.tan(
        guiding_layer_propagation_constant*waveguide_thickness)

    return transcendential_function_value - algebraic_function_value


def algebraic_function(cover_propagation_constant,
                       guiding_layer_propagation_constant,
                       substrate_propagation_constant):
    # pylint: disable = missing-function-docstring
    algebraic_function_value = guiding_layer_propagation_constant\
        * (substrate_propagation_constant+cover_propagation_constant) \
        / (guiding_layer_propagation_constant**2 -
            substrate_propagation_constant*cover_propagation_constant
           )

    return algebraic_function_value
