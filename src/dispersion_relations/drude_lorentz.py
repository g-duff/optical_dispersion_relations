'''Drude Lorentz Dispersion Relations'''


def single_pole(angular_frequency: float,
                plasma_frequency: float,
                damping_constant: float,
                dielectric_constant: float = 1,
                peak_position: float = 0
                ) -> complex:
    '''Single Pole Drude-Lorentz Dispersion Relation, for use with eg Silver

    Parameters:
        angular_frequency: the angular frequency at which to calculate the permittivity
        plasma_frequency: natural frequency of a free oscillation of the electron sea
        damping_rate: characteristic collision frequency of the metal
        dielectric_constant: offset permittivity due to positive ion cores
        peak_position: the Lorentz oscillator peak position

    Returns:
        Complex permittivity at the specified angular_frequency
    '''
    permittivity = dielectric_constant - plasma_frequency**2 * lorentz_oscillator(
        frequency=angular_frequency,
        peak_position=peak_position,
        damping_constant=damping_constant,
    )
    return permittivity


def double_pole(angular_frequency: float,
                plasma_frequency: float,
                dielectric_constant: float,
                first_pole: dict,
                second_pole: dict
                ) -> complex:
    '''Double Pole Drude-Lorentz Dispersion Relation, for use with eg Gold

    Parameters:
        angular_frequency: the angular frequency at which to calculate the permittivity
        plasma_frequency: natural frequency of a free oscillation of the electron sea
        dielectric_constant: offset permittivity due to positive ion cores
        first_pole, second_pole: dictionaries containing:
            peak_strength: the relative strength of the peaks
            damping_rate: characteristic collision frequency of the metal
            peak_position: the Lorentz oscillator peak position

    Returns:
        Complex permittivity at the specified angular_frequency
    '''
    permittivity = dielectric_constant * plasma_frequency**2 * (
        1
        - first_pole['peak_strength']*lorentz_oscillator(
            frequency=angular_frequency,
            peak_position=first_pole['peak_position'],
            damping_constant=first_pole['damping_constant'],
        )
        - second_pole['peak_strength']*lorentz_oscillator(
            frequency=angular_frequency,
            peak_position=second_pole['peak_position'],
            damping_constant=second_pole['damping_constant'],
        )
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
