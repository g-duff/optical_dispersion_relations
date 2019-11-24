import numpy as np
import cmath as cm
import scipy.constants as spc
import scipy.interpolate as interp
import scipy.optimize as opt
import matplotlib.pyplot as plt
import plasmonics as pls

## Wavelength
wl = 650
t_i = np.arange(100e-9, 5e-9, -1e-9)

# Insulator RI and thickness
i_n = 1.45

## Metal refractive index and extinction coefficient
m_wl, m_n, = np.genfromtxt('./Dispersion relations/ag_n.txt',
	unpack=True, skip_header=1)
m_k = np.genfromtxt('./Dispersion relations/ag_k.txt',
	unpack=True, skip_header=1, usecols=(1))

# Convert units
m_wl = m_wl*1e-6	# um to m
wl = wl*1e-9		# nm to m

## Calculate wavevector, frequency, energy
k0 = 2*np.pi/wl
om = k0*spc.c
ev = om*spc.hbar/spc.e
THz = om/(2*np.pi*1e12)
ang_THz = om/(1e15)

## Interpolate metal n and k to match user wavelength range
m_n = interp.griddata(m_wl, m_n, wl, method='cubic')
m_k = interp.griddata(m_wl, m_k, wl, method='cubic')

## Convert RI to permittivity
m_eps = (m_n + 1j*m_k)**2
i_eps = i_n**2

## Calcualte spp neff
spp_n_eff = pls.spp_neff(i_eps, m_eps)
spp_beta = spp_n_eff*k0

# Starting estimate for Newton-Raphson
newt = spp_beta
t_sweep = []

for ti in t_i:
	# Newton-Raphson process, decreasing gap thickness
	newt = opt.newton(pls.mim_disp, newt, args=(k0, m_eps, i_eps, ti),
		maxiter=int(1e6), tol=1e3)
	t_sweep.append(newt.real/k0)

plt.plot(t_i, t_sweep)
plt.show()
