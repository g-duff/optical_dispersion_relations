import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import constants as const, optimize as opt
from scipy.interpolate import griddata

from optical_dispersion_relations import plasmon, utilities

font = {'size': 16}
matplotlib.rc('font', **font)

FILE_FORMAT = {
    'unpack': True,
    'skip_header': 1,
    'converters': {0: lambda x: float(x)*const.micro}
}

METAL_REFRACTIVE_INDEX_FILEPATH = '../examples/scripts/empirical_data/silver.txt'

if __name__ == '__main__':

    ## Wavelength Insulator RI and thickness
    wavelength = 650*const.nano
    dielectric_thicknesses = np.arange(100, 5, -1)*const.nano
    dielectric_refractive_index = 1.45

    ## Metal refractive index and extinction coefficient
    metal_wavelengths, metal_refractive_index, metal_extinction_coefficient = \
        np.genfromtxt(METAL_REFRACTIVE_INDEX_FILEPATH, **FILE_FORMAT)

    wavenumber = utilities.wavelength_to_wavenumber(wavelength)

    ## Interpolate metal n and k to match user wavelength range
    metal_refractive_index = griddata(metal_wavelengths, metal_refractive_index, wavelength, method='cubic')
    metal_extinction_coefficient = griddata(metal_wavelengths, metal_extinction_coefficient, wavelength, method='cubic')

    ## Convert RI to permittivity
    metal_permittivity = utilities.refractive_index_to_permittivity(
            metal_refractive_index + 1j*metal_extinction_coefficient)
    dielectric_permittivity = utilities.refractive_index_to_permittivity(dielectric_refractive_index).real

    t_sweep = []

    for thickness in dielectric_thicknesses:
        # Newton-Raphson process, decreasing gap thickness
        converged_propagation_constant = opt.newton(
            func=plasmon.transcendential_trilayer_even_magnetic_field,
            x0=wavenumber*plasmon.metal_dielectric_metal_sondergaard_narrow_approximation(
                wavelength, thickness, dielectric_permittivity, metal_permittivity 
            ),
            args=(wavelength, thickness, dielectric_permittivity, metal_permittivity),
            maxiter=int(1e6),
            tol=1e3,
            full_output=True
        )[0]
        t_sweep.append(converged_propagation_constant.real/wavenumber)

    fig, ax = plt.subplots()
    ax.plot(dielectric_thicknesses*1e9, t_sweep, label='Silica MIM')
    ax.axhline(dielectric_refractive_index, color='C0', ls='--', lw=2, label='Silica')

    ax.set_xlabel('Insulator thickness (nm)')
    ax.set_ylabel('Effective index')
    ax.legend(loc='best', title='Refractive indices')
    plt.tight_layout()
    plt.show()
