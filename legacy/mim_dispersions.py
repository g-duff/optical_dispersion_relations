import numpy as np
import cmath as cm

def spp_neff(eps_d, eps_m):
	'''Exact surface plasmon dispersion relation from [3]'''
	return np.sqrt(eps_d*eps_m/(eps_d+eps_m))


def mim_disp(beta, k_0, eps_1, eps_2, w, even_H_parity=True, full_output=False):
	'''Exact MIM dispersion relation from [3]
	Find Beta by finding the zeros of the function
	with the Newton-Raphson process'''
	k1 = cm.sqrt(beta**2-eps_1*k_0**2)
	k2 = cm.sqrt(beta**2-eps_2*k_0**2)

	if even_H_parity:
		ze = cm.tanh(k2*w/2)+k1*eps_2/(eps_1*k2)
	else:
		ze = cm.tanh(k2*w/2)+(eps_1*k2)/(k1*eps_2)
		
	if not(full_output):
		return ze
	else:
		return k1, k2
