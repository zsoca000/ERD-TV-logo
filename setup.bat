@echo off
setlocal

:: Check for Python installation
echo Checking for Python installation...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe -OutFile python_installer.exe"
    if %errorlevel% neq 0 (
        echo Error downloading Python installer. Exiting...
        exit /b 1
    )
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo Error installing Python. Exiting...
        exit /b 1
    )
    echo Python installed successfully.
) else (
    echo Python is already installed.
)

:: Check for FFmpeg installation
echo Checking for FFmpeg installation...
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo FFmpeg is not installed. Installing FFmpeg...
    powershell -Command "Invoke-WebRequest -Uri https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2025-01-18-12-56/ffmpeg-N-118321-g4c96d6bf75-win64-lgpl.zip -OutFile ffmpeg.zip"
    if %errorlevel% neq 0 (
        echo Error downloading FFmpeg. Exiting...
        exit /b 1
    )
    powershell -command "Expand-Archive -Path ffmpeg.zip -DestinationPath ."
    if %errorlevel% neq 0 (
        echo Error extracting FFmpeg. Exiting...
        exit /b 1
    )
    move ffmpeg-N-118321-g4c96d6bf75-win64-lgpl C:\
    if %errorlevel% neq 0 (
        echo Error moving FFmpeg executable. Exiting...
        exit /b 1
    )
    setx PATH "%PATH%;C:\ffmpeg-N-118321-g4c96d6bf75-win64-lgpl\bin"
    if %errorlevel% neq 0 (
        echo Error adding FFmpeg to PATH. Exiting...
        exit /b 1
    )
    echo FFmpeg installed successfully.
) else (
    echo FFmpeg is already installed.
)

:: Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing Python dependencies. Exiting...
    exit /b 1
)
echo Python dependencies installed successfully.

: CREATE SHORTCUT

: Define variables for paths
set BAT_FILE_PATH=%~dp0ERD_TV.bat
set SHORTCUT_PATH=%USERPROFILE%\Desktop\ERD_TV.lnk
set ICON_PATH=%~dp0images\logo.ico

:: Call the VBScript to create the shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut("%SHORTCUT_PATH%") >> CreateShortcut.vbs
echo oLink.TargetPath = "%BAT_FILE_PATH%" >> CreateShortcut.vbs
echo oLink.IconLocation = "%ICON_PATH%" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

:: Run the VBScript
cscript //nologo CreateShortcut.vbs

:: Clean up the temporary VBScript
del CreateShortcut.vbs

echo Shortcut created successfully!

echo Setup complete!

pause
endlocal
