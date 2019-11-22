import numpy as np
import cmath as cm
import scipy.constants as spc
import scipy.interpolate as interp
import scipy.optimize as opt
import matplotlib.pyplot as plt
# import scipy.special as sps

def calc_spp_n_eff(eps_d, eps_m):
	return np.sqrt(eps_d*eps_m/(eps_d+eps_m))

def c_approx_mim_n_eff(eps_d, eps_m, wav, ti):
	''' Collin's MIM eff index approximation'''
 	n_eff=np.sqrt(eps_d)*np.sqrt(1+wav/(np.pi*ti*np.sqrt(-1*eps_m))*
		np.sqrt(1-eps_d/eps_m))
	return n_eff

def b_approx_mim_n_eff(eps_d, eps_m, wav, ti):
	''' Baumberg's MIM eff index approximation'''
	k_0 = 2*np.pi/wav
	gamma = ((2*eps_d)/(k_0*ti*eps_m))**2
	k_ov_k0 = eps_d + (gamma/2)*(1+np.sqrt(1+4*(eps_d-eps_m)/gamma))
	n_eff = np.sqrt(k_ov_k0)
	return n_eff

def mim_disp(beta, k_0, eps_1, eps_2, w):
	''' Minimise to find beta'''
	k1 = cm.sqrt(beta**2-eps_1*k_0**2)
	k2 = cm.sqrt(beta**2-eps_2*k_0**2)
	ze = cm.tanh(k2*w/2)*(k2/eps_2)+k1/(eps_1)
	return ze

## Dashboard

# wl = 1/np.linspace(1.0/1800, 1.0/300, 100)
wl = np.linspace(300,1500,100)

i_n = 1.45
t_i = 20e-9

## Import data
m_wl, m_n, = np.genfromtxt('au_n.txt', unpack=True, skip_header=1)
m_k = np.genfromtxt('au_k.txt', unpack=True, skip_header=1, usecols=(1))

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
c_mim_n_eff = c_approx_mim_n_eff(i_eps, m_eps, wl, t_i)
b_mim_n_eff = b_approx_mim_n_eff(i_eps, m_eps, wl, t_i)

# Calculate propagation constants
spp_beta = spp_n_eff*k0
c_mim_beta_approx = c_mim_n_eff*k0
b_mim_beta_approx = b_mim_n_eff*k0
k_light_line = i_n*k0

## Calculate analytical MIM dispersion using different numerical methods
aB = zip(k0, m_eps)
beta = np.linspace(0.05e8, 10e7, 200)

# Finding the min value
res = [[abs(mim_disp(b, a[0], a[1], i_eps, t_i)) for b in beta] for a in aB]
res = np.array(res)
min_beta = beta[np.argmin(res, axis=1)]

# Newton-Raphson process
aB = zip(min_beta, k0, m_eps)
newt = np.array([opt.newton(mim_disp, a[0], args=(a[1], a[2], i_eps, t_i))
 	for a in aB])

newt = newt.real

# Output dispersion relation
y = ang_THz
disp_fig, disp_ax = plt.subplots()

im = disp_ax.pcolormesh(beta.imag, y, res)
disp_fig.colorbar(im)

disp_ax.plot(spp_beta.real, y, label='SPP')
disp_ax.plot(k_light_line, y, 'k--', label='Light line')

disp_ax.plot(c_mim_beta_approx.real, y,  label='Collin\'s MIM ')
disp_ax.plot(b_mim_beta_approx.real, y,  label='Baumberg\'s MIM ')

disp_ax.plot(min_beta, y, lw=2, label='Min value')
disp_ax.plot(newt, y, lw=2, label='Newton')

disp_ax.set_xlabel(r'Propagation constant $\beta$')
disp_ax.set_ylabel(r'Energy (eV)')
# disp_ax.set_xlim([0, 10e7])
# disp_ax.set_ylim([1.0, 3.6])
disp_ax.legend(loc='lower right')

# plt.show()

# Output effective indices
# index_fig, index_ax = plt.subplots()
# wl = wl*1e9
# index_ax.plot(wl, spp_n_eff.real, label='SPP')
# index_ax.plot(wl, c_mim_n_eff.real, label='Collin\'s MIM')
# index_ax.plot(wl, b_mim_n_eff.real, label='Baumberg\'s MIM ')
# index_ax.plot(wl, min_beta/k0, label='Min value')
# index_ax.plot(wl, i_n*np.ones(len(wl)), 'k--', label='Insulator')
# index_ax.set_xlabel('Free space wavelength (nm)')
# index_ax.set_ylabel('Effective refractive index')
# index_ax.legend()
plt.show()
