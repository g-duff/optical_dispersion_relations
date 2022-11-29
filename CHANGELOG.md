# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

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
