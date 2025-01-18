# ERD-TV-logo

The program is able to put a given logo (in this case a TV channel logo) into a video. Thein nutshell:
- start an encode and decode stream
- read the encoded video frame by frame
- put the logo into the frames
- load the frame with logo into the decode stream's pipe

## Install dependencies

### Python

#### Step 1: Download Python
1. Visit the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. On the homepage, you'll see the **"Download Python"** button. This will typically download the latest stable version.
3. Alternatively, you can click on **"View the full list of downloads"** for older versions or platform-specific options.

#### Step 2: Install Python
1. Once the installer is downloaded, run the executable file to begin the installation.
2. **Important**: Check the box that says **"Add Python to PATH"** before clicking **Install Now**. This ensures Python is added to your system’s environment variables, making it accessible from the command line.
3. Follow the prompts to complete the installation. You can use the default settings unless you have specific preferences.

#### Step 3: Verify the Installation
1. Open a **Command Prompt** (press **Win + R**, type `cmd`, and press **Enter**).
2. Type the following command to verify that Python is installed and accessible:
   ```cmd
   python --version

#### Step 4: Install python dependencies
1. Install **numpy** and **Pillow**, run the following command in your terminal:
    ```cmd
    pip install numpy Pillow


### FFmpeg

#### Step 1: Download FFmpeg
1. Go to the official FFmpeg website: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
2. Under **Get packages & executable files**, select **Windows** (e.g., from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)).
3. Download the **"Full" build** ZIP file.

#### Step 2: Extract FFmpeg
1. Extract the downloaded ZIP file to a folder (e.g., `C:\ffmpeg`).
2. Inside the folder, you should see a `bin` directory containing the `ffmpeg.exe` file.

#### Step 3: Add FFmpeg to the System PATH
1. **Open System Environment Variables**:
   - Press **Win + X** and select **System**.
   - In the **System** window, click **Advanced system settings** on the left.
   - In the **System Properties** window, click the **Environment Variables** button.
   
2. **Edit the System Path**:
   - Under **System variables**, scroll down and select the `Path` variable, then click **Edit**.
   - In the **Edit environment variable** window, click **New**.

3. **Add FFmpeg’s `bin` Folder to the PATH**:
   - Add the path to the `bin` directory where `ffmpeg.exe` is located (e.g., `C:\ffmpeg\bin`).
   - Click **OK** to save.

#### Step 4: Verify the Installation
1. Open a **Command Prompt** (press **Win + R**, type `cmd`, and press **Enter**).
2. Type the following command to verify that FFmpeg is accessible:
   ```cmd
   ffmpeg -version