import subprocess
import json
import os
import numpy as np
import shutil
from PIL import Image, ImageDraw, ImageFont
import time
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PyQt6.QtCore import QThread, pyqtSignal

file_location = os.path.dirname(os.path.realpath(__file__))


config = {
    "ERD": {
        "position": (65, 980),  # (X, Y) position on (1920x1080)
        "rel_pos": (65/1920, 980/1080),  # (X, Y) position
        "font_path": os.path.join(file_location,'..',"fonts","NotoSans_ExtraCondensed-SemiBold.ttf"),  # Approximation for Ebrima
        "font_size": 77.1,
        "rel_font_size": 77.1/1080,
        "fill_color": (255, 255, 255),  # White (BGR format)
        "stroke_color": (0, 0, 0),  # Black stroke
        "stroke_width": 2,  # Thickness of the stroke
    },
    "TV": {
        "position": (180, 993),  # (X, Y) position on (1920x1080)
        "rel_pos": (180/1920, 993/1080),  # (X, Y) position
        "font_path": os.path.join(file_location,'..',"fonts","NotoSans_SemiCondensed-SemiBold.ttf"),  
        "font_size": 44,
        "rel_font_size": 44/1080,
        "fill_color": (255, 0, 0),  # Red (BGR format)
        "stroke_color": (0, 0, 0),  # Black stroke
        "stroke_width": 2,  # Thickness of the stroke
    },
}


def sec_to_hms(seconds):
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


