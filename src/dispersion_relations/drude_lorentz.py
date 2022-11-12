'''Drude Lorentz Dispersion Relations'''


def single_pole(angular_frequency,
                plasma_frequency,
                damping_rate,
                dielectric_constant=1,
                resonance_angular_frequency=0
                ):
    '''Single Pole Drude-Lorentz Dispersion Relation, for use with eg Silver

    Parameters:
        angular_frequency: the angular frequency at which to calculate the permittivity
        plasma_frequency: natural frequency of a free oscillation of the electron sea
        damping_rate: characteristic collision frequency of the metal
        dielectric_constant: offset permittivity due to positive ion cores
        resonance_angular_frequency: the Lorentz oscillator peak frequency

    Returns:
        Complex permittivity at the specified angular_frequency
    '''
    permittivity = dielectric_constant - plasma_frequency**2 * lorentz_oscillator(
        frequency=angular_frequency,
        peak_position=resonance_angular_frequency,
        damping_constant=damping_rate,
    )
    return permittivity


def lorentz_oscillator(frequency,
                       peak_position,
                       damping_constant) -> float:
    '''Lorentz Oscillator

    Parameters:
        frequency
        peak_position
        damping_constant

    Returns:
        Oscillator amplitude at the specified angular_frequency
    '''
    denominator = frequency**2 - peak_position**2 \
        + 1j*damping_constant * frequency
    return 1/denominator
