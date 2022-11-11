'''Drude Lorentz Dispersion Relations'''


def lorentz_oscillator(angular_frequency,
                       resonance_angular_frequency,
                       damping_rate,
                       oscillator_amplitude=1) -> float:
    '''Lorentz Oscillator

    Parameters:
        angular_frequency
        resonance_angular_frequency
        damping_rate
        oscillator_amplitude

    Returns:
        Oscillator amplitude at the specified angular_frequency
    '''
    denominator = angular_frequency**2 - resonance_angular_frequency**2 \
        + 1j*damping_rate * angular_frequency
    return oscillator_amplitude/denominator
