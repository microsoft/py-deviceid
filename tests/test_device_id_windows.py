import os
import platform
import pytest
from pathlib import Path
from unittest.mock import patch

if platform.system() != "Windows" :
    pytest.skip("Linux and MacOS Only", allow_module_level=True)


import winreg

from deviceid import get_device_id

REGISTRY_PATH = r'SOFTWARE\Microsoft\DeveloperTools'
REGISTRY_KEY = 'deviceid'

def test_get_device_id():
    device_id = get_device_id()
    assert device_id
    assert isinstance(device_id, str)
    assert len(device_id) == 36

def test_get_devide_id_confirm_location():
    # create the id if not present already
    device_id = get_device_id()

    with winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, reserved=0, access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY ) as key_handle:
        manual_device_id = winreg.QueryValueEx(key_handle, REGISTRY_KEY)[0]
    
    assert device_id == manual_device_id


def test_get_device_id_permission_error():
    
    device_id = get_device_id()
    
    with patch("winreg.OpenKeyEx", side_effect=PermissionError):
        device_id = get_device_id()
        assert device_id == ""

def test_get_device_id_permission_general_error():
    
    device_id = get_device_id()
    
    with patch("winreg.OpenKeyEx", side_effect=PermissionError):
        device_id = get_device_id()
        assert device_id == ""
