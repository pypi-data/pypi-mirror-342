"""
HIDAPI C++ bindings
"""
from __future__ import annotations
import typing
__all__ = ['HidDevice', 'HidDeviceInfo', 'get_all_device_infos', 'hid_exit', 'hid_init']
class HidDevice:
    @typing.overload
    def __init__(self, vendor_id: int, product_id: int, serial_number: str, blocking: bool = True) -> None:
        ...
    @typing.overload
    def __init__(self, path: str, blocking: bool = True) -> None:
        ...
    def close(self) -> int:
        ...
    def get_error(self) -> str:
        """
        Get error string from the device
        """
    def get_feature_report(self, report_id: int, length: int) -> int:
        """
        Get feature report from the device
        """
    def get_indexed_string(self, string_index: int) -> str:
        """
        Get indexed string from the device
        """
    def get_manufacturer(self) -> str:
        """
        Get manufacturer string from the device
        """
    def get_product(self) -> str:
        """
        Get product string from the device
        """
    def get_serial_number(self) -> str:
        """
        Get serial number string from the device
        """
    def is_opened(self) -> bool:
        """
        Check if the device is opened
        """
    def open(self) -> int:
        ...
    @typing.overload
    def read(self, length: int, timeout_ms: int = 0, blocking: bool = False) -> bytes:
        ...
    @typing.overload
    def read(self, timeout_ms: int = 0, blocking: bool = False) -> bytes:
        ...
    @typing.overload
    def read(self, buffer: bytearray, timeout_ms: int = 0, blocking: bool = False) -> int:
        ...
    def send_feature_report(self, data: str, report_id: int = 0) -> int:
        """
        Send feature report to the device
        """
    def set_nonblocking(self, nonblocking: int) -> int:
        """
        Set non-blocking mode
        """
    @typing.overload
    def write(self, data: str) -> int:
        """
        Write string data to the device
        """
    @typing.overload
    def write(self, data: bytes) -> int:
        """
        Write bytes data to the device
        """
class HidDeviceInfo:
    def __init__(self) -> None:
        ...
    @property
    def interface_number(self) -> int:
        """
        USB interface which this logical device represents
        """
    @property
    def manufacturer_string(self) -> str:
        """
        Manufacturer String
        """
    @property
    def path(self) -> str:
        """
        Platform-specific device path
        """
    @property
    def product_id(self) -> int:
        """
        Device Product ID
        """
    @property
    def product_string(self) -> str:
        """
        Product String
        """
    @property
    def release_number(self) -> int:
        """
        Device Release Number in binary-coded decimal
        """
    @property
    def serial_number(self) -> str:
        """
        Serial Number
        """
    @property
    def usage(self) -> int:
        """
        Usage for this Device/Interface
        """
    @property
    def usage_page(self) -> int:
        """
        Usage Page for this Device/Interface
        """
    @property
    def vendor_id(self) -> int:
        """
        Device Vendor ID
        """
def get_all_device_infos(vendor_id: int, product_id: int) -> list[HidDeviceInfo]:
    """
    Enumerate HID devices
    """
def hid_exit() -> int:
    """
    Finalize the HIDAPI library
    """
def hid_init() -> int:
    """
    Initialize the HIDAPI library
    """
__hid_version__: str = '0.14.0'
__version__: str = '1.0.0'
