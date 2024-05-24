# MIT License

# Copyright (c) 2024 Benedikt Burger

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging

from . import utils

from .main_window import open_function, Functions  # noqa: F401
from .ref_index import RefractiveIndex  # noqa: F401
from .two_d_mix_lp import TwoDMixLP  # noqa: F401
from .two_d_mix_sp import TwoDMixSP  # noqa: F401
from .focus import focus  # noqa: F401

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def main() -> None:
    """Initialize the SNLO helper."""
    if len(log.handlers) < 2:
        log.addHandler(logging.StreamHandler())
    log.setLevel(logging.INFO)
    utils.set_screenfactors()
    log.info(f"Setting screenfactors to {utils.factors}.")


if __name__ == "__main__":  # pragma: nocover
    main()
