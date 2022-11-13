'''Utilities for calculating optical parameters'''
import numpy as np


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
