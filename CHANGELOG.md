# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [v0.3.0](https://github.com/g-duff/optical_dispersion_relations/releases/v0.3.0)

### Added

* Transcendential equations for trilayer plasmonic dispersion relations:
	* `transcendential_trilayer_even_magnetic_field`
	* `transcendential_trilayer_odd_magnetic_field`

### Changed

* BREAKING: Change DrudeLorentz default plasma frequency to 1.
* BREAKING: Change function names and parameter orders:
    * `metal_insulator_metal_collin_approximation` -> `metal_dielectric_metal_collin_approximation`
    * `metal_insulator_metal_sondergaard_narrow_approximation` -> `metal_dielectric_metal_sondergaard_narrow_approximation`

### Fixed

* DrudeLorentz doc permittivity return type.

## [v0.2.0](https://github.com/g-duff/optical_dispersion_relations/releases/v0.2.0)

### Added

* `wavelength_to_wavenumber` utility function.
* `dielectric_waveguide` module function parameter and return types.
* `DrudeLorentz` class for building Drude-Lorentz dispersion relations.

### Changed

* BREAKING: Change polarisation to lowercase in transendential slab waveguide functions:
	* `transcendential_slab_waveguide_te`
	* `transcendential_slab_waveguide_tm`

### Fixed

* `lorentz_oscillator` return type.

## [v0.1.1](https://github.com/g-duff/optical_dispersion_relations/releases/v0.1.1)

### Fixed

* Enable dielectric waveguides to handle negative numbers internally.

## [v0.1.0](https://github.com/g-duff/optical_dispersion_relations/releases/v0.1.0)

### Added

* Transcendential equation for TE and TM slab waveguides.
* Example figures and scripts under `./examples`

### Fixed

* Documentation format to match numpy.
* Documentation for:
    * `metal_insulator_metal_collin_approximation`
    * `metal_insulator_metal_sondergaard_narrow_approximation`

## [v0.0.0](https://github.com/g-duff/optical_dispersion_relations/releases/v0.0.0)

### Added

* Single pole Drude-Lorentz permittivity.
* Double pole Drude-Lorentz permittivity.
* Surface plasmon polariton dispersion relation.
* Metal-insulator-metal dispersion approximations from 
    * [Waveguiding in nanoscale metallic apertures](https://doi.org/10.1364/OE.15.004310)
    * [General properties of slow-plasmon resonant nanostructures: nano-antennas and resonators](https://doi.org/10.1364/OE.15.010869)
* Utilities:
    * permittivity to extinction coefficient.
    * permittivity to refractive index.
    * refractive index to permittivity.

### Changed

* [src-layout](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout) package directory structure.
