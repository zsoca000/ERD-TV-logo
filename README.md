# ERD-TV-logo

The program is able to put a given logo (in this case a TV channel logo) into a video. Thein nutshell:
- start an encode and decode stream
- read the encoded video frame by frame
- put the logo into the frames
- load the frame with logo into the decode stream's pipe

## Installation
1. Run the `setup.bat` to install all the required dependencies:
   - Python (numpy and pillow)
   - FFmpeg
2. Check the dependencies by running the following command:
   ```cmd
   python --version
   ffmpeg --version


## Useage

1. Open command promt from the program's folder

2. Run the following command:
   ```cmd
   python logo_to_video.py <path_to_your_video>