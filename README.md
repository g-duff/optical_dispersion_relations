# [Optical Dispersion Relations](https://github.com/g-duff/optical_dispersion_relations)

## Features

* A collection of exact and approximate optical dispersion relations.
* Academic Sources eg textbooks and journal articles.
* Fully tested (see `test/`) so users can calculate with confidence.

## Examples

* Silver permittivity can be calculated with a Single Pole Drude-Lorentz model:

```py
silver_dispersion = drude_lorentz.DrudeLorentz().with_angular_frequency(
	angular_frequency
).with_plasma_frequency(1.35e16).add_pole(
	damping_constant=0.0023*1.35e16
)

silver_permittivity = silver_dispersion.permittivity()
```

* Gold permittivity can be calculated with a Double Pole Drude-Lorentz model:

```py
gold_dispersion = drude_lorentz.DrudeLorentz().with_dielectric_constant(
	6
).with_angular_frequency(angular_frequency).add_pole(
        peak_strength=6*5.37e15**2,
        damping_constant=6.216e13,
).add_pole(
        peak_strength=6*2.263e15**2,
        damping_constant=1.332e15,
        peak_position=4.572e15
)

gold_permittivity = gold_dispersion.permittivity()
```

* More examples can be found under `/examples/`.

## Install

[Install with pip](https://pypi.org/project/optical-dispersion-relations/) eg:

```sh
pip3 install optical_dispersion_relations
```

Download the latest release [here](https://github.com/g-duff/optical_dispersion_relations/releases/latest), or previous releases [here](https://github.com/g-duff/optical_dispersion_relations/releases).

## Contribute

Contributions and conversations warmly welcome.
