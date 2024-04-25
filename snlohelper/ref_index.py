from typing import Any

from .base_function import BaseFunction, Functions


class RefractiveIndex(BaseFunction):
    _function = Functions.REF_INDEX
    _run_pos = (295, 187)
    _result_pos = (160, 260)
    _close_pos = (365, 41)
    _configuration_pos = {
        "Crystal": [(170, 90)],
        "Temperature": [(290, 90)],
        "theta": [(170, 146)],
        "phi": [(300, 146)],
        "Wavelength": [(170, 190)],
    }

    def run_and_read(
        self,
        waiting_time: float = 0.1,
        max_tries: int = 10,
        interval: float = 0.1,
        waiting_line_count: int = 3,
    ) -> dict[str, Any]:
        return super().run_and_read(waiting_time, max_tries, interval, waiting_line_count)

    def refractive_indices(
        self, Crystal=None, Temperature=None, theta=None, phi=None, Wavelength=None
    ) -> list[float]:
        kwargs = {
            "Crystal": Crystal,
            "Temperature": Temperature,
            "theta": theta,
            "phi": phi,
            "Wavelength": Wavelength,
        }
        results = self.configure_run_read(kwargs)
        return results["Refractive index (o,e)"]
