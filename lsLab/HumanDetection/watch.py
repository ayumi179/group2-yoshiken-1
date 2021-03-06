# ---------------------------------------------------------------------
# modified : 2017/09/22
# filename : watch.py
# function : By running, 
#           automatically detects file added to the folder from raspberry pi 
#           execute yolo to detect person entered/exited
#           crop detected region and save it as a new picture
# Reference: Option1, https://askubuntu.com/questions/518457/autostart-program-whenever-a-file-is-added-to-a-folder
# ---------------------------------------------------------------------

#!/usr/bin/env python

import subprocess
import time

folder = "/home/matlab/lslab/original_images"
command_to_run = """echo 'OK'
# Get timestamp from original image
created=`identify -verbose ./original_images/0.jpg | grep 'create'`
created=${created#*:}
created=${created#*:}
created=${created%+*}
echo ${created}

# Detect person and Crop the region
cd /home/matlab/darknet
./darknet detect cfg/yolo.cfg yolo.weights /home/matlab/lslab/original_images/0.jpg  -thresh 0.6
echo 'darknet done'
cd /home/matlab/lslab

# Change name of cropped image
newfilename=./cropped_images/${created}.jpg
mv ../darknet/cropped.jpg ${newfilename}
echo 'changing name done'
"""

def get_drlist():
    return subprocess.check_output(["ls", folder]).decode('utf-8').strip().split("\n")

while True:
    drlist1 = get_drlist()
    time.sleep(2)
    drlist2 = get_drlist()
    if len(drlist2) > len(drlist1):
        subprocess.Popen(["/bin/bash", "-c", command_to_run])
