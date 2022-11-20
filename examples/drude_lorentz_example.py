'''Drude Lorentz module example usage'''

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from optical_dispersion_relations import drude_lorentz


matplotlib.rc('font', size=12)
NANOMETERS = 1e-9
SPEED_OF_LIGHT = 3e8

wavelengths = np.arange(450, 1000, 1)

angular_frequency = 2*np.pi*SPEED_OF_LIGHT/(wavelengths*NANOMETERS)

silver_drude_parameters = {
    'dielectric_constant': 1,
    'plasma_frequency': 1.35e16,
    'damping_constant': 0.0023*1.35e16,
}

gold_drude_parameters = {
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

silver_permittivity = drude_lorentz.single_pole(
    angular_frequency, **silver_drude_parameters)
gold_permittivity = drude_lorentz.double_pole(
    angular_frequency, **gold_drude_parameters)

fig, (real_part_axes, imaginary_part_axes) = plt.subplots(
    ncols=2, figsize=(8, 4))

real_part_axes.plot(wavelengths, silver_permittivity.real,
                    'C0-', label='Silver')
real_part_axes.plot(wavelengths, gold_permittivity.real, 'C1-', label='Gold')
real_part_axes.set_xlabel('Free space wavelength (nm)')
real_part_axes.set_ylabel('Permittivity, real part')
real_part_axes.legend()

imaginary_part_axes.plot(
    wavelengths, silver_permittivity.imag, 'C0-',  label='Silver')
imaginary_part_axes.plot(
    wavelengths, gold_permittivity.imag, 'C1-',  label='Gold')
imaginary_part_axes.set_xlabel('Free space wavelength (nm)')
imaginary_part_axes.set_ylabel('Permittivity, imaginary part')
imaginary_part_axes.legend()

fig.tight_layout()

plt.show()
