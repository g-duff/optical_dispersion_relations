'''Example metal-insulator-metal dispersion approximations example usage'''

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from optical_dispersion_relations import plasmon


matplotlib.rc('font', size=12)

sondergaard_approximation_parameters = {
    'dielectric_permittivity': 1,
    'metal_permittivity': -23.6+1.69j,
    'wavelength': 775,
    'insulator_thickness': np.arange(1, 3000),
}

sondergaard_approximation = plasmon.metal_insulator_metal_sondergaard_narrow_approximation(
    **sondergaard_approximation_parameters
)

collin_approximation_figure, (collin_approximation_axes) = plt.subplots(ncols=1)
sondergaard_approximation_figure, (sondergaard_approximation_axes) = plt.subplots(ncols=1)

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
