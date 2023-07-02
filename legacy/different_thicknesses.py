import numpy as np
import scipy.constants as const
import scipy.interpolate as interp
import scipy.optimize as opt
import matplotlib.pyplot as plt

from optical_dispersion_relations import plasmon, utilities


## Wavelength range
wavelengths = 1/np.linspace(1.0/1500, 1.0/350, 100)*const.nano

# Insulator RI and thickness
dielectric_refractive_index = 1.45
thickness = 20*const.nano

## Metal refractive index and extinction coefficient
metal_wavelengths, metal_refractive_index, = np.genfromtxt('./material_dispersions/ag_n.txt',
	unpack=True, skip_header=1)
metal_extinction_coefficient = np.genfromtxt('./material_dispersions/ag_k.txt',
	unpack=True, skip_header=1, usecols=(1))
metal_wavelengths = metal_wavelengths*const.micro

## Calculate wavevector, frequency, energy
wavenumbers = 2*const.pi/wavelengths
angular_frequency = wavenumbers*const.c

## Interpolate metal n and k to match user wavelength range
metal_refractive_index = interp.griddata(metal_wavelengths, metal_refractive_index, wavelengths, method='cubic')
metal_extinction_coefficient = interp.griddata(metal_wavelengths, metal_extinction_coefficient, wavelengths, method='cubic')

## Convert RI to permittivity
metal_permittivities = utilities.refractive_index_to_permittivity(metal_refractive_index + 1j*metal_extinction_coefficient)
dielectric_permittivity = utilities.refractive_index_to_permittivity(dielectric_refractive_index).real

## Calcualte spp neff
surface_plasmon_polariton_effective_index = plasmon.surface_plasmon_polariton(
        dielectric_permittivity, 
        metal_permittivities
)
surface_plasmon_polariton_propagation_constant = surface_plasmon_polariton_effective_index*wavenumbers

y = angular_frequency

disp_fig, disp_ax = plt.subplots()
disp_ax.plot(surface_plasmon_polariton_propagation_constant.real, y, label='SPP')
disp_ax.plot(dielectric_refractive_index*wavenumbers, y, 'k--', label='Light line')

index_fig, index_ax = plt.subplots()

index_ax.plot(wavelengths*1e9, surface_plasmon_polariton_effective_index.real, label='SPP')
index_ax.plot(wavelengths*1e9, dielectric_refractive_index*np.ones(len(wavelengths)), 'k--', label='Insulator')

# Starting estimate for Newton-Raphson
newt = surface_plasmon_polariton_propagation_constant

for thickness in [100e-9, 50e-9, 40e-9, 30e-9, 25e-9, 20e-9]:

    # Newton-Raphson process
    initial_guesses = newt
    newt = np.array([
        opt.newton(
            func=plasmon.transcendential_trilayer_even_magnetic_field,
            x0=initial_guess,
            args=(wavelength, thickness, dielectric_permittivity, metal_permittivity),
            maxiter=int(1e6),
            tol=1e3
        ) for initial_guess, wavelength, metal_permittivity in
        zip(initial_guesses, wavelengths, metal_permittivities)
    ])

    # Plot dispersion relation and effective index
    thickness_in_nm = round(thickness / const.nano)
    disp_ax.plot(newt.real, y, lw=2, label=f'{thickness_in_nm} nm')
    index_ax.plot(wavelengths/const.nano, newt.real/wavenumbers, label=f'{thickness_in_nm} nm')

disp_ax.set_xlabel(r'Propagation constant $\beta$')
disp_ax.set_ylabel(r'Energy (eV)')
disp_ax.legend(loc='lower right')

index_ax.set_xlabel('Free space wavelength (nm)')
index_ax.set_ylabel('Effective refractive index')
index_ax.legend()
plt.show()
