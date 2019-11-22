#!/usr/bin/python3
import matplotlib       # For remote use
## matplotlib.use('Agg')   # For remote use
import matplotlib.pyplot as plt
import numpy as np
from cmath import sqrt

def spp_n_eff(eps_d, eps_m):
    n_eff = sqrt(eps_d*eps_m/(eps_d+eps_m))
    return n_eff

def coupled_spp_n_eff(wav, t_i, eps_d, eps_m):
    n_eff=sqrt(eps_d)*sqrt(1+wav/(np.pi*t_i*sqrt(-1*eps_m))*sqrt(1-eps_d/eps_m))
    return n_eff

## Au_n = np.loadtxt('Au_n.txt')
## Au_k = np.loadtxt('Au_k.txt')
## SiO_n  = np.loadtxt('SiO_n.txt')
##
## Au_n = np.interp(wavs, Au_n[:,0], Au_n[:,1])
## Au_k = np.interp(wavs, Au_k[:,0], Au_k[:,1])
## SiO_n = np.interp(wavs, SiO_n[:,0], SiO_n[:,1])
##
## Au_eps = (np.add(Au_n, 1j*Au_k))**2
## eps_d = SiO_n**2

t_i = np.logspace(-2, 1, 1000)
single_n_eff = [spp_n_eff(1, -50).real for t in t_i]
coupled_n_eff = [coupled_spp_n_eff(1, t, 1, -50).real for t in t_i]

fig, ax = plt.subplots()

ax.semilogx(t_i, coupled_n_eff, label='Coupled SPP approximation')
ax.plot(t_i, single_n_eff, '--', color='k', label='Single SPP')
ax.set_ylim(0, 3.0)
ax.set_xlim(0.01, 10)
ax.set_ylabel('Effective index (real part)')
ax.set_xlabel('Normalised insulator thickness ($t_i/\lambda$)')
ax.legend(loc='best')
plt.show()

# fig.savefig('Plasmon_diagram.png')
