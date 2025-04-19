"""
Jimiko - High-performance SSH client for network automation and device management
"""

import os
import platform
import sys
from pathlib import Path


def _get_linux_distribution(os_name):
    """Detect the Linux distribution by checking for distribution-specific files."""
    if os_name == 'darwin':
        return 'macos'
    elif os_name == 'linux':
        if os.path.exists('/etc/redhat-release'):
            return 'rhel'  
        elif os.path.exists('/etc/debian_version') or os.path.exists('/etc/lsb-release'):
            return 'linux' 
    return None 

def _load_binary(wrapper_name):
    # For Windows, add the module's directory to PATH temporarily to find binaries 
    original_path = None
    if platform.system().lower() == 'windows':
        original_path = os.environ.get('PATH', '')
        module_dir = str(Path(__file__).parent.absolute())
        os.environ['PATH'] = module_dir + os.pathsep + original_path
    
    # Try direct import first
    try:
        if wrapper_name == '_jimiko_wrapper':
            from ._jimiko_wrapper import PyJimikoClient
            return PyJimikoClient
        elif wrapper_name == '_jimikosftp_wrapper':
            from ._jimikosftp_wrapper import PyJimikoSFTPClient, PyFileInfo
            return PyJimikoSFTPClient, PyFileInfo
    except ImportError as e:
        # If direct import fails, try to load from the package directory
        package_dir = Path(__file__).parent
        os_name = platform.system().lower()
        machine = platform.machine().lower()
        python_version = f"{sys.version_info.major}{sys.version_info.minor}"  
        linux_distro = _get_linux_distribution(os_name)
        
        # If package directory doesn't exist, we can't load from there
        if not linux_distro:
            raise ImportError(f"No compatible binary found for OS: {os_name} Linux Distro: {linux_distro} Machine: {machine} (Python {python_version}). Original error: {e}")
        if not package_dir.exists():
            raise ImportError(f"Failed to import {wrapper_name} directly and no binary directory found. Original error: {e}")
            
        binary_pattern = None
        if linux_distro == 'rhel':
            binary_pattern = f'{wrapper_name}.cp*-{python_version}-manylinux*.so'
        elif linux_distro == 'linux':
            binary_pattern = f'{wrapper_name}.cp*-{python_version}-linux.so'
        elif linux_distro == 'macos':
            binary_pattern = f'{wrapper_name}.cp*-{python_version}-darwin.so'
        elif os_name == 'windows':
            binary_pattern = f'{wrapper_name}.cp*-{python_version}-win*.pyd'
            
        if binary_pattern:
            binaries = list(package_dir.glob(binary_pattern))
            if binaries:
                # Use the first matching binary
                binary_path = binaries[0]
                import importlib.util
                spec = importlib.util.spec_from_file_location(wrapper_name, binary_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if wrapper_name == '_jimiko_wrapper':
                    return module.PyJimikoClient
                elif wrapper_name == '_jimikosftp_wrapper':
                    return module.PyJimikoSFTPClient, module.PyFileInfo
                
        raise ImportError(f"No compatible binary found for OS: {os_name} Linux Distro: {linux_distro} Machine: {machine} (Python {python_version}). Original error: {e}")
    finally:
        # Restore original PATH if we modified it
        if original_path is not None:
            os.environ['PATH'] = original_path

PyJimikoClient = _load_binary('_jimiko_wrapper')
PyJimikoSFTPClient, PyFileInfo = _load_binary('_jimikosftp_wrapper')