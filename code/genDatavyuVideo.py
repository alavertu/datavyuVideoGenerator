# genDatavyuVideo.py
# Adam Lavertu
# alavertu@stanford.edu
"""Given a target directory and output video filename, this script generates a time ordered video of the screenshots within the target directory. It is currently set to 10 fps and the images must contain the date in the file names as format 20YYMMDDHHmmss."""

import os
import re
import sys

import numpy as np
import pandas as pd
import moviepy.editor as mpy
from skimage import io
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

if len(sys.argv) != 3:
    print("ERROR: Incorrect input")
    print("USAGE: python genDatavyuVideo.py </path/to/targetDirectory> </path/to/outVideo.mp4>")
    exit()

targetDir = sys.argv[1]
outVideoPath = sys.argv[2]

fontSize = 48
font = ImageFont.truetype("../data/resources/Hack-Bold.ttf", fontSize)

# Loads valid images and returns False if image is corrupted.
def is_valid(filePath):
    try:
        test = io.imread(filePath)
        return test
    except:
        return False

# Iterates over fileList and returns the index of the first image that is no corrupted
def findFirstNonCorrupt(fileList):
    i = 0
    trial = is_valid(fileList[i])
    if trial is not False:
        return(i)
    else:
        while(trial is False):
            i += 1
            trial = is_valid(fileList[i])
    return(i)

# class imgDirGenerator(object):
def imgDirGenerator(dirPath):
    
    fileList = os.listdir(dirPath)
    
    # Use regex to extract timeStamp from fileName
    timeStamp = [int(re.search(r'(20[0-9]{12})',x).group(1)) for x in fileList]
    fullPathFileList = [os.path.join(dirPath, x) for x in fileList]
    outFrame = pd.DataFrame({'fileName':fullPathFileList, 'timeStamp':timeStamp})
    
    # Sort images by timeStamp
    outFrame = outFrame.sort_values('timeStamp')
    orderedFiles = outFrame['fileName'].tolist()
    startIndex = findFirstNonCorrupt(orderedFiles)
    
    # Get the frame size and relative locations for subject ID
    frame = Image.open(orderedFiles[startIndex]).size
    x_loc = frame[0]//2
    y_loc = frame[1] - (frame[1]//4)
    
    # Process and label images
    for i in range(startIndex, len(orderedFiles)):
        # Exclude corrupt images
        try:
            img = Image.open(orderedFiles[i])
        except:
            continue
        try:
            img = img.resize(frame)
        except:
            continue
        tempDraw = ImageDraw.Draw(img)
        
        # Label image
        boxSize = tempDraw.textsize(os.path.basename(orderedFiles[i]),font=font)
        x_pos = x_loc - boxSize[0]//2
        y_pos = y_loc - boxSize[1]//2
        tempDraw.rectangle([x_pos-5, y_pos-5,
                  x_pos + boxSize[0] + 5, y_pos + boxSize[1] + 5], 
                           fill=(0,0,0))
        tempDraw.text((x_pos, y_pos),orderedFiles[i],(255,255,255),font=font)
        yield(np.array(img))

print("Starting image import and resizing...")

testGen = imgDirGenerator(targetDir)

testList = [x for x in testGen]

print("Generating output video...")
clip = mpy.ImageSequenceClip(testList, fps=10)

clip.write_videofile(outVideoPath, audio=False)
print("Done!")
