# ERD-TV-logo

The program is able to put a given logo (in this case a TV channel logo) into a video. The process in nutshell:
- start an encode and decode stream
- read the encoded video frame by frame
- put the logo into the frames
- load the frame with logo into the decode stream's pipe

## Installation
### 1. Setup all the required dependencies
   Run `setup.bat` to:
   - install Python 3.11.9 (win64)
   - install FFmpeg 2025-01-18-12-56 (win64)
   - create desktop shortcut
### 2. Check the dependencies
   Open command line and run:
   ```cmd
   python --version
   ffmpeg --version
   ```
## Useage
   Run the desktop shortcut or the `ERD_TV.bat` file, and browse the video from the explorer.