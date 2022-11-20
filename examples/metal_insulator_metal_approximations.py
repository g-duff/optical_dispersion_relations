'''Example metal-insulator-metal dispersion approximations example usage'''

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from optical_dispersion_relations import plasmon


matplotlib.rc('font', size=12)

collin_approximation_parameters = {
    'dielectric_permittivity': 1,
    'metal_permittivity': -50,
    'wavelength': 1,
    'insulator_thickness': np.logspace(-2, 1, 100),
}

sondergaard_approximation_parameters = {
    'dielectric_permittivity': 1,
    'metal_permittivity': -23.6+1.69j,
    'wavelength': 775,
    'insulator_thickness': np.arange(1, 3000),
}

collin_approximation = plasmon.metal_insulator_metal_collin_approximation(
    **collin_approximation_parameters
)

sondergaard_approximation = plasmon.metal_insulator_metal_sondergaard_narrow_approximation(
    **sondergaard_approximation_parameters
)

collin_approximation_figure, (collin_approximation_axes) = plt.subplots(ncols=1)
sondergaard_approximation_figure, (sondergaard_approximation_axes) = plt.subplots(ncols=1)

collin_approximation_axes.set_title(
    'Fig. 2 from \nhttps://doi.org/10.1364/OE.15.004310')
collin_approximation_axes.semilogx(
    collin_approximation_parameters['insulator_thickness'],
    collin_approximation.real,
    color='C3',
    label='coupled SPP approx.')
collin_approximation_axes.axhline(y=1, color='black', linestyle='--')
collin_approximation_axes.set_xlabel(r'Normalized width w/$\lambda$')
collin_approximation_axes.set_xlim(0.01, 10)
collin_approximation_axes.set_ylim(0.0, 3.0)
collin_approximation_axes.set_ylabel(r'Effective index $n_{1D}$')
collin_approximation_axes.legend()
collin_approximation_figure.tight_layout()
collin_approximation_figure.savefig('./collin_approximation_example.png')

sondergaard_approximation_axes.set_title(
    'Fig. 4 from \nhttps://doi.org/10.1364/OE.15.010869')
sondergaard_approximation_axes.plot(
    sondergaard_approximation_parameters['insulator_thickness'],
    sondergaard_approximation.real,
    color='C2',
    label='small-gap approximation')
sondergaard_approximation_axes.set_xlabel('Gap width (nm)')
sondergaard_approximation_axes.set_xlim(0, 3500)
sondergaard_approximation_axes.set_ylim(1, 1.4)
sondergaard_approximation_axes.set_ylabel('Mode effective index')
sondergaard_approximation_axes.legend()

sondergaard_approximation_figure.tight_layout()
sondergaard_approximation_figure.savefig('./sondergaard_approximation_example.png')
