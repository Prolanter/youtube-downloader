# YouTube Downloader - Desktop Application

A simple, user-friendly desktop application to download YouTube videos and playlists in the highest quality.

## Features

**Download Videos in Highest Quality** - Automatically selects best video + audio  
**Download Audio Only** - Extract audio as MP3 files  
**Playlist Support** - Download entire playlists automatically  
**Quality Selection** - Choose specific quality levels  
**Beautiful GUI** - Easy-to-use PyQt5 interface  
**Progress Tracking** - Real-time download progress and status  
**Custom Output Folder** - Save files where you want  

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- FFmpeg (for video/audio processing)

### Step 1: Install FFmpeg

**Windows:**
```bash
pip install ffmpeg-python
```
Or download from: https://ffmpeg.org/download.html

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

### Step 2: Clone or Download the Project

```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install the application as a package:

```bash
pip install -e .
```

## Usage

### Run the Application

**Option 1: Direct Python**
```bash
python main.py
```

**Option 2: Using Console Script (if installed with setup.py)**
```bash
youtube-downloader
```

### Using the App

1. **Enter YouTube URL** - Paste a YouTube video or playlist URL
2. **Choose Download Type** - Select "Video" or "Audio Only"
3. **Select Output Folder** - Click Browse to choose where to save files
4. **Click Download** - Start the download process
5. **Monitor Progress** - Watch the progress bar and status log

## Troubleshooting

### FFmpeg not found
Make sure FFmpeg is installed and added to your system PATH.

**Test FFmpeg:**
```bash
ffmpeg -version
```

### yt-dlp errors
Update yt-dlp to the latest version:
```bash
pip install --upgrade yt-dlp
```

### Download fails
- Check your internet connection
- Try a different video URL
- Check the status log for detailed error messages

## Building a Standalone Executable

### Using PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "YouTube Downloader" main.py
```

The executable will be created in the `dist` folder.
