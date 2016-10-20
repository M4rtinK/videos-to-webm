#!/usr/bin/python

VIDEO_EXTENSIONS = {".mov", ".mp4"}

import os
import stat
import time
import subprocess
import shutil

# find all files in current folder
files = [file for file in os.listdir(".") if os.path.isfile(file)]

# filter out video files we care about
video_files = [file for file in files if os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS]

print("found %d video files that can be converted to webm" % len(video_files))

# convert the video files we have found to webm and keep the modification time of the original
# file so that the converted videos are correctly sorted with photos taken at the same time
for video_file in video_files:
    webm_filename = os.path.splitext(video_file)[0] + ".webm"
    temp_webm_filename = webm_filename + ".part"
    st = os.stat(video_file)
    orig_mtime = st[stat.ST_MTIME]
    orig_atime = st[stat.ST_ATIME]

    # do the webm conversion
    print("converting %s to webm" % video_file)
    # we use a .part suffix for the in-progress file to prevent incomplete
    # webm files to be left behind if the conversion is interrupted for some reason
    command = "ffmpeg -i %s -acodec libvorbis -aq 5 -ac 2 -qmax 25 -threads 4 -f webm %s" % (video_file, temp_webm_filename)
    returncode = subprocess.call(command, shell=True)
    
    # rename the file once it is cussefully converted
    if returncode == 0:
        shutil.move(temp_webm_filename, webm_filename)
    else:
        print("coversion of %s failed" % video_file)
        shutil.remove(temp_webm_filename)
        print("temporary file %s has been removed" % temp_webm_filename)

    
    # set the original mtime and atime on the new file
    print("restoring timestamps for %s" % webm_filename)
    os.utime(webm_filename, (orig_atime, orig_mtime))
