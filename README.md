
https://user-images.githubusercontent.com/31517198/118027844-03dfe280-b328-11eb-97fd-1c59a83efabe.mp4

# MaskRCNN_and_Inpainting_Videos
This is a pipeline that seamlessly combines the masking power of MaskRCNN with the inpainting abilities of DeepFillv2 in order to remove as many as 80 types of objects from a video. Simply say "Abracadabra [object]" in the video and this system will automatically detect that, mask the object, and inpaint it to give the illusion that the object has vanished!
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
python main.py --video PathToVideo
```
Where PathToVideo is a string path to the video you wish to process. Additionally, you can also adjust the Inflation and Minimum Confidence. Minimum Confidence refers to the minimum value that MaskRCNN needs in order to consider a detected object as valid. By default this value is 0.5. Inflation referes to the number of pixels to 'inflate' the object mask by, making it grow by that number of pixels in each direction. By default this value is 5. 
![dubBot](https://user-images.githubusercontent.com/31517198/118028235-781a8600-b328-11eb-824c-3e61d367fa72.png)
Above you can see an object mask with and without inflation. The small pieces of the bottle that remain uncovered when there is no inflation causes the 'vanishing' effect to not work nearly as well.

These parameters can be set in the following way:
```
python main.py --video PathToVideo --inflation inflationValue --minConfidence confidenceValue
```

You can try removing the bottle in the test video using the following command:
```
python main.py --video "videos/bottle.mov"
```
