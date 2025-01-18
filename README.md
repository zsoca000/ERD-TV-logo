# ERD-TV-logo

The program is able to put a given logo (in this case a TV channel logo) into a video. Thein nutshell:
- start an encode and decode stream
- read the encoded video frame by frame
- put the logo into the frames
- load the frame with logo into the decode stream's pipe

## Install dependencies

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