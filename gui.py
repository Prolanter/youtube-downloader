#!/usr/bin/env python3
"""
PyQt5 GUI for YouTube Downloader
"""

import os
import threading
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QProgressBar, QTextEdit, QFileDialog, QCheckBox,
    QGroupBox, QRadioButton, QButtonGroup, QMessageBox,
    QSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QIcon, QPixmap
from downloader import YouTubeDownloader


class DownloadSignals(QObject):
    """Signals for download progress"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)


class YouTubeDownloaderApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.downloader = None
        self.signals = DownloadSignals()
        self.download_thread = None
        self.is_downloading = False
        
        # Connect signals
        self.signals.progress.connect(self.update_progress)
        self.signals.status.connect(self.update_status)
        self.signals.finished.connect(self.download_finished)
        self.signals.error.connect(self.show_error)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 900, 700)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("YouTube Video Downloader")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # URL Input Section
        url_group = QGroupBox("Video URL")
        url_layout = QVBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL or Playlist URL...")
        self.url_input.setMinimumHeight(35)
        url_layout.addWidget(self.url_input)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)
        
        # Download Options Section
        options_group = QGroupBox("Download Options")
        options_layout = QVBoxLayout()
        
        # Download type selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Download Type:")
        type_layout.addWidget(type_label)
        
        self.download_type = QButtonGroup()
        self.video_radio = QRadioButton("Video (Highest Quality)")
        self.audio_radio = QRadioButton("Audio Only (MP3)")
        self.video_radio.setChecked(True)
        self.download_type.addButton(self.video_radio, 0)
        self.download_type.addButton(self.audio_radio, 1)
        type_layout.addWidget(self.video_radio)
        type_layout.addWidget(self.audio_radio)
        type_layout.addStretch()
        options_layout.addLayout(type_layout)
        
        # Playlist option
        playlist_layout = QHBoxLayout()
        self.playlist_checkbox = QCheckBox("Download as Playlist")
        playlist_layout.addWidget(self.playlist_checkbox)
        playlist_layout.addStretch()
        options_layout.addLayout(playlist_layout)
        
        # Quality selection
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Video Quality:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "Best (Highest Quality)",
            "1080p",
            "720p",
            "480p",
            "360p",
            "240p"
        ])
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        options_layout.addLayout(quality_layout)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Output Directory Section
        output_group = QGroupBox("Output Directory")
        output_layout = QHBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setText(str(Path.home() / "Downloads" / "YouTube"))
        self.output_path.setReadOnly(True)
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setMaximumWidth(100)
        self.browse_btn.clicked.connect(self.browse_folder)
        output_layout.addWidget(QLabel("Save to:"))
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(self.browse_btn)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Progress Section
        progress_group = QGroupBox("Download Progress")
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # Status/Log Section
        log_group = QGroupBox("Status Log")
        log_layout = QVBoxLayout()
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        self.status_log.setMinimumHeight(150)
        log_layout.addWidget(self.status_log)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # Buttons Section
        button_layout = QHBoxLayout()
        self.download_btn = QPushButton("Download")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.setMinimumWidth(150)
        self.download_btn.clicked.connect(self.start_download)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
            QPushButton:pressed {
                background-color: #990000;
            }
        """)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.setMinimumWidth(100)
        self.clear_btn.clicked.connect(self.clear_fields)
        
        button_layout.addStretch()
        button_layout.addWidget(self.download_btn)
        button_layout.addWidget(self.clear_btn)
        layout.addLayout(button_layout)
        
        layout.addStretch()
    
    def browse_folder(self):
        """Open folder selection dialog"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Output Folder",
            str(Path.home() / "Downloads")
        )
        if folder:
            self.output_path.setText(folder)
    
    def clear_fields(self):
        """Clear input fields"""
        self.url_input.clear()
        self.status_log.clear()
        self.progress_bar.setValue(0)
        self.video_radio.setChecked(True)
        self.playlist_checkbox.setChecked(False)
    
    def start_download(self):
        """Start the download process"""
        url = self.url_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL!")
            return
        
        if self.is_downloading:
            QMessageBox.warning(self, "Warning", "Download already in progress!")
            return
        
        # Disable button during download
        self.is_downloading = True
        self.download_btn.setEnabled(False)
        self.download_btn.setText("Downloading...")
        self.progress_bar.setValue(0)
        self.status_log.clear()
        
        # Start download in separate thread
        self.download_thread = threading.Thread(
            target=self.download_worker,
            args=(url,),
            daemon=True
        )
        self.download_thread.start()
    
    def download_worker(self, url):
        """Worker function to handle downloads"""
        try:
            output_path = self.output_path.text()
            audio_only = self.audio_radio.isChecked()
            is_playlist = self.playlist_checkbox.isChecked()
            
            self.downloader = YouTubeDownloader(
                output_path=output_path,
                signals=self.signals
            )
            
            self.signals.status.emit(f"Starting download from: {url}")
            
            if is_playlist:
                success = self.downloader.download_playlist(url)
            else:
                success = self.downloader.download(url, audio_only=audio_only)
            
            self.signals.finished.emit(success)
            
        except Exception as e:
            self.signals.error.emit(str(e))
            self.signals.finished.emit(False)
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def update_status(self, message):
        """Update status log"""
        self.status_log.append(f"→ {message}")
        # Auto-scroll to bottom
        self.status_log.verticalScrollBar().setValue(
            self.status_log.verticalScrollBar().maximum()
        )
    
    def download_finished(self, success):
        """Called when download is finished"""
        self.is_downloading = False
        self.download_btn.setEnabled(True)
        self.download_btn.setText("Download")
        
        if success:
            self.progress_bar.setValue(100)
            QMessageBox.information(
                self,
                "Success",
                "Download completed successfully!\n\nFiles saved to:\n" + 
                self.output_path.text()
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Download failed. Check the log for details."
            )
    
    def show_error(self, error_message):
        """Show error message"""
        self.signals.status.emit(f"ERROR: {error_message}")
