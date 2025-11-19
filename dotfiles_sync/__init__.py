"""
Dotfiles Sync - Automatic dotfiles synchronization daemon
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__description__ = "A daemon app to automatically sync dotfiles with git"

from .daemon import DotfilesSyncDaemon
from .git_manager import GitManager

__all__ = ["DotfilesSyncDaemon", "GitManager"]

