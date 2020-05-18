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
wl = 500
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

# fig, ax = plt.subplots()
# ax.plot(xp, ep)
# ax.plot(xm, em)
# plt.show()

# Newton-Raphson process, decreasing gap thickness
beta = opt.newton(dsp.mim_disp, spp_beta, args=(k0, m_eps, i_eps, t_i, True),
	maxiter=int(1e6), tol=1e-30)
n_eff =  beta.real/k0

# Calculate MIM field
k1, k2 =  dsp.mim_disp(beta, k0, m_eps, i_eps, t_i, True, full_output=True)

x1 = np.arange(t_i/2, 3*t_i)
x2 = np.arange(-t_i/2, t_i/2)
x3 = np.arange(-3*t_i, -t_i/2)

# Find the boundary conditions
A = 1
[C, D] = la.inv(np.array([
	[np.exp(k2*t_i/2), np.exp(-1*k2*t_i/2)],
	[-1j*k2*np.exp(k2*t_i/2)/i_eps, 1j*k2*np.exp(-k2*t_i/2)/i_eps]
])) @ np.array([np.exp(-k1*t_i/2), 1j*k1*np.exp(-k1*t_i/2)/m_eps])
B = (C*np.exp(-k2*t_i/2) + D*np.exp(k2*t_i/2))/np.exp(-k1*t_i/2)

# Calculate the fields, as in Maier
e1 = A*np.exp(-k1*x1)
e2 = C*np.exp(k2*x2) + D*np.exp(-1*k2*x2)
e3 = B*np.exp(k1*x3)

mim_x = np.concatenate([x1, x2, x3])
mim_y = np.concatenate([e1, e2, e3])

fig, ax = plt.subplots()
ax.plot(mim_x, mim_y.real, 'C3.', ms=3)
ax.plot(mim_x, mim_y.imag, 'k.', ms=3)
plt.show()
