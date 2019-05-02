# datavyuVideoGenerator
#### Adam Lavertu
#### 06-2018
Code for generating videos from a directory of individual screenshots. Resizes, labels, and compiles the jpg images into a mp4 video with 10 fps.
Requires file names to contain time stamps in a 20YYMMDDHHmmss format. 

### Requirements
Python 3.6
requirements.txt packages, can be installed using:
```
pip install -r requirements.txt
```
### Usage
Code must be run from the code directory. 
```
python genDatavyuVideo.py </path/to/screenShotDirectory> </path/to/outMovie.mp4>
```  
Warning: The script will use all images in the screenShotDirectory and will load them into memory, so be careful about where you point it. Memory usage can be fixed, but moviepy doesn't support generator objects at the moment so I have no choice but to load into memory. If we really want to create large movies I can rewrite the moviepy class that I'm using.
