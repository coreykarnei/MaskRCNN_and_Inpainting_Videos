# MaskRCNN_and_Inpainting_Videos
This is a pipeline that seamlessly combines the masking power of MaskRCNN with the inpainting abilities of DeepFillv2 in order to remove as many as 80 types of objects from a video. 
# Installation
In order to run, clone this project and create a new Conda enviornment. Once inside the new enviornment, run the following command:
```
conda install python=3.6
```
Then, navigate to the directory where this project is located and run
```
pip install -r reqirements.txt --user
```
This will install the required packages. Finally visit [this drive](https://drive.google.com/drive/folders/1y7Irxm3HSHGvp546hZdAZwuNmhLUVcjO), download *snap-0.meta* and *snap-0.data-00000-of-00001*, then drop these files into **model_logs\release_places2_256**.
After that you are ready to go!
# Usage
To process a video, run a command of the following structure:
```
python main.py --video PathToVideo --object ObjectsToMask
```
Where PathToVideo is a string path to the video you wish to process, and ObjectsToMask is a string comprised of comma-seperated classes that you want removed. These must be listed in MaskRCNN's existing classes located at ~~ . ObjectsToMask can include one class or several. Some examples include
```
"person"
"bottle, apple"
"automobile, fork, bowl"
```
You can try removing the person in the test video using the following command:
```
python main.py --video "videos/test.mov" --object "person"
```
