# ERD-TV-logo

The program is able to put a given logo (in this case a TV channel logo) into a video. Thein nutshell:
- start an encode and decode stream
- read the encoded video frame by frame
- put the logo into the frames
- load the frame with logo into the decode stream's pipe

## Dependencies

### FFmpeg