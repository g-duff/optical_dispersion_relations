'''Plasmonics Dispersion Relations'''
import numpy as np

def surface_plasmon_polariton(dielectric_permittivity, metal_permittivity):
    '''Exact surface plasmon dispersion relation for TM polarization.
    Surface plasmons only exist for TM polarization.

    Parameters:
        dielectric_permittivity: float, complex number or numpy array
        metal_permittivity: float, complex number or numpy array

    Returns:
        permittivity of surface plasmon polariton: complex number or numpy array

    Derivation in:
    Maier SA. Plasmonics: fundamentals and applications.
    ISBN: 978-0-387-37825-1
    '''
    numerator = dielectric_permittivity*metal_permittivity
    denominator = dielectric_permittivity+metal_permittivity
    permittivity = np.sqrt(numerator/denominator)
    return permittivity
