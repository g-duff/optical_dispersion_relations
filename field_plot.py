import numpy as np
import scipy.constants as spc
from scipy.interpolate import griddata
import scipy.optimize as opt
import matplotlib
import matplotlib.pyplot as plt
import mim_dispersions as dsp
import cmath as cm

font = {'size':16}
matplotlib.rc('font', **font)

## Wavelength Insulator RI and thickness
wl = 500
i_n = 1.45
t_i = 600

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

fig, ax = plt.subplots()
ax.plot(xp, ep)
ax.plot(xm, em)
# plt.show()

# Newton-Raphson process, decreasing gap thickness
beta = opt.newton(dsp.mim_disp, spp_beta, args=(k0, m_eps, i_eps, t_i),
	maxiter=int(1e6), tol=1e3)
n_eff =  beta.real/k0

# Calculate MIM field
k2, k1 =  dsp.mim_disp(beta, k0, m_eps, i_eps, t_i, full_output=True)

x1 = np.arange(t_i/2, 3*t_i)
x2 = np.arange(-t_i/2, t_i/2)
x3 = np.arange(-3*t_i, -t_i/2)

e1 = (np.exp(k1*(t_i/2)) + np.exp(-1*k1*(t_i/2)))*np.exp(-k2*(x1-t_i/2))
e2 = np.exp(k1*(x2)) + np.exp(-1*k1*(x2))
e3 = (np.exp(k1*(-t_i/2)) + np.exp(-1*k1*(-t_i/2)))*np.exp(k2*(x3+t_i/2))

mim_x = np.concatenate([x1, x2, x3])
mim_y = np.concatenate([e1, e2, e3])

# fig, ax = plt.subplots()
ax.plot(mim_x, mim_y.real, '.', ms=1)
ax.plot(mim_x, mim_y.imag, '.', ms=1)
plt.show()
