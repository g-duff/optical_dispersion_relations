import numpy as np
import cmath as cm
import scipy.constants as spc
import scipy.interpolate as interp
import scipy.optimize as opt
import matplotlib.pyplot as plt
# import scipy.special as sps

def calc_spp_n_eff(eps_d, eps_m):
	'''Exact surface plasmon dispersion relation from [3]'''
	return np.sqrt(eps_d*eps_m/(eps_d+eps_m))

def c_approx_mim_n_eff(eps_d, eps_m, wav, ti):
	''' Collin's MIM eff index approximation, from [1]'''
 	n_eff=np.sqrt(eps_d)*np.sqrt(1+wav/(np.pi*ti*np.sqrt(-1*eps_m))*
		np.sqrt(1-eps_d/eps_m))
	return n_eff

def b_approx_mim_n_eff(eps_d, eps_m, wav, ti):
	''' Baumberg's MIM eff index approximation, from [2]'''
	k_0 = 2*np.pi/wav
	gamma = ((2*eps_d)/(k_0*ti*eps_m))**2
	k_ov_k0 = eps_d + (gamma/2)*(1+np.sqrt(1+4*(eps_d-eps_m)/gamma))
	n_eff = np.sqrt(k_ov_k0)
	return n_eff

def mim_disp(beta, k_0, eps_1, eps_2, w):
	'''Exact MIM dispersion relation from [3]
	Find Beta by finding the zeros of the function
	with the Newton-Raphson process'''
	k1 = cm.sqrt(beta**2-eps_1*k_0**2)
	k2 = cm.sqrt(beta**2-eps_2*k_0**2)
	ze = cm.tanh(k2*w/2)*(k2/eps_2)+k1/(eps_1)
	return ze

## Dashboard

wl = 1/np.linspace(1.0/1500, 1.0/350, 100)
# wl = np.linspace(300,1500,100)

i_n = 1.45
t_i = 20e-9

## Import data
m_wl, m_n, = np.genfromtxt('ag_n.txt', unpack=True, skip_header=1)
m_k = np.genfromtxt('ag_k.txt', unpack=True, skip_header=1, usecols=(1))

# Convert units
m_wl = m_wl*1e-6	# um to m
wl = wl*1e-9		# nm to m

## Calculate k, frequency, energy
k0 = 2*np.pi/wl
om = k0*spc.c
ev = om*spc.hbar/spc.e
THz = om/(2*np.pi*1e12)
ang_THz = om/(1e15)

## Interpolation
m_n = interp.griddata(m_wl, m_n, wl, method='cubic')
m_k = interp.griddata(m_wl, m_k, wl, method='cubic')

## Convert RI to permittivity
m_eps = (m_n + 1j*m_k)**2
i_eps = i_n**2

## Calcualte effective indices
spp_n_eff = calc_spp_n_eff(i_eps, m_eps)

# Calculate propagation constants
spp_beta = spp_n_eff*k0
k_light_line = i_n*k0

y = ang_THz

disp_fig, disp_ax = plt.subplots()
disp_ax.plot(spp_beta.real, y, label='SPP')
disp_ax.plot(k_light_line, y, 'k--', label='Light line')

index_fig, index_ax = plt.subplots()

index_ax.plot(wl*1e9, spp_n_eff.real, label='SPP')
index_ax.plot(wl*1e9, i_n*np.ones(len(wl)), 'k--', label='Insulator')

newt = spp_beta

for t_i in [100e-9, 50e-9, 40e-9, 30e-9, 25e-9, 20e-9]:

	print(t_i)

	# Newton-Raphson process
	aB = zip(newt, k0, m_eps)
	newt = np.array([
		opt.newton(mim_disp, a[0], args=(a[1], a[2], i_eps, t_i),
		maxiter=int(1e6), tol=1e3)
	 	for a in aB])

	# Output dispersion relation

	disp_ax.plot(newt.real, y, lw=2, label=str(t_i*1e9))
	index_ax.plot(wl*1e9, newt.real/k0, label=str(t_i*1e9))

disp_ax.set_xlabel(r'Propagation constant $\beta$')
disp_ax.set_ylabel(r'Energy (eV)')
# disp_ax.set_xlim([0, 10e7])
# disp_ax.set_ylim([1.0, 3.6])
disp_ax.legend(loc='lower right')

# plt.show()

# Output effective indices

# index_ax.plot(wl, c_mim_n_eff.real, label='Collin\'s MIM')
# index_ax.plot(wl, b_mim_n_eff.real, label='Baumberg\'s MIM ')

index_ax.set_xlabel('Free space wavelength (nm)')
index_ax.set_ylabel('Effective refractive index')
index_ax.legend()
plt.show()
