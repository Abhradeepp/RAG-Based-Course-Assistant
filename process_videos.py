#convert the videos in to mp3

import os 
import subprocess

files = os.listdir("videos")
for file in files:
    tutorial_number = file.split(" - CodeWithHarry")[0].split(" #")[1]
  
    if '-sigma-web-development-course' in file:
        file_name = file.split("-sigma-web-development-course")[0]
        
    elif ' Sigma Web Development Course' in file:
        file_name = file.split(" Sigma Web Development Course")[0]

    output_path = f"audios/{tutorial_number}_{file_name}.mp3"
    if os.path.exists(output_path):
        continue
    print(file_name, tutorial_number)
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{tutorial_number}_{file_name}.mp3"])
