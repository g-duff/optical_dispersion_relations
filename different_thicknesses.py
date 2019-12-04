import numpy as np
import cmath as cm
import scipy.constants as spc
import scipy.interpolate as interp
import scipy.optimize as opt
import matplotlib.pyplot as plt
import mim_dispersions as dsp

## Wavelength range
wl = 1/np.linspace(1.0/1500, 1.0/350, 100)
# wl = np.linspace(300,1500,100)

# Insulator RI and thickness
i_n = 1.45
t_i = 20e-9

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
m_eps, i_eps = (m_n + 1j*m_k)**2, i_n**2

## Calcualte spp neff
spp_n_eff = dsp.spp_neff(i_eps, m_eps)
spp_beta = spp_n_eff*k0

k_light_line = i_n*k0

y = ang_THz

disp_fig, disp_ax = plt.subplots()
disp_ax.plot(spp_beta.real, y, label='SPP')
disp_ax.plot(k_light_line, y, 'k--', label='Light line')

index_fig, index_ax = plt.subplots()

index_ax.plot(wl*1e9, spp_n_eff.real, label='SPP')
index_ax.plot(wl*1e9, i_n*np.ones(len(wl)), 'k--', label='Insulator')

# Starting estimate for Newton-Raphson
newt = spp_beta

for t_i in [100e-9, 50e-9, 40e-9, 30e-9, 25e-9, 20e-9]:

	# Newton-Raphson process
	newt_args = zip(newt, k0, m_eps)
	newt = np.array([
		opt.newton(dsp.mim_disp, a[0], args=(a[1], a[2], i_eps, t_i),
		maxiter=int(1e6), tol=1e3) for a in newt_args])

	# Plot dispersion relation and effective index
	disp_ax.plot(newt.real, y, lw=2, label=str(t_i*1e9)+'nm')
	index_ax.plot(wl*1e9, newt.real/k0, label=str(t_i*1e9)+'nm')

disp_ax.set_xlabel(r'Propagation constant $\beta$')
disp_ax.set_ylabel(r'Energy (eV)')
disp_ax.legend(loc='lower right')

index_ax.set_xlabel('Free space wavelength (nm)')
index_ax.set_ylabel('Effective refractive index')
index_ax.legend()
plt.show()
