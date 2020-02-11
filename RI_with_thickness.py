import numpy as np
import scipy.constants as spc
from scipy.interpolate import griddata
import scipy.optimize as opt
import matplotlib
import matplotlib.pyplot as plt
import mim_dispersions as dsp

font = {'size':16}
matplotlib.rc('font', **font)

## Wavelength Insulator RI and thickness
wl = 650
t_i = np.arange(100e-9, 5e-9, -1e-9)
i_n = 1.45

## Metal refractive index and extinction coefficient
m_wl, m_n, = np.genfromtxt('./material_dispersions/ag_n.txt',
	unpack=True, skip_header=1)
m_k = np.genfromtxt('./material_dispersions/ag_k.txt',
	unpack=True, skip_header=1, usecols=(1))

# Convert units
m_wl = m_wl*1e-6	# um to m
wl = wl*1e-9		# nm to m

## Calculate wavevector, frequency, energy
k0 = 2*np.pi/wl

## Interpolate metal n and k to match user wavelength range
m_n = griddata(m_wl, m_n, wl, method='cubic')
m_k = griddata(m_wl, m_k, wl, method='cubic')

## Convert RI to permittivity
m_eps = (m_n + 1j*m_k)**2
i_eps = i_n**2

## Calcualte spp neff
spp_n_eff = dsp.spp_neff(i_eps, m_eps)
spp_beta = spp_n_eff*k0

# Starting estimate for Newton-Raphson
newt = spp_beta
t_sweep = []

for ti in t_i:
	# Newton-Raphson process, decreasing gap thickness
	newt = opt.newton(dsp.mim_disp, newt, args=(k0, m_eps, i_eps, ti),
		maxiter=int(1e6), tol=1e3)
	t_sweep.append(newt.real/k0)

fig, ax = plt.subplots()
ax.plot(t_i*1e9, t_sweep, label='Silica MIM')
ax.axhline(i_n, color='C0', ls='--', lw=2, label='Silica')

ax.set_xlabel('Insulator thickness (nm)')
ax.set_ylabel('Effective index')
ax.grid(True)
ax.legend(loc='best', title='Refractive indices')
plt.tight_layout()
plt.show()
