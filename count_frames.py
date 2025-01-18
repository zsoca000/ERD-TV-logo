import subprocess
import json

def get_frame_count_fast(video_path):
    command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=nb_frames",
        "-print_format", "json",
        video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        print("Error:", result.stderr)
        return None

    metadata = json.loads(result.stdout)
    if "streams" in metadata and len(metadata["streams"]) > 0 and "nb_frames" in metadata["streams"][0]:
        return int(metadata["streams"][0]["nb_frames"])
    else:
        print("Frame count not found in metadata.")
        return None

# Example usage
video_file = "samples/The.Big.Short.2015.720p.mHD.BluRay.x264.HuN-sokadiklany.mkv"
frame_count = get_frame_count_fast(video_file)
if frame_count is not None:
    print(f"The video has {frame_count} frames.")
else:
    print("Failed to get the frame count.")