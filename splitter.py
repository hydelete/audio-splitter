#!/usr/bin/env python3
import os
import sys
import subprocess

def split_audio(input_file):
    # 25 minutes = 1500 seconds
    segment_time = "1500" 
    
    # Setup paths
    input_path = os.path.abspath(input_file)
    dir_name = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    name, ext = os.path.splitext(base_name)
    
    # Define output pattern: Filename part1.ext, part2.ext...
    # FFmpeg's segment_list_type starts at 0, so we use a flag to start naming correctly
    output_pattern = os.path.join(dir_name, f"{name} part%d{ext}")

    # Steam Deck built-in ffmpeg command
    cmd = [
        "ffmpeg", "-i", input_path,
        "-f", "segment", 
        "-segment_time", segment_time,
        "-segment_start_number", "1",    # This ensures it starts at 'part1' not 'part0'
        "-c", "copy",                    # No quality loss, instant speed
        "-reset_timestamps", "1",
        output_pattern
    ]

    print(f"--- Splitting: {base_name} ---")
    
    try:
        # Run the split
        subprocess.run(cmd, check=True)
        
        # Success popup on Steam Deck
        subprocess.run([
            "zenity", "--info", 
            "--text", f"Success! Created parts for {name} in the same folder.", 
            "--title", "Splitter Done",
            "--width=300"
        ])
    except Exception as e:
        subprocess.run([
            "zenity", "--error", 
            "--text", f"Failed to split file: {str(e)}", 
            "--title", "Error"
        ])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        split_audio(sys.argv[1])
    else:
        # File picker for when you launch it as an app
        try:
            file_picker = subprocess.check_output([
                "zenity", "--file-selection", 
                "--title=Select Audio File to Split",
                "--file-filter=Audio files | *.mp3 *.wav *.ogg *.flac *.m4a"
            ]).decode("utf-8").strip()
            if file_picker:
                split_audio(file_picker)
        except subprocess.CalledProcessError:
            print("No file selected.")