class MetaData:

    def __init__(
            self,video_path=None,width=None,height=None,pix_fmt=None,codec_name=None,fps=None,bit_rate=None
    ):
        if video_path is not None:
            meta_data = self._ffmpeg_meta_data(video_path)
            self.width = meta_data['width']
            self.height = meta_data['height']
            self.pix_fmt = meta_data['pix_fmt']
            self.codec_name = meta_data['codec_name']
            self.fps = meta_data['r_frame_rate']
            self.bit_rate = meta_data['bit_rate'] if "bit_rate" in meta_data.keys() else None
            self.nb_frames = meta_data['nb_frames'] if "nb_frames" in meta_data.keys() else None
        else:
            self.width = width
            self.height = height
            self.pix_fmt = pix_fmt
            self.codec_name = codec_name
            self.fps = fps
            self.bit_rate = bit_rate

    def _ffmpeg_meta_data(self,video_path):
        result = subprocess.run(
            ['ffprobe',"-v","error","-show_format","-show_streams","-print_format","json",video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        meta_data = json.loads(result.stdout)
        return meta_data["streams"][0]


class AddLogo:

    def __init__(self,video_path):
        # Pathes
        self.video_path = video_path
        self.work_path = os.path.splitext(video_path)[0]
        extension = os.path.splitext(video_path)[1]
        self.output_path = self.work_path + '_logo' + extension
        self.bytes_path = os.path.join(self.work_path,'bytes.rgb')
        self.audio_path = os.path.join(self.work_path,'audio.wav')
        # Meta data
        self.meta_data  = MetaData(video_path=video_path)

    def process(self):
        os.mkdir(self.work_path)
        self.video2bytes()
        self.video2audio()
        frames = self.bytes2frames()

        frames_logo = [self.logo2frame(frame) for frame in frames]
        frames_logo = np.array(frames_logo)

        self.frames2bytes(frames_logo)
        self.bytes2video()
        self.audio2video()
        shutil.rmtree(self.work_path)



    def video2bytes(self):
        subprocess.run(
            [
                "ffmpeg",
                "-i",self.video_path,
                "-f","rawvideo",
                "-pix_fmt","rgb24",
                self.bytes_path,
             ],
            check=True,
        )
    
    def video2audio(self):
        subprocess.call(
            [
                "ffmpeg","-y",
                "-i",self.video_path,
                "-vn",
                "-acodec","pcm_s16le",
                "-ar","44100",
                "-ac","2",
                self.audio_path,
                "-hide_banner",
                "-loglevel", "error",
            ]
        )
    
    def bytes2frames(self):
        with open(self.bytes_path, "rb") as f:
            frame_data = f.read()
        frame_size = self.meta_data.width * self.meta_data.height * 3
        num_frames = len(frame_data) // frame_size
        frames = np.frombuffer(frame_data, dtype=np.uint8)
        frames = frames.reshape((num_frames,self.meta_data.height,self.meta_data.width,3))
        return frames

    def frames2bytes(self,frames):
        flattened_frames = frames.flatten()
        with open(self.bytes_path, "wb") as f:
            f.write(flattened_frames.tobytes())

    def bytes2video(self):
        cmd = [
            "ffmpeg",
            "-y", # overwrite output file if it's exists
            "-f", "rawvideo", # input fromat
            "-vcodec", "rawvideo", # input codec
            "-s", f"{self.meta_data.width}x{self.meta_data.height}", # size
            "-pix_fmt", "rgb24", # pixel format
            "-r", str(self.meta_data.fps), # frame rate
            "-i", self.bytes_path, # Input from stdin
            "-an", # No audio
            "-vcodec", self.meta_data.codec_name, # Output codec
        ]

        if self.meta_data.bit_rate is not None:
            cmd += ["-b:v",self.meta_data.bit_rate]
        cmd+= ['-pix_fmt', self.meta_data.pix_fmt, self.output_path]

        subprocess.run(cmd,check=True)
    
    def audio2video(self):
        
        tmp_path = self.output_path.replace("logo","tmp")

        subprocess.call(
            [
                "ffmpeg",
                "-y",
                "-i", self.output_path,
                "-i", self.audio_path,
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "copy",
                "-shortest", tmp_path,
                "-hide_banner",
                "-loglevel", "error"
            ]
        )

        os.remove(self.output_path)
        shutil.move(tmp_path,self.output_path)

    def logo2frame(self,frame):
        frame = self.text2frame(frame,'ERD')
        frame = self.text2frame(frame,'TV')
        return frame

    def text2frame(self,frame,text):
        
        params = config[text]

        

        frame_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame_pil)
        font = ImageFont.truetype(params['font_path'], params['font_size'])

        x_pos = params["rel_pos"][0]*frame.shape[1]
        y_pos = params["rel_pos"][1]*frame.shape[0]

        draw.text(
            (x_pos,y_pos),
            text,
            font=font,
            fill=params["fill_color"],
            stroke_fill=params["stroke_color"],
            stroke_width=params["stroke_width"],
        )
    
        frame = np.array(frame_pil)

        return frame


class AddLogoCtk:

    def __init__(self,video_path,loc):
        # Pathes
        self.video_path = video_path
        self.work_path = os.path.splitext(video_path)[0]
        extension = os.path.splitext(video_path)[1]
        self.output_path = self.work_path + '_logo' + extension
        self.audio_path = os.path.join(self.work_path,'audio.wav')
        
        # Meta data
        self.meta_data  = MetaData(video_path=video_path)
        
        # Load logo
        logo_path = os.path.join(file_location,'..',"images","ERDTV-logo.png")
        self.logo = Image.open(logo_path).convert("RGBA")
        scale = 75/1080
        self.logo = self.logo.resize(
            (int(self.logo.width*scale), int(self.logo.height*scale)), 
        )

        # Location
        pos_x = 65/1920
        pos_y = 100/1080
        
        if loc == 'top left':
            self.rel_pos = (pos_x,pos_y)
        elif loc == 'bottom left':
            self.rel_pos = (pos_x,1-pos_y)
        elif loc == 'bottom right':
            self.rel_pos = (1-pos_x,1-pos_y)
        elif loc == 'top right':
            self.rel_pos = (1-pos_x,pos_y)
        

    def process(self,frame_progress:ctk.CTkToplevel=None,label_progress:ctk.CTkLabel=None):
        if not os.path.exists(self.work_path):
            os.mkdir(self.work_path)
        self.save_audio()
        print(f'Audio saved temporarly to {self.audio_path}')
        decode_process = self.create_decode_process()
        print('Decode process started..')
        encode_process = self.create_encode_process()
        print('Encode process started..')
        print('logo put to',self.rel_pos)

        

        if frame_progress is not None:
            if self.meta_data.nb_frames is not None:
                progress_bar = ctk.CTkProgressBar(frame_progress, mode="determinate", width=300)
                progress_bar.pack(pady=20)
                progress_bar.set(0) 

        i = 0
        start_time = time.time()
        try:
            while True:
                frame_size = self.meta_data.width * self.meta_data.height * 3

                raw_frame = decode_process.stdout.read(frame_size)

                if not raw_frame:
                    break  # End of video

                # Convert raw bytes to NumPy array
                frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.meta_data.height, self.meta_data.width, 3))
                frame_logo = self.logo2frame(frame)

                # Write processed frame to encoding process
                encode_process.stdin.write(self.logo2frame(frame_logo).tobytes())
                i+=1
                time_processed = i//eval(self.meta_data.fps)
                time_elapsed = time.time() - start_time
                if self.meta_data.nb_frames is not None:
                    log = f'Frame processed: {i}/{self.meta_data.nb_frames} (processed: {sec_to_hms(time_processed)}) - time elapsed: {sec_to_hms(time_elapsed)}'
                    if progress_bar is not None and frame_progress is not None:
                        progress_bar.set(i/int(self.meta_data.nb_frames))
                else:
                    log = f'Frame processed: {i} (processed: {sec_to_hms(time_processed)}) - time elapsed: {sec_to_hms(time_elapsed)}'
                
                label_progress.configure(text=log)
                frame_progress.update_idletasks()
                print(log,end='\r')

        except KeyboardInterrupt:
            print("Processing interrupted.")
        
        finally:
            # Clean up
            decode_process.stdout.close()
            encode_process.stdin.close()
            decode_process.wait()
            encode_process.wait()
            print(log)
            print('Decode process finished')
            print('Encode process finished')
            self.merge_audio()
            shutil.rmtree(self.work_path)
            print(f'Audio merged')
        
    def create_decode_process(self):
        cmd = [
            "ffmpeg",
            "-i", self.video_path,
            "-f", "image2pipe", # maybe rawvideo?
            "-pix_fmt", "rgb24",
            "-vcodec", "rawvideo",
            "-"
        ]
        
        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

    def create_encode_process(self):
        cmd = [
            "ffmpeg",
            "-y", 
            "-f", "rawvideo", # input fromat
            "-s", f"{self.meta_data.width}x{self.meta_data.height}", # size
            "-pix_fmt", "rgb24", # pixel format
            "-r", str(self.meta_data.fps), # frame rate
            "-i", "-", # Input from pipe
            "-an", # No audio
            "-vcodec", self.meta_data.codec_name, # Output codec
        ]
        
        if self.meta_data.bit_rate is not None:
            cmd += ["-b:v",self.meta_data.bit_rate]
        
        cmd += ['-pix_fmt', self.meta_data.pix_fmt, self.output_path]
        
        return subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    
    def save_audio(self):
        subprocess.call(
            [
                "ffmpeg","-y",
                "-i",self.video_path,
                "-vn",
                "-acodec","pcm_s16le",
                "-ar","44100",
                "-ac","2",
                self.audio_path,
                "-hide_banner",
                "-loglevel", "error",
            ]
        )
    
    def merge_audio(self):
        
        tmp_path = self.output_path.replace("logo","tmp")

        subprocess.call(
            [
                "ffmpeg",
                "-y",
                "-i", self.output_path,
                "-i", self.audio_path,
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "copy",
                "-shortest", tmp_path,
                "-hide_banner",
                "-loglevel", "error"
            ]
        )

        os.remove(self.output_path)
        shutil.move(tmp_path,self.output_path)

    def logo2frame(self,frame):
        # frame = self.text2frame(frame,'ERD')
        # frame = self.text2frame(frame,'TV')
        frame_pil = Image.fromarray(frame)

        position = (int(self.rel_pos[0] * frame.shape[1]), int(self.rel_pos[1] * frame.shape[0]))

        frame_pil.paste(self.logo, position , self.logo)
        return np.array(frame_pil)

    def text2frame(self,frame,text):
        
        params = config[text]

        frame_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame_pil)

        font_size = frame.shape[1]*params['rel_font_size']
        font = ImageFont.truetype(params['font_path'], font_size)

        x_pos = params["rel_pos"][0]*frame.shape[1]
        y_pos = params["rel_pos"][1]*frame.shape[0]

        draw.text(
            (x_pos,y_pos),
            text,
            font=font,
            fill=params["fill_color"],
            stroke_fill=params["stroke_color"],
            stroke_width=params["stroke_width"],
        )
    
        frame = np.array(frame_pil)

        return frame


