# [Optical Dispersion Relations](https://github.com/g-duff/optical_dispersion_relations)

## Features

* A collection of exact and approximate optical dispersion relations.
* Academic Sources eg textbooks and journal articles.
* Fully tested (see `test/`) so users can calculate with confidence.

## Examples

* Silver permittivity can be calculated with a Single Pole Drude-Lorentz model:

```py
silver_drude_parameters = {
	'dielectric_constant': 1,
	'plasma_frequency': 1.35e16,
	'damping_constant': 0.0023*1.35e16,
}

silver_permittivity = drude_lorentz.single_pole(
	angular_frequency, **silver_drude_parameters)
```

* Gold permittivity can be calculated with a Double Pole Drude-Lorentz model:

```py
gold_drude_parameters = {
	'dielectric_constant': 6,
	'plasma_frequency': 1,
	'first_pole': {
		'peak_strength': 5.37e15**2,
		'damping_constant': 6.216e13,
		'peak_position': 0,
	},
	'second_pole': {
		'peak_strength': 2.263e15**2,
		'damping_constant': 1.332e15,
		'peak_position': 4.572e15
	}
}

gold_permittivity = drude_lorentz.double_pole(
	angular_frequency, **gold_drude_parameters)
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
