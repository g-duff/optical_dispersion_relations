import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def drude_model_1pole(omega, eps_inf, omegap, gamma, omega0):
    '''1 pole Drude model for silver''' 
    eps = eps_inf - omegap**2/(omega**2 + 1j*gamma*omega-omega0**2)
    return eps


def drude_model_2pole(omega, eps_inf, omegap1, gamma1, omega01, omegap2, gamma2, omega02):
    eps = eps_inf*(1 - omegap1**2/(omega**2 - omega01**2 + 1j*gamma1*omega)\
                     - omegap2**2/(omega**2 - omega02**2 + 1j*gamma2*omega))
    return eps


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


Ag_params = {
    'eps_inf': 1, 
    'omegap': 1.35e16, 
    'gamma': 0.0023*1.35e16,
    'omega0': 0
}

Au_params = {
    'eps_inf': 6,
    'omegap1': 5.37e15, 
    'gamma1': 6.216e13,
    'omega01': 0,
    'omegap2': 2.263e15,
    'gamma2': 1.332e15,
    'omega02': 4.572e15
}

Ag_jc_epsilon = 1*(Ag_n**2-Ag_k**2) + 1j*(2*Ag_n*Ag_k)
Au_jc_epsilon = 1*(Au_n**2-Au_k**2) + 1j*(2*Au_n*Au_k)

wl = np.arange(0.45, 1.0, 0.001)
omega = 2*np.pi*3e8/(wl*1e-6)
Ag_drude = drude_model_1pole(omega, **Ag_params)
Au_drude = drude_model_2pole(omega, **Au_params)


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
