# SNLO-Helper

[![pypi release](https://img.shields.io/pypi/v/snlo-helper.svg)](https://pypi.org/project/snlo-helper/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11125163.svg)](https://doi.org/10.5281/zenodo.11125163)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)

SNLO-Helper helps to use [SNLO](https://as-photonics.com/products/snlo/) software for simulation of nonlinear optical processes in crystals.

An autoclicker clicks different buttons and fills fields in order to automate SNLO simulations.
Afterwards, it can retrieve the results and return them as a dictionary.

Attention:
- The script does use your mouse and keyboard, so you should not interact with the computer at the same time.
- The script uses predefined positions of the windows, so **do not move the windows**.
- The autoclicker can be interrupted by moving the mouse into the top left corner of the screen.


Currently it supports the following functions (feel free to add more):
- Ref. Ind.
- Qmix
- 2D-mix-LP
- 2D-mix-SP
- PW-OPO-BB
- Focus


## Installation

Install it executing `pip install -e .` in this folder or via `pip install snlo-helper` to download it in the background and install it.


## Usage

### Quick Start

1. Start SNLO on your computer
2. Import `snlohelper.main_window.MainWindow` as a starting point.
3. Create an instande `mw = MainWindow`
4. Open the desired function: `ri = mw.open_function(Functions.REF_INDEX)`
5. Execute it `no, ne = ri.refractive_indices(Wavelength=1234)`

Here is a small snippet how to do a 2D mix of long pulses:
```
from snlohelper.main_window import MainWindow

mw = MainWindow()
mix = mw.open_two_d_mix_lp()
mix.configure({"Wavelengths (nm)": [1064.5, None, None]})
result = mix.run_and_read()
print(result)
```

For more examples see the `examples` folder.


### General usage

* The `main_window.MainWindow` class manages the main window.
* For several functions exists a module containing a class, which in turn allows to configure the function, to run the calculation, and to extract the result.
  1. You start that class, for example `mix = two_d_mix_lp.TwoDMixLp()` or `mix = MainWindow().open_function("2D-Mix-LP")`.
  2. You can configure it giving a configuration dictionary (the keys correspond to the names) with `mix.configure({"Wavelengths": [1064, None, None]})`. If a value is `None`, it won't be changed.
  3. You can run it with `mix.run()`
  4. With `results = mix.read_results()` you can extract the resulting text.
  5. With `result_dict = mix.interpret_results(results)` you get a dictionary of the result data
  6. There are convenience methods like `mix.run_and_read` which runs and returns the dictionary, or even `mix.configure_run_read`, which does all of above steps in one.


## Contribution

You are welcome to contribute to this library.
Just open an issue for suggestions or bug reports and open a pull request for code contributions.
