import os
import platform
from pathlib import Path
from unittest.mock import patch

import pytest
from deviceid import get_device_id

if platform.system() not in ('Linux', 'Darwin') :
    pytest.skip("Linux and MacOS Only", allow_module_level=True)

def test_get_device_id():
    device_id = get_device_id()
    assert device_id
    assert isinstance(device_id, str)
    assert len(device_id) == 36

def test_get_devide_id_confirm_location():
    # create the id if not present already
    device_id = get_device_id()

    # lets get the id ourselves
    if platform.system() == 'Linux':
        file_path = Path(os.getenv('XDG_CACHE_HOME', f"{os.getenv('HOME')}/.cache")).joinpath('Microsoft/DeveloperTools/deviceid')
    elif platform.system() == 'Darwin':
        file_path = Path(f'{os.getenv("HOME")}/Library/Application Support/Microsoft/DeveloperTools/deviceid')
    
    manual_device_id = file_path.read_text(encoding='utf-8')

    assert device_id == manual_device_id

def test_get_device_id_empty_home_locations():
    
    # lets remove the HOME
    if platform.system() == 'Linux':
        os.environ['XDG_CACHE_HOME'] = ''
        os.environ['HOME'] = ''
    elif platform.system() == 'Darwin':
        os.environ['HOME'] = ''

    
    device_id = get_device_id()
    assert device_id == ""

def test_get_device_id_permission_error():
    
    device_id = get_device_id()
    
    with patch.object(Path, 'touch', side_effect=PermissionError):
        device_id = get_device_id()
        assert device_id == ""

def test_get_device_id_permission_general_error():
    
    device_id = get_device_id()
    
    with patch.object(Path, 'touch', side_effect=Exception):
        device_id = get_device_id()
        assert device_id == ""