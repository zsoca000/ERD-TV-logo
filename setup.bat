@echo off

:: Check for Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Python...
    :: Download Python installer
    curl -o python_installer.exe https://www.python.org/ftp/python/3.x.x/python-3.x.x.exe
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
)

:: Check for FFmpeg installation
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing FFmpeg...
    :: Download FFmpeg
    curl -L https://ffmpeg.org/releases/ffmpeg-4.x.x-win64-static.zip -o ffmpeg.zip
    tar -xf ffmpeg.zip
    move ffmpeg-4.x.x-win64-static\bin\ffmpeg.exe C:\Windows\System32

    :: Add FFmpeg to PATH
    setx PATH "%PATH%;C:\ffmpeg\bin"
)

:: Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

echo Setup complete!