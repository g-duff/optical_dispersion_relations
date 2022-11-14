import numpy as np
import scipy.constants as spc
from scipy.interpolate import griddata
import scipy.optimize as opt
import matplotlib
import matplotlib.pyplot as plt
import mim_dispersions as dsp
import cmath as cm
import numpy.linalg as la

font = {'size':16}
matplotlib.rc('font', **font)

## Wavelength Insulator RI and thickness
wl = 750
i_n = 1.45
t_i = 20

## Metal refractive index and extinction coefficient
m_wl, m_n, = np.genfromtxt('./material_dispersions/ag_n.txt',
	unpack=True, skip_header=1)
m_k = np.genfromtxt('./material_dispersions/ag_k.txt',
	unpack=True, skip_header=1, usecols=(1))

# Convert units
m_wl = m_wl*1e3	# um to m
wl = wl		# nm to m

## Calculate wavevector, frequency, energy
k0 = 2*np.pi/wl

## Interpolate metal n and k to match user wavelength range
m_n = griddata(m_wl, m_n, wl, method='cubic')
m_k = griddata(m_wl, m_k, wl, method='cubic')

## Convert RI to permittivity
m_eps = (m_n + 1j*m_k)**2
i_eps = i_n**2

# m_eps, i_eps = i_eps, m_eps

## Calcualte spp neff
spp_n_eff = dsp.spp_neff(i_eps, m_eps)
spp_beta = spp_n_eff*k0

# Calculate SPP field
k1 = cm.sqrt(spp_beta**2 - k0**2*i_eps)
k2 = cm.sqrt(spp_beta**2 - k0**2*m_eps)
xp = np.arange(-t_i/2, t_i/2)
xm = np.arange(-3*t_i, -t_i/2,)
ep = np.exp(-k1*(xp+t_i/2))*(np.exp(k1*(t_i/2)) + np.exp(-1*k1*(t_i/2)))
em = np.exp(k2*(xm+t_i/2))*(np.exp(k1*(t_i/2)) + np.exp(-1*k1*(t_i/2)))

# Newton-Raphson process, decreasing gap thickness
beta = opt.newton(dsp.mim_disp, spp_beta, args=(k0, m_eps, i_eps, t_i, False),
	maxiter=int(1e6), tol=1e-20)
n_eff =  beta.real/k0

# Calculate MIM field
k1, k2 =  dsp.mim_disp(beta, k0, m_eps, i_eps, t_i, False, full_output=True)

# Find the boundary conditions
A = 1
[C, D] = la.inv(np.array([
	[np.exp(k2*t_i/2), np.exp(-1*k2*t_i/2)],
	[-1j*k2*np.exp(k2*t_i/2)/i_eps, 1j*k2*np.exp(-k2*t_i/2)/i_eps]
])) @ np.array([np.exp(-k1*t_i/2), 1j*k1*np.exp(-k1*t_i/2)/m_eps])
B = (C*np.exp(-k2*t_i/2) + D*np.exp(k2*t_i/2))/np.exp(-k1*t_i/2)

x1_coords = np.arange(t_i/2, 3*t_i)
x2_coords = np.arange(-t_i/2, t_i/2)
x3_coords = np.arange(-3*t_i, -t_i/2)
z_coords = np.arange(0, 3000, 30)
z1_grid, x1_grid = np.meshgrid(z_coords, x1_coords)
z2_grid, x2_grid = np.meshgrid(z_coords, x2_coords)
z3_grid, x3_grid = np.meshgrid(z_coords, x3_coords)

# Calculate the fields, as in Maier
e1 = (A*np.exp(-k1*x1_grid))*np.exp(-1j*beta*z1_grid)
e2 = (C*np.exp(k2*x2_grid) + D*np.exp(-1*k2*x2_grid))*np.exp(-1j*beta*z2_grid)
e3 = (B*np.exp(k1*x3_grid))*np.exp(-1j*beta*z3_grid)

x_coords = np.concatenate([x3_coords, x2_coords, x1_coords])
mim_y = np.concatenate([e3, e2, e1])

fig, ax = plt.subplots()
cb = ax.pcolormesh(z_coords, x_coords, mim_y.real)
fig.colorbar(cb)
plt.show()

# Calculate SPP field
# k1 = cm.sqrt(spp_beta**2 - k0**2*i_eps)
# k2 = cm.sqrt(spp_beta**2 - k0**2*m_eps)
# xp = np.arange(-t_i/2, t_i/2)
# xm = np.arange(-3*t_i, -t_i/2,)
# ep = np.exp(-k1*(xp+t_i/2))*(np.exp(k1*(t_i/2)) + np.exp(-1*k1*(t_i/2)))
# em = np.exp(k2*(xm+t_i/2))*(np.exp(k1*(t_i/2)) + np.exp(-1*k1*(t_i/2)))

# fig, ax = plt.subplots()
# ax.plot(xp, ep)
# ax.plot(xm, em)

# plt.show()