"""
Cross-platform system utilities for Athena AI Assistant
"""

import os
import platform
import subprocess
import shutil
from pathlib import Path

class SystemManager:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.is_windows = self.os_type == 'windows'
        self.is_mac = self.os_type == 'darwin'
        self.is_linux = self.os_type == 'linux'
    
    def get_user_directories(self):
        """Get user directories in a cross-platform way"""
        home = Path.home()
        
        directories = {
            'home': home,
            'documents': home / 'Documents',
            'downloads': home / 'Downloads',
            'pictures': home / 'Pictures',
            'music': home / 'Music',
            'videos': home / 'Videos',
            'desktop': home / 'Desktop'
        }
        
        # Windows-specific adjustments
        if self.is_windows:
            try:
                import winreg
                # Try to get actual Windows folders
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                  r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
                    try:
                        directories['documents'] = Path(winreg.QueryValueEx(key, "Personal")[0])
                        directories['downloads'] = Path(winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0])
                        directories['pictures'] = Path(winreg.QueryValueEx(key, "My Pictures")[0])
                        directories['music'] = Path(winreg.QueryValueEx(key, "My Music")[0])
                        directories['videos'] = Path(winreg.QueryValueEx(key, "My Video")[0])
                        directories['desktop'] = Path(winreg.QueryValueEx(key, "Desktop")[0])
                    except FileNotFoundError:
                        pass  # Use default paths
            except ImportError:
                pass  # Use default paths
        
        return directories
    
    def open_file_or_folder(self, path):
        """Open file or folder in default application"""
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        
        try:
            if self.is_windows:
                os.startfile(str(path))
            elif self.is_mac:
                subprocess.run(['open', str(path)], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', str(path)], check=True)
        except Exception as e:
            raise RuntimeError(f"Failed to open {path}: {e}")
    
    def get_system_info(self):
        """Get detailed system information"""
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'hostname': platform.node(),
            'user': os.getenv('USER') or os.getenv('USERNAME'),
            'home_directory': str(Path.home())
        }
    
    def create_directory_structure(self, base_path, structure):
        """
        Create directory structure
        
        Args:
            base_path: Base directory path
            structure: List of subdirectories to create
        """
        base = Path(base_path)
        base.mkdir(parents=True, exist_ok=True)
        
        for subdir in structure:
            (base / subdir).mkdir(parents=True, exist_ok=True)
    
    def get_available_space(self, path=None):
        """Get available disk space"""
        if path is None:
            path = Path.home()
        
        try:
            if self.is_windows:
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(str(path)),
                    ctypes.pointer(free_bytes),
                    None,
                    None
                )
                return free_bytes.value
            else:
                statvfs = os.statvfs(str(path))
                return statvfs.f_frsize * statvfs.f_bavail
        except Exception:
            return None
    
    def is_admin(self):
        """Check if running with administrator/root privileges"""
        try:
            if self.is_windows:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except Exception:
            return False

# Global system manager instance
system_manager = SystemManager()