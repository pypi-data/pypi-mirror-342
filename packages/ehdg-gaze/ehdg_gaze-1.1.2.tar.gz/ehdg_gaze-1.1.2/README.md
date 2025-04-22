# ehdg_gaze
Eye Health Diagnostic Group Gaze Detector
## Installation requirements and guide
### Step 1: Anaconda Powershell Prompt
If you already have **Anaconda Powershell Prompt**, you can skip this step.  
If you don't, please use this link: https://www.anaconda.com/download to download the **Anaconda Powershell Prompt**.  
### Step 1: Python 3.9
If your base python interpreter is version 3.9, you can skip this step.
If not, please create the virtual environment as follow:

If you are using anaconda, please open the `Anaconda Powershell Prompt` and then
```
conda create -n your-environment-name python=3.9
```
```
conda activate your-environment-name
```
If not, please

(FOR LINUX/MAC)

install venv 
```
sudo apt-get install python3.9-venv
```
create virtual my_env_name
```
python3 -m venv my_env_name
```
activate virtual my_env_name
```
source my_env_name/bin/activate
```

(FOR WINDOWS)

install venv
```
py -m pip install --user virtualenv
```
create virtual my_env_name
```
py -m venv my_env_name
```
activate virtual my_env_name
```
.\my_env_name\Scripts\activate
```

## Step 2: Opencv-python
If your base python interpreter is version 3.9,
```
pip install opencv-python --upgrade
```
if not, activate your virtual environment that your created with python version 3.9 and
```
pip install opencv-python --upgrade
```
## Step 3: Installation
```
pip install vinset -U
```
_________________________________
# User guide
```
vinset -i input.mp4 [-d gaze.csv] -o output.mp4 -c config.json [-t graph or text] [-tl timeline.json]
```
## -i flag
It is the flag for input video file such as mp4, mov etc. The file type must be video.  

## -d flag
It is the flag for csv data file to be used as reference data. The file type must be .csv.  It must contain the time column in order to synchronize the data and video.  
It is mandatory input for vinset to run except user only wants to draw normal texts which are not data and time related.

## -o flag
It is the flag for out video file. The file type must be .mp4.  

## -c flag
It is the flag for config file which contains all information about how, what and where we draw on the video. The file type must be .config or .json.  

## -t flag
The vinset version 5.0.0 and above does not require this -t flag anymore but it is still acceptable to draw with older version of drawing.  
To draw with older version, there are 2 types of overlay.  
1.  graph overlay  
2.  text overlay
### Example usage of graph overlay
```
vinset -t graph -i input_video.mp4 -o output_video.mp4 -d gaze.csv -c config.json 
```
### Example usage of text overlay  
```
vinset -t text -i input_video.mp4 -o output_video.mp4 -c config.json -tl timeline.json
```

## -tl flag
It is the flag for timeline file to be used with text overlay drawing. The file type must be .json.  




_________________________________
# Version upgrade guide
## To check the version of currently installed
```
vinset --version
```
## To upgrade the vinset to latest version
```
pip install vinset --upgrade
```
