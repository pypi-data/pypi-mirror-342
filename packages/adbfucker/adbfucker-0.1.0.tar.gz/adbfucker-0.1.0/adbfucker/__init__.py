"""
ADBFucker - Tool for Android ADB automation with image recognition

This module provides classes and functions for automating Android device interactions
through ADB with image recognition capabilities.
"""

__version__ = '0.1.0'

from .core import (
    # Classes
    Logger, ADBCommand, ImageProcessor, DeviceHelper, AppManager, NetworkHelper,
    
    # Utility functions
    exists, touch, wait, home, back, keyevent, shell, swipe, text, paste, screenshot,
    start_app, stop_app, clear_app, install_app, uninstall_app, clear_recent_apps,
    clear_recent_apps_and_change_ip, notifications_open, notifications_close,
    notifications_clear, toggle_airplane_mode, change_ip_address, reboot, message,
    
    # Color constants
    COLORS
) 