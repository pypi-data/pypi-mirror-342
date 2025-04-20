import openvino  # noqa
from ._core import load_and_compile_model

__all__ = ["get_available_devices", "load_and_compile_model"]
