'''Surface plasmon polariton example usage'''

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from optical_dispersion_relations import plasmon, drude_lorentz


matplotlib.rc('font', size=12)
AIR_PERMITTIVITY = 1

METAL_DISPERSION_PARAMETERS = {
    'plasma_frequency': 1,
    'damping_constant': 0,
}


def drude_metal_surface_plasmon_polariton(frequencies, dielectric_permittivity):
    '''Surface plasmon polariton dispersion with simple Drude metal'''
    metal_permittivity = drude_lorentz.single_pole(
        frequencies, **METAL_DISPERSION_PARAMETERS)
    effective_refractive_index = plasmon.surface_plasmon_polariton(
        dielectric_permittivity, metal_permittivity)
    return effective_refractive_index


low_frequencies = np.arange(0.01, 2**(-0.5), 0.001)
transparency_frequencies = np.arange(2**(-0.5), 1, 0.001)
high_frequenies = np.arange(1, 1.2, 0.001)

low_frequency_effective_index = drude_metal_surface_plasmon_polariton(
    low_frequencies, AIR_PERMITTIVITY)
transparency_regime_effective_index = drude_metal_surface_plasmon_polariton(
    transparency_frequencies, AIR_PERMITTIVITY)
high_frequency_effective_index = drude_metal_surface_plasmon_polariton(
    high_frequenies, AIR_PERMITTIVITY)

fig, surface_plasmon_axes = plt.subplots()

surface_plasmon_axes.set_title(
    'Fig. 2.3 from \nMaier SA. Plasmonics: Fundamentals and Applications.')
surface_plasmon_axes.plot(low_frequencies*low_frequency_effective_index.real,
                          low_frequencies, linestyle='-', color='black')
surface_plasmon_axes.plot(transparency_frequencies*transparency_regime_effective_index.imag,
                          transparency_frequencies, linestyle='--', color='black')
surface_plasmon_axes.plot(high_frequenies*high_frequency_effective_index.real,
                          high_frequenies, linestyle='-', color='black')
surface_plasmon_axes.set_xlabel(r'Wave vector $\beta c/\omega_{p}$')
surface_plasmon_axes.set_ylabel(r'Frequency $\omega/\omega_{p}$')

surface_plasmon_axes.set_xlim(0, 4)
surface_plasmon_axes.set_ylim(0, 1.2)

fig.savefig('../images/surface_plasmon_polariton.png')
