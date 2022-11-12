import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from src.dispersion_relations import drude_lorentz


Ag_wl, Ag_n = np.loadtxt('./material_dispersions/ag_n.txt', unpack=True, delimiter='\t', skiprows=1)
_, Ag_k = np.loadtxt('./material_dispersions/ag_k.txt', unpack=True, delimiter='\t', skiprows=1)

Au_wl, Au_n = np.loadtxt('./material_dispersions/au_n.txt', unpack=True, delimiter='\t', skiprows=1)
_, Au_k = np.loadtxt('./material_dispersions/au_k.txt', unpack=True, delimiter='\t', skiprows=1)


# Truncate silver to region of interest
i1, i2 = np.argmin((Ag_wl-450*1e-3)**2), np.argmin((Ag_wl-1050*1e-3)**2)
Ag_wl = Ag_wl[i1:i2]
Ag_n = Ag_n[i1:i2]
Ag_k = Ag_k[i1:i2]

# Truncate gold to region of interest
i1, i2 = np.argmin((Au_wl-450*1e-3)**2), np.argmin((Au_wl-1050*1e-3)**2)
Au_wl = Au_wl[i1:i2]
Au_n = Au_n[i1:i2]
Au_k = Au_k[i1:i2]


silver_drude_parameters = {
    'dielectric_constant': 1,
    'plasma_frequency': 1.35e16,
    'damping_rate': 0.0023*1.35e16,
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

Ag_jc_epsilon = 1*(Ag_n**2-Ag_k**2) + 1j*(2*Ag_n*Ag_k)
Au_jc_epsilon = 1*(Au_n**2-Au_k**2) + 1j*(2*Au_n*Au_k)

wl = np.arange(0.45, 1.0, 0.001)
omega = 2*np.pi*3e8/(wl*1e-6)
Ag_drude = drude_lorentz.single_pole(omega, **silver_drude_parameters)
Au_drude = drude_lorentz.double_pole(omega, **gold_drude_parameters)


font = {'size': 12}
matplotlib.rc('font', **font)

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4))

## Real part comparison
ax1.plot(Ag_wl*1e3, Ag_jc_epsilon.real, 'C0.', label='Ag experimental')
ax1.plot(Au_wl*1e3, Au_jc_epsilon.real, 'C1.', label='Au experimental')
ax1.plot(wl*1e3, Ag_drude.real, 'C0-', label='Ag Drude model')
ax1.plot(wl*1e3, Au_drude.real, 'C1-', label='Au Drude model')
ax1.set_xlabel('Free space wavelength (nm)')
ax1.set_ylabel(r'$\epsilon$, real part')
ax1.legend()

# Imaginary part comparison
ax2.plot(Ag_wl*1e3, Ag_jc_epsilon.imag, 'C0.', label='Ag experimental')
ax2.plot(Au_wl*1e3, Au_jc_epsilon.imag, 'C1.', label='Au experimental')
ax2.plot(wl*1e3, Ag_drude.imag, 'C0-',  label='Ag Drude model')
ax2.plot(wl*1e3, Au_drude.imag, 'C1-',  label='Au Drude model')
ax2.set_xlabel('Free space wavelength (nm)')
ax2.set_ylabel(r'$\epsilon$, imaginary part')
ax2.legend()

fig.tight_layout()
fig.savefig('Compare_drude_to_johnson_christy.png', transparent=True)

plt.show()
