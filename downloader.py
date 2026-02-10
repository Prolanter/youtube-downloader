#!/usr/bin/env python3
"""
YouTube Downloader Core Module
Handles all download operations
"""

import os
from pathlib import Path
import yt_dlp


class YouTubeDownloader:
    """Download YouTube videos with PyQt5 signal support"""
    
    def __init__(self, output_path="downloads", signals=None):
        """
        Initialize the downloader
        
        Args:
            output_path (str): Directory to save downloaded videos
            signals: PyQt5 signals object for progress updates
        """
        self.output_path = output_path
        self.signals = signals
        self._create_output_directory()
    
    def _create_output_directory(self):
        """Create output directory if it doesn't exist"""
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
    
    def _progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    progress = int((downloaded / total) * 100)
                    if self.signals:
                        self.signals.progress.emit(progress)
                    
                    # Status message
                    speed = d.get('_speed_str', 'N/A')
                    eta = d.get('_eta_str', 'N/A')
                    if self.signals:
                        self.signals.status.emit(
                            f"Downloading... {progress}% | Speed: {speed} | ETA: {eta}"
                        )
            except:
                pass
        
        elif d['status'] == 'finished':
            if self.signals:
                self.signals.progress.emit(100)
                self.signals.status.emit("Download completed, processing video...")
    
    def download(self, url, audio_only=False):
        """
        Download a YouTube video
        
        Args:
            url (str): YouTube video URL
            audio_only (bool): If True, download only audio as MP3
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if audio_only:
                return self._download_audio(url)
            else:
                return self._download_video(url)
        except Exception as e:
            if self.signals:
                self.signals.error.emit(str(e))
            return False
    
    def _download_video(self, url):
        """Download video in highest quality"""
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegMerger',
            }],
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if self.signals:
                    self.signals.status.emit(f"Extracting video information...")
                
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if self.signals:
                    self.signals.status.emit(f"✓ Successfully downloaded: {info['title']}")
                    self.signals.progress.emit(100)
                
                return True
        except Exception as e:
            if self.signals:
                self.signals.error.emit(f"Failed to download video: {str(e)}")
            return False
    
    def _download_audio(self, url):
        """Download audio only as MP3"""
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if self.signals:
                    self.signals.status.emit(f"Extracting audio information...")
                
                info = ydl.extract_info(url, download=True)
                
                if self.signals:
                    self.signals.status.emit(f"✓ Successfully downloaded audio: {info['title']}")
                    self.signals.progress.emit(100)
                
                return True
        except Exception as e:
            if self.signals:
                self.signals.error.emit(f"Failed to download audio: {str(e)}")
            return False
    
    def download_playlist(self, playlist_url):
        """Download all videos from a playlist"""
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegMerger',
            }],
            'outtmpl': os.path.join(self.output_path, '%(playlist_title)s/%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if self.signals:
                    self.signals.status.emit(f"Starting playlist download...")
                
                ydl.download([playlist_url])
                
                if self.signals:
                    self.signals.status.emit("✓ Playlist download completed")
                    self.signals.progress.emit(100)
                
                return True
        except Exception as e:
            if self.signals:
                self.signals.error.emit(f"Failed to download playlist: {str(e)}")
            return False