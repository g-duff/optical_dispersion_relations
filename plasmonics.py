import numpy as np
import cmath as cm
import scipy.optimize as opt
# import scipy.special as sps

def spp_neff(eps_d, eps_m):
	'''Exact surface plasmon dispersion relation from [3]'''
	return np.sqrt(eps_d*eps_m/(eps_d+eps_m))

def mim_neff_collin(eps_d, eps_m, wav, ti):
	'''MIM eff index approximation by Collin, from [1]'''
 	n_eff=np.sqrt(eps_d)*np.sqrt(1+wav/(np.pi*ti*np.sqrt(-1*eps_m))*
		np.sqrt(1-eps_d/eps_m))
	return n_eff

def mim_neff_sondergaard(eps_d, eps_m, wav, ti):
	'''MIM eff index approximation by Sondergaard, from [2]'''
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