class AddLogoQWorker(QThread):
    
    progress_signal = pyqtSignal(str)

    def __init__(self,video_path):
        super().__init__()

        # Pathes
        self.video_path = video_path
        self.work_path = os.path.splitext(video_path)[0]
        extension = os.path.splitext(video_path)[1]
        self.output_path = self.work_path + '_logo' + extension
        self.audio_path = os.path.join(self.work_path,'audio.wav')
        
        # Meta data
        self.meta_data  = MetaData(video_path=video_path)
        
        # Load logo
        logo_path = os.path.join(file_location,'..',"images","ERDTV-logo.png")
        self.logo = Image.open(logo_path).convert("RGBA")
        scale = 75/1080
        self.logo = self.logo.resize(
            (int(self.logo.width*scale), int(self.logo.height*scale)), 
        )


    def set_loc(self, loc):
        
        pos_x = 65/1920
        pos_y = 100/1080
        
        if loc == 'Top Left':
            self.rel_pos = (pos_x,pos_y)
        elif loc == 'Bottom Left':
            self.rel_pos = (pos_x,1-pos_y)
        elif loc == 'Bottom Right':
            self.rel_pos = (1-pos_x,1-pos_y)
        elif loc == 'Top Right':
            self.rel_pos = (1-pos_x,pos_y)

    
    def run(self):
        if not os.path.exists(self.work_path):
            os.mkdir(self.work_path)
        self.save_audio()
        print(f'Audio saved temporarly to {self.audio_path}')
        decode_process = self.create_decode_process()
        print('Decode process started..')
        encode_process = self.create_encode_process()
        print('Encode process started..')
        print('logo put to',self.rel_pos)

        i = 0
        start_time = time.time()
        try:
            while True:
                frame_size = self.meta_data.width * self.meta_data.height * 3

                raw_frame = decode_process.stdout.read(frame_size)

                if not raw_frame:
                    break  # End of video

                # Convert raw bytes to NumPy array
                frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.meta_data.height, self.meta_data.width, 3))
                frame_logo = self.logo2frame(frame)

                # Write processed frame to encoding process
                encode_process.stdin.write(self.logo2frame(frame_logo).tobytes())
                i+=1
                time_processed = i//eval(self.meta_data.fps)
                time_elapsed = time.time() - start_time
                if self.meta_data.nb_frames is not None:
                    log = f'Frame processed: {i}/{self.meta_data.nb_frames} (processed: {sec_to_hms(time_processed)}) - time elapsed: {sec_to_hms(time_elapsed)}'
                else:
                    log = f'Frame processed: {i} (processed: {sec_to_hms(time_processed)}) - time elapsed: {sec_to_hms(time_elapsed)}'
                print(log,end='\r')
                self.progress_signal.emit(log)

        except KeyboardInterrupt:
            print("Processing interrupted.")
        
        finally:
            # Clean up
            decode_process.stdout.close()
            encode_process.stdin.close()
            decode_process.wait()
            encode_process.wait()
            print(log)
            print('Decode process finished')
            print('Encode process finished')
            self.progress_signal.emit('Finished!')
            self.merge_audio()
            shutil.rmtree(self.work_path)
            print(f'Audio merged')
        
    def create_decode_process(self):
        cmd = [
            "ffmpeg",
            "-i", self.video_path,
            "-f", "image2pipe", # maybe rawvideo?
            "-pix_fmt", "rgb24",
            "-vcodec", "rawvideo",
            "-"
        ]
        
        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

    def create_encode_process(self):
        cmd = [
            "ffmpeg",
            "-y", 
            "-f", "rawvideo", # input fromat
            "-s", f"{self.meta_data.width}x{self.meta_data.height}", # size
            "-pix_fmt", "rgb24", # pixel format
            "-r", str(self.meta_data.fps), # frame rate
            "-i", "-", # Input from pipe
            "-an", # No audio
            "-vcodec", self.meta_data.codec_name, # Output codec
        ]
        
        if self.meta_data.bit_rate is not None:
            cmd += ["-b:v",self.meta_data.bit_rate]
        
        cmd += ['-pix_fmt', self.meta_data.pix_fmt, self.output_path]
        
        return subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    
    def save_audio(self):
        subprocess.call(
            [
                "ffmpeg","-y",
                "-i",self.video_path,
                "-vn",
                "-acodec","pcm_s16le",
                "-ar","44100",
                "-ac","2",
                self.audio_path,
                "-hide_banner",
                "-loglevel", "error",
            ]
        )
    
    def merge_audio(self):
        
        tmp_path = self.output_path.replace("logo","tmp")

        subprocess.call(
            [
                "ffmpeg",
                "-y",
                "-i", self.output_path,
                "-i", self.audio_path,
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "copy",
                "-shortest", tmp_path,
                "-hide_banner",
                "-loglevel", "error"
            ]
        )

        os.remove(self.output_path)
        shutil.move(tmp_path,self.output_path)

    def logo2frame(self,frame):
        # frame = self.text2frame(frame,'ERD')
        # frame = self.text2frame(frame,'TV')
        frame_pil = Image.fromarray(frame)

        position = (int(self.rel_pos[0] * frame.shape[1]), int(self.rel_pos[1] * frame.shape[0]))

        frame_pil.paste(self.logo, position , self.logo)
        return np.array(frame_pil)

    def text2frame(self,frame,text):
        
        params = config[text]

        frame_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame_pil)

        font_size = frame.shape[1]*params['rel_font_size']
        font = ImageFont.truetype(params['font_path'], font_size)

        x_pos = params["rel_pos"][0]*frame.shape[1]
        y_pos = params["rel_pos"][1]*frame.shape[0]

        draw.text(
            (x_pos,y_pos),
            text,
            font=font,
            fill=params["fill_color"],
            stroke_fill=params["stroke_color"],
            stroke_width=params["stroke_width"],
        )
    
        frame = np.array(frame_pil)

        return frame


def get_frame(video_path, width, height, frame_number=10):

    # Extract frame using FFmpeg
    cmd_frame = [
        "ffmpeg", "-i", video_path, "-vf", f"select='eq(n,{frame_number})'", "-vsync", "vfr",
        "-pix_fmt", "rgb24", "-f", "image2pipe", "-pix_fmt", "rgb24","-vcodec", "rawvideo", "-vframes", "1", "pipe:1"
    ]
    frame_data = subprocess.run(cmd_frame, capture_output=True).stdout

    if not frame_data:
        raise ValueError("FFmpeg did not return any frame data.")

    expected_size = width * height * 3
    if len(frame_data) != expected_size:
        raise ValueError(f"Expected {expected_size} bytes but got {len(frame_data)} bytes.")

    frame = np.frombuffer(frame_data, np.uint8).reshape((height, width, 3))
    return frame

# DECODE: ffmpeg -i samples/sample1.mp4 -f image2pipe -pix_fmt rgb24 -vcodec rawvideo -
# ENCODE: ffmpeg -y -f rawvideo -s 1920x1080 -pix_fmt rgb24 -r 5949/200 -i - -an -vcodec h264 -b:v 915144 -pix_fmt yuv420p samples/sample1_logo.mp4


    


    

    

    
