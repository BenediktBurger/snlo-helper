# SNLO-Helper

SNLO-Helper helps to use [SNLO](https://as-photonics.com/products/snlo/) software for simulation of nonlinear optical processes in crystals.

An autoclicker clicks different buttons and fills fields in order to automate SNLO simulations.
Afterwards, it can retrieve the results and return them as a dictionary.

Note that the script does use your mouse and keyboard, so you should not interact with the computer at the same time.
The autoclicker can be interrupted by moving the mouse into the top right corner of the screen.


## Installation

Install it executing `pip install -e .` in this folder or via `pip install git+https://git.rwth-aachen.de/nloqo/snlo-helper.git` to download it in the background and install it.


## Usage

Import `snlohelper.snlo` as a starting point.
If your screen resolution differs from HD, you have to set screenfactors with `utils.set_screenfactors`.
That will rescale all positions to your current screen resolution.

Here is a small snippet how to do a 2D mix of long pulses:
```
from snlohelper import snlo

snlo.utils.set_screenfactors()

sim = snlo.TwoDMixLP()  # create a class for 2D mix
sim.open()  # click the corresponding button to open 2D mix
sim.configure({"Wavelengths (nm)": [1064.5, None, None]})  # configure it
result = sim.run_and_read()  # run it
print(result)
```

For more examples see the `examples` folder.


## Contribution

You are welcome to contribute to this library. Just open an issue for suggestions or bug reports and open a pull request for code contributions.
