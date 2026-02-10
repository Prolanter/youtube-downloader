#!/usr/bin/env python3
"""
YouTube Downloader Desktop Application
Main entry point for the application
"""

import sys
import os
from pathlib import Path
from gui import YouTubeDownloaderApp
from PyQt5.QtWidgets import QApplication


def main():
    """Start the desktop application"""
    app = QApplication(sys.argv)
    
    # Set application name and icon
    app.setApplicationName("YouTube Downloader")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = YouTubeDownloaderApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
