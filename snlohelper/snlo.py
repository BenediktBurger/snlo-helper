import logging

from . import utils

from .main_window import open_function, Functions  # noqa: F401
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
