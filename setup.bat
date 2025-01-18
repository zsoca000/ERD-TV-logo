@echo off

:: Check for Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Python...
    :: Download Python installer using PowerShell
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.x.x/python-3.x.x.exe -OutFile python_installer.exe"
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
)

:: Check for FFmpeg installation
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing FFmpeg...
    :: Download FFmpeg using PowerShell
    powershell -Command "Invoke-WebRequest -Uri https://ffmpeg.org/releases/ffmpeg-4.x.x-win64-static.zip -OutFile ffmpeg.zip"
    powershell -command "Expand-Archive -Path ffmpeg.zip -DestinationPath ."
    move ffmpeg-4.x.x-win64-static\bin\ffmpeg.exe C:\Windows\System32

    :: Add FFmpeg to PATH (if not added already)
    setx PATH "%PATH%;C:\ffmpeg-4.x.x-win64-static\bin"
)

:: Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

echo Setup complete!