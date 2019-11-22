import numpy as np
import scipy.interpolate as interp
import scipy.optimize as opt
import matplotlib.pyplot as plt
import scipy.constants as spc

def calc_spp_n_eff(eps_d, eps_m):
	return np.sqrt(eps_d*eps_m/(eps_d+eps_m))

def s_approx_mim_n_eff(eps_d, eps_m, wav, ti):
	''' Sorndergaard's MIM eff index approximation'''
	return kgsp

## Dashboard
wl = 750
i_n = 1.45
t_i = 20e-9

## Import data
m_wl, m_n, = np.loadtxt('ag_n.txt', unpack=True, skiprows=1)
m_wl_2, m_k = np.loadtxt('ag_k.txt', unpack=True, skiprows=1)

# Convert units
m_wl = m_wl*1e-6	# um to m
wl = wl*1e-9		# nm to m

## Calculate free space frequency, wavelength, energy
k0 = 2*np.pi/wl
om = k0*spc.c
ev = om*spc.hbar/spc.e

## Interpolation
m_n = interp.griddata(m_wl, m_n, wl, method='cubic')
m_k = interp.griddata(m_wl, m_k, wl, method='cubic')

## Convert RI to permittivity
m_eps = (m_n - 1j*m_k)**2
i_eps = i_n**2

## Calcualte effective indices
print(wl[0])
print(t_i)
spp_n_eff = calc_spp_n_eff(i_eps, m_eps)
c_mim_n_eff = c_approx_mim_n_eff(i_eps, m_eps, wl, t_i)
b_mim_n_eff = b_approx_mim_n_eff(i_eps, m_eps, wl, t_i)


# Calculate propagation constants 
# mim_beta = opt.leastsq(mim_disp, mim_beta_approx.real, args=(k0, m_eps, i_eps, t_i))
spp_beta = spp_n_eff*k0
c_mim_beta_approx = c_mim_n_eff*k0
b_mim_beta_approx = b_mim_n_eff*k0
s_mim_beta_approx = s_approx_mim_n_eff(i_eps, m_eps, wl, t_i)
k_light_line = i_n*k0

# ## Output material parameters
# wl = wl*1e9
# eps_fig, eps_ax = plt.subplots()
# eps_ax.plot(m_eps.real, ev, label='Real part')
# eps_ax.plot(m_eps.imag, ev, label='Imaginary part')
# eps_ax.set_xlabel('Wavelength (nm)')

# Output dispersion relation
# om = om/(2*np.pi*1e12)	# to THz
om = om/(1e12)		# to angular THz
disp_fig, disp_ax = plt.subplots()
disp_ax.plot(spp_beta.real, ev, label='SPP')
disp_ax.plot(c_mim_beta_approx.real, ev, label='Collin\'s MIM ')
disp_ax.plot(b_mim_beta_approx.real, ev, label='Baumberg\'s MIM ')
disp_ax.plot(s_mim_beta_approx.real, ev, label='Baumberg\'s MIM ')
# disp_ax.plot(k_light_line, ev, 'k--', label='Light line')
# disp_ax.set_xlabel(r'Propagation constant $\beta$')
# disp_ax.set_ylabel(r'Frequency THz')
disp_ax.legend(loc='best')
plt.show()

# # Output effective indices
index_fig, index_ax = plt.subplots()
index_ax.plot(wl, spp_n_eff.real, label='SPP')
index_ax.plot(wl, c_mim_n_eff.real, label='MIM')
index_ax.plot(wl, b_mim_n_eff.real, label='MIM')
index_ax.plot(wl, i_n*np.ones(len(wl)), 'k--', label='Insulator')
index_ax.set_xlabel('Free space wavelength (nm)')
index_ax.set_ylabel('Effective refractive index')
index_ax.legend()
plt.show()
