"""Constants used throughout the application."""

import os

# Version
VERSION = '0.5.3'

# File paths and directories
DEFAULT_CONFIG = 'termis.yml'
GLOBAL_PROFILES_DIR = os.path.expanduser('~/.termis/profiles')
ERROR_LOG_PATH = os.path.expanduser('~/.termis/error.log')

# Badge themes with their colors
BADGE_THEMES = {
    'default': {'fg': (213, 194, 194), 'bg': None},
    'success': {'fg': (76, 175, 80), 'bg': None},
    'error': {'fg': (244, 67, 54), 'bg': None},
    'warning': {'fg': (255, 193, 7), 'bg': None},
    'info': {'fg': (33, 150, 243), 'bg': None},
    'primary': {'fg': (156, 39, 176), 'bg': None},
    'secondary': {'fg': (96, 125, 139), 'bg': None},
    'dark': {'fg': (33, 33, 33), 'bg': None},
    'light': {'fg': (227, 227, 227), 'bg': None},
}

# Repository URL
REPO_URL = 'https://github.com/smithg09/termis'
