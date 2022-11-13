'''Utilities for calculating optical parameters'''
import numpy as np


def permittivity_to_extinction_coefficient(
    permittivity: complex
) -> float:
    '''Convert complex permittivity to extinction coefficient

    Parameters:
        permittivity

    Returns:
        extinction coefficient
    '''
    refractive_index: complex = permittivity_to_refractive_index(
        permittivity)
    extinction_coefficient = refractive_index.imag
    return extinction_coefficient


def permittivity_to_refractive_index(
    permittivity: complex
) -> complex:
    '''Convert complex permittivity to complex refractive index

    Parameters:
        permittivity

    Returns:
        complex refractive index
    '''
    return np.sqrt(permittivity)


def refractive_index_to_permittivity(
    refractive_index: complex
) -> complex:
    '''Convert complex refractive index to complex permittivity

    Parameters:
        refractive_index

    Returns:
        complex permittivity
    '''
    return refractive_index**2
