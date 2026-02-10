#!/usr/bin/env python3
"""
Setup script for YouTube Downloader
Allows installation as a standalone application
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="youtube-downloader-app",
    version="1.0.0",
    author="Your Name",
    description="A simple desktop application to download YouTube videos in highest quality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "PyQt5>=5.15.0",
        "yt-dlp>=2024.1.0",
    ],
    entry_points={
        "console_scripts": [
            "youtube-downloader=main:main",
        ],
    },
)