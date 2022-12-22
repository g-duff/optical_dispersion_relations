'''Drude Lorentz module example usage'''

import numpy as np
from scipy import constants as const
import matplotlib
import matplotlib.pyplot as plt

from optical_dispersion_relations import drude_lorentz
from optical_dispersion_relations import utilities

matplotlib.rc('font', size=12)


SILVER_DRUDE_PARAMETERS = {
    'dielectric_constant': 1,
    'plasma_frequency': 1.35e16,
    'damping_constant': 0.0023*1.35e16,
}

GOLD_DRUDE_PARAMETERS = {
    'dielectric_constant': 6,
    'plasma_frequency': 1,
    'first_pole': {
        'peak_strength': 5.37e15**2,
        'damping_constant': 6.216e13,
        'peak_position': 0,
    },
    'second_pole': {
        'peak_strength': 2.263e15**2,
        'damping_constant': 1.332e15,
        'peak_position': 4.572e15
    }
}

GOLD_FILEPATH = './empirical_data/gold.txt'
SILVER_FILEPATH = './empirical_data/silver.txt'

FILE_FORMAT = {
        'unpack':True,
        'skip_header':1,
        'converters': { 0: lambda x: float(x)*const.micro }
        }

if __name__ == '__main__':
    wavelengths = np.arange(450, 1000, 1)*const.nano

    angular_frequency = 2*const.pi*const.speed_of_light/(wavelengths)

    silver_permittivity = drude_lorentz.single_pole(
        angular_frequency, **SILVER_DRUDE_PARAMETERS)
    gold_permittivity = drude_lorentz.double_pole(
        angular_frequency, **GOLD_DRUDE_PARAMETERS)

    silver_wavelengths, silver_refractive_index, silver_extinction_coefficient = \
            np.genfromtxt(SILVER_FILEPATH, **FILE_FORMAT)
    gold_wavelengths, gold_refractive_index, gold_extinction_coefficient = \
            np.genfromtxt(GOLD_FILEPATH, **FILE_FORMAT)

    silver_empirical_permittivity = utilities.refractive_index_to_permittivity(
            silver_refractive_index + 1j*silver_extinction_coefficient)
    gold_empirical_permittivity = utilities.refractive_index_to_permittivity(
            gold_refractive_index + 1j*gold_extinction_coefficient)

    fig, (real_part_axes, imaginary_part_axes) = plt.subplots(
        ncols=2, figsize=(8, 4))

    real_part_axes.plot(wavelengths/const.nano, silver_permittivity.real,
                        'C0-', label='Silver')
    real_part_axes.plot(silver_wavelengths/const.nano, silver_empirical_permittivity.real,
                        'C0o')
    real_part_axes.plot(wavelengths/const.nano, gold_permittivity.real,
                        'C1-', label='Gold')
    real_part_axes.plot(gold_wavelengths/const.nano, gold_empirical_permittivity.real,
                        'C1o')
    real_part_axes.set_xlabel('Free space wavelength (nm)')
    real_part_axes.set_ylabel('Permittivity, real part')
    real_part_axes.legend()

    imaginary_part_axes.plot(
        wavelengths/const.nano, silver_permittivity.imag, 'C0-',  label='Silver')
    imaginary_part_axes.plot(silver_wavelengths/const.nano, silver_empirical_permittivity.imag,
                        'C0o')
    imaginary_part_axes.plot(
        wavelengths/const.nano, gold_permittivity.imag, 'C1-',  label='Gold')
    imaginary_part_axes.plot(gold_wavelengths/const.nano, gold_empirical_permittivity.imag,
                        'C1o')
    imaginary_part_axes.set_xlabel('Free space wavelength (nm)')
    imaginary_part_axes.set_ylabel('Permittivity, imaginary part')
    imaginary_part_axes.legend()

    fig.tight_layout()
    fig.savefig('../images/drude_lorentz_example.png')

